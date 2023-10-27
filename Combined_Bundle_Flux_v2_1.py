#######################################################
###     This code is the main routine to combine    ###
###     simulated SV tracks on an axon from         ###
###     different synapse starting locations.       ###
#######################################################
###     Written By: M.W. Gramlich                   ###
###     Last Date Modified: 09/2023                 ###
#######################################################
###     Version 1 of this code selects tracks from  ###
###     each synapse randomly, and then replaces    ###
###     the track. New tracks are selected at set   ###
###     intervals of time.                          ###
###                                                 ###
###     If a track reaches x = 0, it is counted in  ###
###     the flux array at that time and is no longer###
###     included in the simulation.                 ###
#######################################################
###     Version 2 of this algorithm allows for      ###
###     two different distributions of vesicles     ###
###     chosen by random threshold choices          ###
#######################################################

###################################################
###	This model operates in the following order  ###
### [1] Load all subroutines                    ### 
### [2] Initiate all Variables for bundle       ###
### [3] Define locations of track files         ###  <------- Note this is important! You must manually input where the track data is located!
### [4] Initiate/Create Directories for files   ###
### [5] Start main routine for N-SVs            ###
### [6] Run through individual synapse location ###
###     [i]  Select individual tracks randomly  ###
###     [ii] Add track to bundle at given time  ###
###     [iii]Continue for N-tracks every t-secs ### 
### [7] Repeat step [6] at different synapses   ###
### [8] Output combined SV density and flux     ###
###################################################

###################################################
### Important Notes about the philosophical     ###
### apporach of this model:                     ###
### [A] All random processes are treated as     ###
###     stochastic. Including motor randomness  ###
### [B] Probabilistic choices are made by       ###
###     a static threshold comparison.          ###
### [C] A bootstrapping approach is used for    ###
###     loading single SV tracks. This means    ###
###     that a collection of individual tracks  ### 
###     at each assumed synapse location. Then  ###
###     a single track is drawn at random from  ###
###     that collection. It is then added to the###
###     axon bundle simulation at the time it is###
###     selected. This is repeated as many times###
###     as desired.                             ###
###################################################


#--------------------------------------------------------------#
#---               Stage [1]                                ---#

import csv
import sys
import string
import math
import cmath
import numpy as np	#import package numpy and give it the designation "np"
import os
import random
import matplotlib.pyplot as plt

from mypyfuncs_os import check_make_dir


####################################################
def linecount(filename):
	myinput = open(filename,'r')
	lines = 0
	while myinput.readline():
		lines += 1
	return lines

####################################################


# Note: Define the version number of the model here
ver_num = "v_F2_1"

#--------------------------------------------------------------#
#---               Stage [2]                                ---#

# Let's start by defining initial variables
Release_Rate = 30      # This is the rate a new SV is selected to leave a synapse
Bundle_size = 3030      # This is the size of the axon bundle that will combine all individual tracks
Time_STEP = 100000     # Total number of time-steps
Num_tracks = 99        # How many tracks exist in the database for each synapse?
P_choice = 0.20        # Fraction of Vesicles in the Fast motion distribution

# Now variables that come from the low-level model of individual synapses
Dist_syn = 30         # This is the distance between synapses

# Let's create arrays used to store resulting simulation

Bundle = [[float(0.0) for x in range(int(Bundle_size))] for z in range(0,int(Time_STEP))]	# Generate "array" to store bundle data
Soma_Flux = [[float(0.0) for x in range(0,2)] for z in range(0,int(Time_STEP))]	            # Generate "array" to store flux data

#--------------------------------------------------------------#
#---               Stage [3]                                ---#

# Define location where files will be selected from and/or data saved to
dir_slow = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\Low Mobility Equal Capture\\"
#dir_fast = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\High Mobility Ant_75_Ret_25\\"
#dir_fast = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\High Mobility Ant_75_Ret_5\\"
dir_fast = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\High Mobility Equal Capture\\"

#--------------------------------------------------------------#
#---               Stage [4]                                ---#

# Define location where data will be saved to
dir_out = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\"
Flux_out = "Flux_simulation_1.txt"
outro_flux = open(dir_out + Flux_out, "w")  # Open Flux file
outro_bundle = open(dir_out + "Bundle_Simluation_1.txt", "w")  # Open Flux file
outro_bundle2 = open(dir_out + "Bundle_Simluation_2.txt", "w")  # Open Flux file
outro_flux_syn = open(dir_out + "Flux_synapse_out.txt", "w")  # Open Flux file

#--------------------------------------------------------------#
#---               Stage [5]                                ---#

Track_SV = []
Track_Dist = []
Track_Syn = []
# Set code to run through multiple synapses
for j in range(1,99):
    # Define the synapse(s) to be selected
	print("Current Synapse: %f\n" % (j*Dist_syn))
	curr_syn = "synapse_" + str(j*Dist_syn)

    # Define EPOCH time for simulation
	for T_EPOCH in range (0, 599):           # This is the starting point 
		if T_EPOCH < 100: T_sim = T_EPOCH*Release_Rate        # Scale the time based on release rate
		if T_EPOCH >= 100 and T_EPOCH < 200: T_sim = (T_EPOCH-100)*Release_Rate        # Scale the time based on release rate
		if T_EPOCH >= 200 and T_EPOCH < 300: T_sim = (T_EPOCH-200)*Release_Rate        # Scale the time based on release rate
		if T_EPOCH >= 300 and T_EPOCH < 400: T_sim = (T_EPOCH-300)*Release_Rate        # Scale the time based on release rate
		if T_EPOCH >= 400 and T_EPOCH < 500: T_sim = (T_EPOCH-400)*Release_Rate        # Scale the time based on release rate
		if T_EPOCH >= 500 and T_EPOCH < 600: T_sim = (T_EPOCH-500)*Release_Rate        # Scale the time based on release rate
        
#----->			print(T_sim)       #-----> If you need to check the track currently running, have this line uncommented 
#--------------------------------------------------------------#
#---               Stage [6,7]                              ---#

    # Run through all tracks for a given synapse

# Draw an unweighted random number used to select the track
		i = Num_tracks*np.random.rand()
    # Define specific track(s) to be selected
		curr_track = "Trap-model_motor-position_v3_2-#" + str(int(i)) + ".txt"
#	t = linecount(input_dir2+input_file)
		tmp_rnd = np.random.rand()
		if tmp_rnd >= P_choice: 
			input_dir2 = dir_slow + curr_syn + "\\"
			Track_SV.append(0)
			Track_Dist.append(int(j))
		if tmp_rnd < P_choice: 
			input_dir2 = dir_fast + curr_syn + "\\"
			Track_SV.append(1)
			Track_Dist.append(int(j))
#----->			print(input_dir2)        
		t = linecount(input_dir2+curr_track)             # Find out how big the file is
		intro_track = open(input_dir2+curr_track, "r")  # Open Track file

# Read line-by-line until the end
		while True:
			r2 = intro_track.readline()
			cols2 = r2.split()
			t_track = 0
			x_track = 1
			if len(cols2) > 0 :
				t_track = (float(cols2[0]))             # Select the position column (see original track file(s) to know which one)
				x_track = (float(cols2[4]))             # Select the position column (see original track file(s) to know which one)
#----->			print(t_track, x_track)       #-----> If you need to check that the track data was read in correctly have this line uncommented 
# Add the location of the current track to the axon lattice bundle. If another track is already there, add on top of it
			if x_track < Bundle_size and ( (t_track+T_sim) < Time_STEP):
				Bundle[int(t_track+T_sim)][int(x_track)] = Bundle[int(t_track+T_sim)][int(x_track)] + 1

			if x_track == 0 and ( (t_track+T_sim) < Time_STEP):
				Soma_Flux[int(t_track+T_sim)][1] = Soma_Flux[int(t_track+T_sim)][1] + 1
				Track_Syn.append(j)
#----->					print(t_track+T_sim, x_track)       #-----> If you need to check that the track data was read in correctly have this line uncommented 	

			if not r2: break


#--------------------------------------------------------------#

#--------------------------------------------------------------#
#---               Stage [8]                                ---#

for t_tmp in range(1,Time_STEP):
	outro_flux.write(("%d\t%f\n") % (t_tmp, Soma_Flux[int(t_tmp)][1]) )

outro_flux.close()

for t_tmp in range(1,len(Track_Syn)):
	outro_flux_syn.write(("%f\n") % (Track_Syn[int(t_tmp)]) )

outro_flux_syn.close()

for t_tmp in range(1,int(Time_STEP/10)):
	for x_tmp in range(1,Bundle_size):
		outro_bundle.write( ("%f\t") % (Bundle[int(t_tmp)][int(x_tmp)] ))
	print(("%d\n") % (t_tmp))
	outro_bundle.write(("\n") )
outro_bundle.close()

for t_tmp in range(int(Time_STEP/10),int(2*Time_STEP/10)):
	for x_tmp in range(1,Bundle_size):
		outro_bundle2.write( ("%f\t") % (Bundle[int(t_tmp)][int(x_tmp)] ))
	print(("%d\n") % (t_tmp))
	outro_bundle2.write(("\n") )
outro_bundle2.close()

for inc in range(1,int(Time_STEP/10)):
	print(inc)    
	outro_bundle = open(dir_out + "Bundle_Simluation_" + str(inc) + ".txt", "w")  # Open Flux file
	for t_tmp in range(int((inc-1)*Time_STEP/10),int(inc*Time_STEP/10)):
		for x_tmp in range(1,Bundle_size):
			outro_bundle.write( ("%f\t") % (Bundle[int(t_tmp)][int(x_tmp)] ))
#		print(("%d\n") % (t_tmp))
		outro_bundle.write(("\n") )
	outro_bundle.close()
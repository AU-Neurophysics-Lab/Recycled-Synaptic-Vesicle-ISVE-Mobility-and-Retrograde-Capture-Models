###################################################
### This code simulates vesicle motility and    ###
### presynapse capture during axonal motion.    ###
###                                             ###
###  This is the first phase of the simulation  ###
###  This code generates a collection of single ###
###  SV tracks starting from different spots    ###
###---------------------------------------------###
### Written By:          Michael W. Gramlich    ###
### Date:                10/2023                ###
###---------------------------------------------###
### Published in: Frontiers in                  ###
### Cell and Developmental Biology Cell Growth  ###
### and Division.                               ###
###                                             ###
### Recently Recycled Synaptic Vesicles Use     ###
### Multi-Cytoskeletal Transport and Differen-  ###
### tial Presynaptic Capture Probability to     ###
### Establish a Retrograde Net Flux During ISVE ###
### in Central Neurons.                         ###
###                                             ###
###  M. Parkes, N.L. Landers, M.W. Gramlich     ###
###################################################

###################################################
###	This model operates in the following order  ###
### [1] Load all subroutines                    ### 
### [2] Initiate all Variables for SV motion    ###
### [3] Initiate Array to store SV positions    ###
### [4] Initiate/Create Directories for files   ###
### [5] Start main routine for N-synapses       ###
### [6] Generate SV track from sub-routine      ###
### [7] Output final combined SV results        ###
###################################################

###################################################
### Important Notes about the philosophical     ###
### apporach of this model:                     ###
### [A] All random processes are treated as     ###
###     stochastic. Including motor randomness  ###
### [B] Probabilistic choices are made by       ###
###     a static threshold comparison.          ###
### [C] Differences between actin/MT motility   ###
###     are treated as differences in speeds    ###
### [D] SVs transport is independent of other   ###
###     SVs along the axon                      ###
###################################################

import os
from mypyfuncs_os import check_make_dir
from mypyfuncs_motorcode_vS4 import four_param_motorv3_2


# Note: Define the version number of the model here
ver_num = "v_S6_1"


#--------------------------------------------------------------#

#---------------------#
#  Initial Variables  #


detachment_prob = 0.00
reatachment_prob = 1.0
reversal_prob = 0.5
motor_stop = 0
N_motors = 100
Latt_conv = 100         # This is the nanometers per lattice site
Time_conv = 200         # This is the msec per time-step
velocity = 1            # This number should be given in lattice sites per time-step
STDEV_vel = 0       	# This number should be given in lattice sites per time-step
Resolution = 1          # This is the resolution in number of lattice-sites/pixel
P_ON = 100;             # This is a parameter for the number of time-steps a motor will pause
Mod_P = 1;		        # This parameter allows for consecutive runs between pausing
Time_STEP = 100000      # Total number of time-steps
#--------------------#





dir = os.getcwd() + "\\2D-motor simulation data\\Slow_Bi-directionalCapture\\"

#-----------------------------------------------#
#	Initialize bundle lattice		#

Bundle_size = 14000
Lambda = 20	# Define Distance Between Synapses
Dist_syn = Lambda+10    # Distance between synapse center locations is distance between synapses plus size of synapse
m_start = Dist_syn

mean_Ph = 0.75         # This is the direction-independent pause probability
Ant_Ph = 0.75         # This is the anterograde-dependent pause probability
Ret_Ph = 0.75         # This is the Retrograde-dependent pause probability

N_MT = 5
re_scale = 1	# minimum re-scale of bundle in lattice units
x_max = 9030

motor_stop = Bundle_size/re_scale

# The index i represents the number of synapses to be modeled
for i in range(0,99):	

# Generate the bundle for this particular synapse
	Bundle = [[float(0.0) for x in range(int(2))] for z in range(0,int(Bundle_size))]	# Generate "array" to store bundle data
 	# Generate synapse locations
	for j in range(1,int(Bundle_size/Dist_syn)-1): Bundle[int(j*Dist_syn)][0] = 1.0

	MTd = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
	syndir = dir +"synapse_" + str(m_start + i*Dist_syn) + "\\"
	check_make_dir(syndir)

	r = four_param_motorv3_2(Bundle, x_max, detachment_prob, reatachment_prob, reversal_prob, Lambda, mean_Ph, velocity, syndir, N_motors, N_MT, MTd, m_start + i*Dist_syn,Bundle_size, P_ON, Ant_Ph, Ret_Ph, Time_STEP)


###################################################
### This code simulates vesicle motility and    ###
### presynapse capture during axonal motion.    ###
###                                             ###
###  This is the subroutine that generates a    ###
###  single SV track following parameters given ###
###  by the main routine.                       ###
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
### [5] Start main routine for N-SVs            ###
### [6] Run through individual SV steps         ###
### [7] Output each individual SV track results ###
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

import numpy as np	#import package numpy and give it the designation "np"



#--------------------------------------------------------------#
#--------------------------------------------------------------#
#      This version takes a 2Dimensional lattice
#--------------------------------------------------------------#
def four_param_motorv3_2(lattice, x_max, Pd, Pa, Pr, Lambda, mean_Ph, velocity, location, Num_Motors, y_MT, MTs, x_start,Bundle_size, Pause_time_synapse, Ant_prob, Ret_prob, Time_STEP):

	x1 = x_start			# Initialize motor at initial x-position. This keeps track of x-position
	x_conversion = 0.0 
#---------------------------#
#   Loop of motors	    #

	for i in range(0, Num_Motors):
		curr_out = open( str(location) + "/Trap-model_motor-position_v3_2-#" + str(int(i)) + ".txt","w")		# Open current output file
		curr_position = x1 			# Make conversion if desired
		memory1 = 0				#Memory of Pause at synapse
		Bundle_tmp_t = [[float(0.0) for x in range(int(1))] for z in range(0,int(Time_STEP))]	# Generate "array" to store bundle data
		Bundle_tmp_x = [[float(0.0) for x in range(int(1))] for z in range(0,int(Time_STEP))]	# Generate "array" to store bundle data

	# Reset all values to starting value
		t = 0				# Initial simulation start time
		
		y1 = 0.0			# This keeps track of the MT the motor is on during the simulation
		Start_prob = np.random.rand()   #Pull a random MT start location probability between (0,1)
		kk = 0
		curr_velocity = velocity	# Initialize motor velocity toward distal regardless of MT

	
		while t < Time_STEP:			# Run the simulation until the end of the lattice
			t += 1


		#----------------------------------------------#
		#    Reflecting Barrier at end of bundle 	   #
			if curr_position > x_max:
				curr_velocity = -velocity
			if curr_position <= 0:
				curr_velocity = 0
				curr_out.close()
				break


		#----------------------------------#
		#Get random numbers
			probability = np.random.rand()         #Pull a single random number detachment
			re_prob = 0                            # This parameter is used to determine SV reversals 




# Determine the next Vesicle Position
			next_pos = curr_position + curr_velocity			# Define the next lattice position, based on current velocity

# Check if vesicle is already paused, if yes, then decrement hold vesicle and decrement time
			if memory1 > 0 : 
				curr_position = curr_position
				memory1 = memory1 - 1			

# Now check if when the pause is down the vesicle reverses direction
				if memory1 == 0:
					re_prob = np.random.rand()   #Pull a single random number for re-attachment
					if re_prob < Pr:
						curr_velocity = -curr_velocity	# Initialize SV velocity toward distal regardless of MT

 
#---------------------- Velocity equals 1 ------------------------------#                   
# Check for Synapse at next position (next_pos) for velocity of 1, if not then run vesicle options	
			if velocity == 1:
#				print(velocity)

				if lattice[int(next_pos)][0] < 1 and memory1 == 0: 
					curr_position = next_pos


# Check for Synapse at next position for velocity of 1, if yes and Vesicle is NOT already paused, then run pause probability
				if lattice[int(next_pos)][0] == 1: 
    # Note: we will control for each possibility of direction and pausing
    
					if curr_velocity > 0 and probability < Ant_prob:
						curr_position = next_pos		
						memory1 = int(np.random.exponential(Pause_time_synapse,1) )
					if curr_velocity > 0 and probability >= Ant_prob:
						curr_position = next_pos		
					if curr_velocity < 0 and probability < Ret_prob:
						curr_position = next_pos		
						memory1 = int(np.random.exponential(Pause_time_synapse,1) )
					if curr_velocity < 0 and probability >= Ret_prob:
						curr_position = next_pos		


#---------------------- Velocity GREATER than 1 ------------------------------#
# Check for Synapse at next position (next_pos) for velocity of 1, if not then run vesicle options	
			if lattice[int(next_pos)][0] < 1 and memory1 == 0: 
				curr_position = next_pos


# Check for Synapse at next position for velocity of 1, if yes and Vesicle is NOT already paused, then run pause probability
			if velocity > 1:
#				print(velocity)
				for tmp_chk in range (0,(velocity)): 
					if lattice[int(next_pos + tmp_chk*np.sign(curr_velocity))][0] == 1: 
    # Note: we will control for each possibility of direction and pausing
    
						if curr_velocity > 0 and probability < Ant_prob:
							curr_position = next_pos		
							memory1 = int(np.random.exponential(Pause_time_synapse,1) )
						if curr_velocity > 0 and probability >= Ant_prob:
							curr_position = next_pos		
						if curr_velocity < 0 and probability < Ret_prob:
							curr_position = next_pos		
							memory1 = int(np.random.exponential(Pause_time_synapse,1) )
						if curr_velocity < 0 and probability >= Ret_prob:
							curr_position = next_pos		
			


# Output all results
			if curr_velocity < 0 :
				curr_out.write("%s\t%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (t, x1, y1, curr_position, next_pos, lattice[int(next_pos)][0], memory1, re_prob, curr_velocity,Ret_prob))
			if curr_velocity > 0 :
				curr_out.write("%s\t%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (t, x1, y1, curr_position, next_pos, lattice[int(next_pos)][0], memory1, re_prob, curr_velocity,Ant_prob))
			if curr_velocity == 0 :
				curr_out.write("%s\t%s\t%s\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (t, x1, y1, curr_position, next_pos, lattice[int(next_pos)][0], memory1, re_prob, curr_velocity,Ant_prob))


			Bundle_tmp_t[t] = t
			Bundle_tmp_x[t] = curr_position
			if curr_position < 0 : 
				curr_out.close()
				break

			if t == (Time_STEP-2) :
				curr_out.close()
				break


	return (Bundle_tmp_x, Bundle_tmp_t)

#--------------------------------------------------------------#
#--------------------------------------------------------------#
#--------------------------------------------------------------#

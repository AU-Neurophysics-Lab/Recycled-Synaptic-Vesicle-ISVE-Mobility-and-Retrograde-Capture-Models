# Recycled-Synaptic-Vesicle-ISVE-Mobility-and-Retrograde-Capture-Models
These Models Simulate Experimentally Observed SV ISVE Mobility and Retrograde Presynaptic Capture
Written By: Michael W. Gramlich
Date: 10/2023

This file will outline the workflow to follow in order to generate a bundle of single SV tracks on an axonal lattice and then calculate the flux and density.

General Notes about script implementations:
[A] All python scripts were written with python 3.11. Function calls may have changed from earlier or at later enviroments
[B] Matlab plotting scripts were written in Matlab 2012b. Function calls DEFINATELY have changed from earlier and at later enviroments (i.e. array and cell element function calls change)

Outline:
[1] Download all scripts within the stable build to a single folder

[2] Generate a collection of individual tracks using the script "SV_transport_model_v3_1.py"
* Note: Depending upon the number of tracks and synapses this could result in >gigabytes of data
  - Define the paramaters of the individual SVs to be modeled
  - Define the paramaters of the presynapse locations
  - Define the paramters of the bundle size and simulation time
  - Define the presynapse capture probability of axonal SVs
  - Run the script
  - Data will be output into a set of sub-folders with the name "synapse_XX," where XX is the location of the presynapse (in lattice units)
    
[3] Manually create a new sub-folder that will indicate the parameters modeled in the simulation

[4] Move the generated individual synapse folders into (i.e. ["synapse_30", "synapse_60", ...]) into the sub-folder created above [3] 

[5] Repeat steps [3] and [4] above for a different set of parameters

[6] Open and run "Combined_Bundle_Flux_v2_1.py" script to aggregate results from [2]-[5]
  - Define the rate that new SVs are added to the bundle (in time-steps)
  - Define the number of tracks per presynapse
  - Define the fraction of SVs from each group (designed as a binomial (p, 1-p) choice)
  - Manually input the location of the SV track files
  - Manually input the location of the aggregate flux, SV-density files
    
[7] To visualize the aggregate bundle density with time open the file "subpanel_plot_trackdensity.m" in matlab 
  - Manually input the location of the density file
  - Run script

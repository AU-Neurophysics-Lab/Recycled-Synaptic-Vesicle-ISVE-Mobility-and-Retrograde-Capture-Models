# Recycled-Synaptic-Vesicle-ISVE-Mobility-and-Retrograde-Capture-Models
These Models Simulate Experimentally Observed SV ISVE Mobility and Retrograde Presynaptic Capture
Written By: Michael W. Gramlich
Date: 10/2023

This file will outline the workflow to follow in order to generate a bundle of single SV tracks on an axonal lattice and then calculate the flux and density.

General Notes about script implementations:
[A] All python scripts were written with python 3.11. Function calls may have changed from earlier or at later enviroments
[B] Matlab plotting scripts were written in Matlab 2012b. Function calls DEFINATELY have changed from earlier and at later enviroments (i.e. array and cell element function calls change)

Outline:
[] Download all scripts within the stable build
[] Generate a collection of individual tracks using the script "SV_transport_model_v3_1.py"
* Note: Depending upon the number of tracks and synapses this could result in >gigabytes of data
[] Manually create a new sub-folder that will indicate the parameters modeled in the simulation
[] Move the generated individual synapse folders into (i.e. ["synapse_30", "synapse_60", ...]) into the sub-folder created above [] 
[] Repeat steps [] and [] above for a different set of parameters
[] 

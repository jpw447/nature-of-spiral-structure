import numpy as np
import matplotlib.pyplot as plt
import os

'''
This file loads the data produced via OSU Analysis.py and ArmAnalysis.py
to plot all three wavebands on the same plot.

This code is not written to be run on any computer, and the paths will need
editing.
'''

if "__name__" == "__main__":
    lst = os.listdir("C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure\\Good Images")
    
    # Aspect ratio 21:9 for figure
    width = 13
    height = width*(9/21)
    
    # Goes over each galaxy in the file
    for galaxy in lst:
        null = False
        
        fig, ax = plt.subplots(1, 2, figsize=(width,height))
        plt.subplots_adjust(wspace=0.2, top=0.85)
        
        # Lists to cycle through colours and line styles for visual clarity
        bands = ['b', 'h', 'v']
        colours = ['dodgerblue', 'crimson', 'blueviolet']
        style = ['-', '--', '-.']
        
        # Looping over each waveband
        for i in range(0,2):
            ax[i].set_xlabel("Radius (pixels)", fontsize=18)
            ax[i].set_ylabel("Pitch angle $i$ (°)", fontsize=18)
            j = 0
            
            for colour_band in bands:
                file_name = galaxy+colour_band+colour_band.upper()+"_arm_"+str(i+1)+".txt"
                
                path = "Good Images\\"+galaxy+"\\"+file_name
                
                # In case there's no image and data for a waveband,
                # ignore the waveband for the galaxy.
                try:
                    file = np.loadtxt(path)
                except OSError: 
                    i = 3
                    print("ERROR")
                    ax[0].set_title("NULL PLOT")
                    ax[1].set_title("NULL PLOT")
                    null = True
                    break;
                
                # Grabbing data from read-in file
                radius = file[:, 0]
                pitch_angle = file[:, 1]
                
                ax[i].set_ylim(-90, 90)
                ax[i].plot(radius, pitch_angle, colours[j], linestyle = style[j], label=colour_band.upper()+"-band")
                j += 1
                
        # Saving the plot only if there's a valid image/data for the galaxy
        if null == False:
            plt.savefig("Good Images\\Final Figures - Unnormalised\\"+galaxy+"_unnormalised_plot.png", dpi=300)
        plt.close()
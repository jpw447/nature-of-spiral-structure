import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc

'''
This file is used to produce logarithmic spirals on a polar and Cartesian plot.
This was used to test the pitch angle calculation. The file is in a condition
to be run and will produce the plots.
'''

if __name__ == "__main__":
    # Defining logarithmic spiral
    degrees = 65
    a = 1
    b = 1/np.tan(degrees*np.pi/180)
    N = 1000
    # Logarithmic Spiral
    theta = np.linspace(0, 2*np.pi, N)
    r = a*np.exp(b*theta)
    
    amplitude = 0.01
    noise = amplitude*np.random.rand(N) * np.exp(b*theta)
    
    # Every nth point is picked out for pitch angle calculation
    interval = 10
    
    r_noise = r + noise
    r_filtered = sc.savgol_filter(r,53,3)[::interval]
    # Perfect Circle - just uncomment the following line and comment out line 19
    # r = np.zeros(N) + 0.1
    
    # Plotting logarithmic spiral on polar projection
    fig_polar = plt.figure()
    ax_polar = fig_polar.gca(projection='polar')
    ax_polar.plot(theta,r_noise)
    ax_polar.set_title("Noisy Logarithmic spiral, a="+str(a)+", b="+str(b)+" (Polar)")
    
    # Origin
    centre_x, centre_y = 0,0
    
    # Cartesian plot by converting to Cartesian co-ordinates
    x_vals = r*np.cos(theta) + centre_x
    y_vals = r*np.sin(theta) + centre_y
    
    # Aspect ratio 21:9 for figure
    width = 12
    height = width*(9/21)
    
    # Spiral and pitch angle radius figure
    fig_pa, ax_pa = plt.subplots(1, 2, figsize=(width,height))
    plt.subplots_adjust(wspace=0.2, top=0.85)
    
    # Plotting logarithmic spiral on Cartesian plane
    ax_pa[0].plot(x_vals, y_vals, 'k', linewidth=1)
    ax_pa[0].plot(centre_x, centre_y, 'rx') # Origin marked as red cross
    ax_pa[0].set_xlim(-np.max(r), np.max(r))
    ax_pa[0].set_ylim(-np.max(r), np.max(r))
    ax_pa[0].set_xlabel("$x$", fontsize=16)
    ax_pa[0].set_ylabel("$y$", fontsize=16)
    ax_pa[0].axis('equal')
    
    # Pitch angle calculation
    x_mean = 0.5*(x_vals[1:] + x_vals[:-1])
    y_mean = 0.5*(y_vals[1:] + y_vals[:-1])
    rbar = np.sqrt((x_mean-centre_x)**2 + (y_mean-centre_y)**2)
    
    # Comparing mean value of r to true value
    fig_compare = plt.figure()
    ax_compare = fig_compare.gca()
    ax_compare.plot(r, label="$r$")
    ax_compare.plot(rbar, label="$\overline{r}$")
    ax_compare.set_title("Mean $r$ versus true $r$ values")
    ax_compare.set_xlabel("Index")
    ax_compare.set_ylabel("$r$, $\overline{r}$")
    ax_compare.legend()
    
    # Pitch angle calculation as in the online diary
    x_prime = centre_x + (x_vals[1:] - x_vals[:-1])
    y_prime = centre_y + (y_vals[1:] - y_vals[:-1])
    r1 = np.sqrt((centre_x - x_prime)**2 + (centre_y - y_prime)**2)
    r2 = np.sqrt((centre_x - x_mean)**2 + (centre_y - y_mean)**2)
    r3 = np.sqrt((x_mean - x_prime)**2 + (y_mean - y_prime)**2)
    
    argument = (r1**2 + r2**2 - r3**2)/(2*r1*r2)
    pitch_angle = 90 - np.arccos((r1**2 + r2**2 - r3**2)/(2*r1*r2)) * 180/np.pi
    
    # Theoretically expecting pitch angle
    expected_angle = (np.pi/2 - np.arctan(1/b)) * 180/np.pi
    
    # Final pitch angle plots
    ax_pa[1].plot(rbar, pitch_angle, 'b-', label="Calculated pitch angle")
    ax_pa[1].hlines(expected_angle, 0, np.max(rbar), 'r', label="Expected pitch angle")
    ax_pa[1].set_xlabel("$\overline{r}$", fontsize=16)
    ax_pa[1].set_ylabel("Pitch Angle (°)", fontsize=16)
    ax_pa[1].set_xlim(0,np.max(rbar))
    ax_pa[1].set_ylim(0, 90)
    
    # Saving figure for report
    plt.savefig("C:\\Users\\Joe\\Documents\\Uni\\Year 3\\Nature of Spiral Structure\\Good Images\\log_spiral_result.png", dpi=300)
    
    
    

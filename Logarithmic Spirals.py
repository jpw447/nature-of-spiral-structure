import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sc

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
# Perfect Circle
# r = np.zeros(N) + 0.1

# Origin
centre_x, centre_y = 0,0

# Polar plot
fig_polar = plt.figure()
ax_polar = fig_polar.gca(projection='polar')
ax_polar.plot(theta,r_noise)
ax_polar.set_title("Noisy Logarithmic spiral, a="+str(a)+", b="+str(b)+" (Polar)")

# Origin
centre_x, centre_y = 0,0

# Cartesian plot by converting to Cartesian co-ordinates
x_vals = r*np.cos(theta) + centre_x
y_vals = r*np.sin(theta) + centre_y

fig_cart = plt.figure()
ax_cart = fig_cart.gca()
ax_cart.plot(x_vals, y_vals, 'b')
ax_cart.plot(x_vals[::interval], y_vals[::interval], 'rx', label="Pitch Angle Points")
ax_cart.plot(centre_x, centre_y, 'rx') # Origin marked as red cross
ax_cart.set_xlim(-np.max(r), np.max(r))
ax_cart.set_ylim(-np.max(r), np.max(r))
ax_cart.set_xlabel("$x$")
ax_cart.set_ylabel("$y$")
ax_cart.set_title("Logarithmic spiral, a="+str(a)+", b="+str(b)+" (Cartesian)")
ax_cart.axis('equal')
ax_cart.legend()

# Pitch angle calculation
x_mean = 0.5*(x_vals[1:] + x_vals[:-1])
y_mean = 0.5*(y_vals[1:] + y_vals[:-1])
rbar = np.sqrt((x_mean-centre_x)**2 + (y_mean-centre_y)**2)

# Comparing mean value of r to true value. 
fig_compare = plt.figure()
ax_compare = fig_compare.gca()
ax_compare.plot(r, label="$r$")
ax_compare.plot(rbar, label="$\overline{r}$")
ax_compare.set_title("Mean $r$ versus true $r$ values")
ax_compare.set_xlabel("Index")
ax_compare.set_ylabel("$r$, $\overline{r}$")
ax_compare.legend()

# Pitch angle calculation
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
fig_pa = plt.figure()
ax_pa = fig_pa.gca()
ax_pa.plot(rbar, pitch_angle, label="Calculated pitch angle")
# ax_pa.hlines(expected_angle, 0, np.max(rbar), 'g', label="Expected pitch angle")
ax_pa.set_title("Pitch Angle versus $\overline{r}$")
ax_pa.set_xlabel("$\overline{r}$")
ax_pa.set_ylabel("Pitch Angle")
ax_pa.set_xlim(0,np.max(rbar))
ax_pa.set_ylim(0, 90)
ax_pa.legend()



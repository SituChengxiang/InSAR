import numpy as np
import math
import matplotlib.pyplot as plt

# target location
target_loc = (10000,0,0)

# aircraft start and end locations
aircraft_start = (0,-100,10000)
aircraft_end = (0,+100,10000)

# number of points for discretization
npoints = 200

# some user-defined quantities
meas_error = 0.01   # motion measurement error, in units of meters

# create an ideal flightline
points = np.linspace(aircraft_start, aircraft_end, num=npoints)
x_pts = points[:, 0]
y_pts = points[:, 1]
z_pts = points[:, 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the line
ax.plot(x_pts, y_pts, z_pts, label='flightline', color='blue')
ax.scatter(*aircraft_start, color='green', label='Start')
ax.scatter(*aircraft_end, color='red', label='End')

# subset the points to show every tenth one, to make the plotting look nicer
nsub_pts = 10
nskip = round(npoints/nsub_pts)
x_pts_sub = points[::nskip, 0]
y_pts_sub = points[::nskip, 1]
z_pts_sub = points[::nskip, 2]

ax.scatter(x_pts_sub[1::], y_pts_sub[1::], z_pts_sub[1::],
           marker='o',
           facecolors='none',
           edgecolors='black',
           s=50,   # size of the circles
           label='Markers')

# Labels and legend
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
ax.legend()

plt.show()

# calculate the distance to the target for each point along the flightline

R = np.linalg.norm(points - target_loc, axis=1)

# Plot the Range to Target as it changes along the flightline

plt.plot(y_pts, (R/1000.0), color='blue')
plt.xlabel('y position')
plt.ylabel('R (km)')
plt.title('Range to Target')
plt.grid(True)
plt.show()

# calculate the frequency, the wavelenght, the wavenumber and convert it into a phase

freq = 13.6e9
c = 3e8
lam = c/freq
wavenum = 2*np.pi/lam
phase = 2*wavenum*R

# calculate the effect of phase wrapping (i.e. we can't observe absolute phase)
phase_wrapped = phase % (2*np.pi)

# Plot the wrapped phase

plt.plot(y_pts, phase_wrapped, '.-', color='blue')
plt.xlabel('y position (m)')
plt.ylabel('phase (radians)')
plt.title('wrapped phase')
plt.grid(True)
plt.show()

# add the effect of motion errors to the flightline

gaussian_noise = np.random.normal(loc=0, scale=meas_error, size=npoints)
x_pts_error = x_pts + gaussian_noise
points_error = np.stack((x_pts_error, y_pts, z_pts), axis=1)
R_error = np.linalg.norm(points_error - target_loc, axis=1)
phase_error = 2*wavenum*R_error

# calculate the effect of phase wrapping (i.e. we can't observe absolute phase)
phase_error_wrapped = phase_error % (2*np.pi)

plt.plot(y_pts, phase, '-', color='black')
plt.plot(y_pts, phase_error, '.', color='blue')
plt.xlabel('y position (m)')
plt.ylabel('phase (radians)')
plt.title('unwrapped phase vs. position')
plt.grid(True)
plt.show()

plt.plot(y_pts, phase_wrapped, '-', color='black')
plt.plot(y_pts, phase_error_wrapped, '.', color='blue')
plt.xlabel('y position (m)')
plt.ylabel('phase (radians)')
plt.title('wrapped phase vs. position')
plt.grid(True)
plt.show()

# Convert to an exponential form, and correct the observed return for the estimated target path

ant_gain = 1.0
estimated_signal = ant_gain * np.exp(1.0j * phase)
actual_signal = ant_gain * np.exp(1.0j * phase_error)

perfect_signal = actual_signal
perfect_correction = actual_signal * np.conj(perfect_signal)    # we don't actu
imperfect_correction = actual_signal * np.conj(estimated_signal)
magnitude_perfect = abs(sum(perfect_correction)/len(perfect_correction))
magnitude_imperfect = abs(sum(imperfect_correction)/len(imperfect_correction))
print(f"Radar cross-section for {meas_error: 6.4f} m of motion error, wavelenghth = {lam: 5.3f} m")
print(f"  Perfect Correction: {np.log10(magnitude_perfect):5.2f} dB")
print(f"Imperfect Correction: {np.log10(magnitude_imperfect):5.2f} dB")
import numpy as np
import math
import matplotlib.pyplot as plt

# target location 目标坐标
target_loc = (10000,0,0)

# aircraft start and end locations 航空器出发点和终点
aircraft_start = (0,-100,10000)
aircraft_end = (0,+100,10000)

# number of points for discretization 离散化点的数量
npoints = 200

# some user-defined quantities 用户定义的量
meas_error = 0.01   # motion measurement error, in units of meters

# create an ideal flightline 创建一条理想航迹
points = np.linspace(aircraft_start, aircraft_end, num=npoints)
x_pts = points[:, 0]
y_pts = points[:, 1]
z_pts = points[:, 2]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the line 绘制航迹
ax.plot(x_pts, y_pts, z_pts, label='flightline', color='blue')
ax.scatter(*aircraft_start, color='green', label='Start')
ax.scatter(*aircraft_end, color='red', label='End')

# subset the points to show every tenth one, to make the plotting look nicer 让图看起来更好看一点
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

# calculate the frequency, the wavelenght, the wavenumber and convert it into a phase 计算频率和波长、波数，并转为向量

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
perfect_correction = actual_signal * np.conj(perfect_signal)    # we don't actua
imperfect_correction = actual_signal * np.conj(estimated_signal)
magnitude_perfect = abs(sum(perfect_correction)/len(perfect_correction))
magnitude_imperfect = abs(sum(imperfect_correction)/len(imperfect_correction))
print(f"Radar cross-section for {meas_error: 6.4f} m of motion error, wavelenghth = {lam: 5.3f} m")
print(f"  Perfect Correction: {np.log10(magnitude_perfect):5.2f} dB")
print(f"Imperfect Correction: {np.log10(magnitude_imperfect):5.2f} dB")

# 1.1
# I'm not sure weather we need static motion error or not, so I will just use the same as in the previous example
# Define the error range in wavelengths
error_wls = np.arange(0.00, 2.01, 0.01)

# 2. placeholder for storing imperfect correction dB values
imperfect_dBs = []

# 3. suppose a constant antenna gain
ant_gain_constant = 1.0
estimated_signal = ant_gain_constant * np.exp(1.0j * phase)

# 4. Cycle for each error level
for err_wl in error_wls:
    # 4.1 convert the error from wavelengths to meters
    meas_error_m = err_wl * lam

    # 4.2 Superimpose Gaussian noise in the x direction
    gn = np.random.normal(loc=0.0, scale=meas_error_m, size=npoints)
    pts_err = np.stack((x_pts + gn, y_pts, z_pts), axis=1)

    # 4.3 Recalculate the distance, phase, and echo with error included
    R_err       = np.linalg.norm(pts_err - target_loc, axis=1)
    phase_err   = 2 * wavenum * R_err
    actual_sig  = ant_gain_constant * np.exp(1.0j * phase_err)

    # 4.4 "imperfect correction"：actual * conj(estimated)
    imp_corr = actual_sig * np.conj(estimated_signal)
    mag_imp  = np.abs(imp_corr.sum() / len(imp_corr))

    # 4.5 Convert to dB storage
    imperfect_dBs.append(10 * np.log10(mag_imp))

# 5. plot error (in wavelengths) vs. imperfect correction (in dB)
plt.figure(figsize=(8,5))
plt.plot(error_wls, imperfect_dBs, lw=2, color='C3')
plt.xlabel('Motion Error (Standard Deviation in wavelengths)(m)')
plt.ylabel('Imperfect Correction RCS (dB)')
plt.title('1.1 Impact of Motion Error on Radar Cross Section')
plt.grid(True)
plt.tight_layout()
plt.show()

# 1.2
ant_width = 1.0  # in units of meters
ant_angle = np.arctan2(y_pts,R)
ant_gain = np.sinc(ant_width/lam * ant_angle)   # the factor, ant_width/lam is an approximation for the gain pattern 

plt.plot(y_pts,40*np.log10(ant_gain));    # the factor of 40 accounts for both the transmit and receive antenna gains (i.e. 2*20log10())
plt.xlabel('y position (m)')
plt.ylabel('gain (dB)')
plt.title('Model for round trip antenna gain')
plt.grid(True)
plt.show()

meas_error = 0.05 * lam
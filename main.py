import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the differential equation for a simple pendulum
def pendulum(y, t, g, l):
    theta, omega = y
    dydt = [omega, -g/l * np.sin(theta)]
    return dydt

# Set initial conditions and parameters
y0 = [np.pi/4, 0]  # Initial angle, initial angular velocity
g = 9.81  # Gravity
l = 1  # Pendulum length
t = np.linspace(0, 10, 100)  # Time points

# Solve the differential equation
sol = odeint(pendulum, y0, t, args=(g, l))

# Plot the results
plt.plot(t, sol[:, 0], label='Angle')
plt.plot(t, sol[:, 1], label='Angular Velocity')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Angle / Angular Velocity')
plt.title('Simple Pendulum Simulation')
plt.show()
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Data provided in the previous turn
T = np.array([35, 45, 55, 65, 75, 85])  # Temperature (C)
E = np.array([0.7524, 1.1281, 1.5045, 1.8802, 2.2566, 2.6325])  # EMF (mV)

# Linear Regression Calculation
slope, intercept, r_value, p_value, std_err = linregress(T, E)

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(T, E, color='black', label='Experimental Data', zorder=5)

# Plot the fitted line
fit_line = slope * T + intercept
plt.plot(T, fit_line, color='red', linestyle='--', label=f'Fitted Line\nE = {slope:.4f}T {intercept:.4f}')

# Formatting graph
plt.title('Relationship between Temperature (T) and Thermal EMF (E)', fontsize=14)
plt.xlabel('Temperature, T ($^\circ$C)', fontsize=12)
plt.ylabel('Thermal EMF, $E_x$ (mV)', fontsize=12)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(fontsize=11)

# Display equation on the graph
text_str = f'$E = {slope:.4f} T - {abs(intercept):.4f}$ mV\n$R^2 = {r_value**2:.4f}$'
plt.text(36, 2.3, text_str, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

# Show plot
plt.tight_layout()
plt.show()


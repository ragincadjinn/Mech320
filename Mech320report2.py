
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

control = pd.read_csv("EL_Control_S1_09282026_151034.csv")
thin = pd.read_csv("EL_thin_S2_09282026_151340.csv")
cr2 = pd.read_csv("EL_CR-2_S3_09282026_152210.csv")
cr1 = pd.read_csv("EL_CR-1_S4_09282026_152352.csv")

# cross sections
A_control = 12.20 * 4.91 / 25.4**2
A_thin = 12.10 * 4.21 / 25.4**2
A_cr2 = 12.15 * 4.91 / 25.4**2
A_cr1 = 12.17 * 4.91 / 25.4**2

#dist between grips in (inches)
D_control = 113.87 / 25.4
D_thin = 113.88 / 25.4
D_cr2 = 113.86 / 25.4
D_cr1 = 113.86 / 25.4

# stress = load / area
stress_control = control["S:Load (lbs)"] / A_control
stress_thin = thin["S:Load (lbs)"] / A_thin
stress_cr2 = cr2["S:Load (lbs)"] / A_cr2
stress_cr1 = cr1["S:Load (lbs)"] / A_cr1

#strain--change in length / D
strain_control = control["S:Position (in)"] / D_control
strain_thin = thin["S:Position (in)"] / D_thin
strain_cr2 = cr2["S:Position (in)"] / D_cr2
strain_cr1 = cr1["S:Position (in)"] / D_cr1

#Yungs modulus for the control= (strain 0.002 to 0.010)
x = strain_control[(strain_control >= 0.002) & (strain_control <= 0.010)]
y = stress_control[(strain_control >= 0.002) & (strain_control <= 0.010)]
E, b = np.polyfit(x, y, 1)
 print("Control modulus E =", round(E / 1000, 2), "ksi")
print("Control UTS =", round(stress_control.max(), 2), "psi")

#.2% offset 
offset_strain = np.linspace(0.002, 0.026, 50)
offset_stress = E * (offset_strain - 0.002)

#---------------
plt.plot(strain_control, stress_control, label="S1 Control")
plt.plot(strain_thin, stress_thin, label="S2 Thin")
plt.plot(strain_cr2, stress_cr2, label="S3 CR-2")
plt.plot(strain_cr1, stress_cr1, label="S4 CR-1")
plt.plot(offset_strain, offset_stress, "--", label="0.2% offset")

plt.xlabel("Strain (in/in)")
plt.ylabel("Stress (psi)")
plt.title("Stress vs Strain")
plt.xlim(0, 0.07)
plt.ylim(0, 4500)
plt.legend
plt.grid()
plt.savefig("Figure_1_stress_strain.png", dpi=200)
plt.show()

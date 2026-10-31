#c00054452 & c0053899

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) #files in same folder

L = 3.50    # span
w = 0.500   # width
t = 0.185   # thick 

files = {"Al 6063": "EJD_RVH_6063_1_10262026_162802.csv",
         "Al 2024": "EJD_RVH_2024_1_10262026_163157.csv"}

for name in files:
    #sign swaps to plot
    data = pd.read_csv(files[name])
    load = -data["S:Load (lbs)"]          
    position = -data["S:Position (in)"]  

    #slope
    P_max = load.max()
    elastic = (load > 0.10 * P_max) & (load < 0.35 * P_max) & (data.index < load.idxmax())
    m, b = np.polyfit(position[elastic], load[elastic], 1)

    #too much slack
    deflection = position + b / m

    #Eqs. 1 and 2
    stress = 3 * load * L / (2 * w * t**2)
    strain = 6 * deflection * t / L**2

    #Eq. 3
    E_B = L**3 * m / (4 * w * t**3)

    # Proof strength
    offset_line = E_B * (strain - 0.002)
    for i in range(len(stress)):
        if strain[i] > 0.002 and stress[i] < offset_line[i]:
            #interpolating bc of time intervals
            gap_before = stress[i-1] - offset_line[i-1]
            gap_after = offset_line[i] - stress[i]
            fraction = gap_before / (gap_before + gap_after)
            sigma_p = stress[i-1] + fraction * (stress[i] - stress[i-1])
            eps_p = strain[i-1] + fraction * (strain[i] - strain[i-1])
            break

    #Eq. 5
    sigma_M = stress.max()
    eps_M = strain[stress.idxmax()]

    #Eq. 6
    u_r = sigma_p**2 / (2 * E_B)

    print(name, "E_B =", round(E_B), "psi, sigma_p =", round(sigma_p), "psi, sigma_M =", round(sigma_M), "psi")

    # Figure 1: load vs deflection
    plt.figure(1)
    curve1, = plt.plot(deflection, load, label=name)
    plt.plot(deflection[load.idxmax()], P_max, "o", color=curve1.get_color())   # peak load

    # Figure 2: stress vs strain
    plt.figure(2)
    curve2, = plt.plot(strain, stress / 1000, label=name)
    color = curve2.get_color()                         # same color for this alloy

    e = np.linspace(0.002, eps_p * 1.3, 20)            # strain values for the offset line
    plt.plot(e, E_B * (e - 0.002) / 1000, "--", color=color, label=name + " 0.2% offset")

    plt.plot(eps_p, sigma_p / 1000, "s", color=color)  # square = proof strength
    plt.plot(eps_M, sigma_M / 1000, "o", color=color)  # circle = max flexural stress

plt.figure(1)
plt.xlabel("Midspan deflection (in)")
plt.ylabel("Load (lbf)")
plt.xlim(0, 1.1)
plt.ylim(0, 400)
plt.grid(True)
plt.legend()
plt.savefig("figure1.png", dpi=200)

plt.figure(2)
plt.xlabel("Flexural strain (in/in)")
plt.ylabel("Flexural stress (ksi)")
plt.xlim(0, 0.10)
plt.ylim(0, 120)
plt.grid(True)
plt.legend()
plt.savefig("figure2.png", dpi=200)

plt.show()

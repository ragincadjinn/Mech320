import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Specimen dimensions (inches)
L = 3.50    # support span
w = 0.500   # width
t = 0.185   # thickness

files = {"Al 6063": "EJD_RVH_6063_1_10262026_162802.csv",
         "Al 2024": "EJD_RVH_2024_1_10262026_163157.csv"}

for name in files:
    # 1. Read the data file
    data = pd.read_csv(files[name])
    load = -data["S:Load (lbs)"]          # make load positive
    position = -data["S:Position (in)"]   # make deflection positive

    # 2. Find the slope (m) of the straight-line part of the curve
    #    (between 10% and 35% of the highest load)
    P_max = load.max()
    elastic = (load > 0.10 * P_max) & (load < 0.35 * P_max) & (data.index < load.idxmax())
    m, b = np.polyfit(position[elastic], load[elastic], 1)

    # 3. Remove the slack at the start of the test
    deflection = position + b / m

    # 4. Flexural stress and strain, Eqs. 1 and 2
    stress = 3 * load * L / (2 * w * t**2)
    strain = 6 * deflection * t / L**2

    # 5. Bending modulus, Eq. 3
    E_B = L**3 * m / (4 * w * t**3)

    # 6. Proof strength: first point where the curve falls below the 0.2% offset line (Eq. 4)
    offset_line = E_B * (strain - 0.002)
    for i in range(len(stress)):
        if strain[i] > 0.002 and stress[i] < offset_line[i]:
            # the crossing is between point i-1 and point i, so interpolate
            gap_before = stress[i-1] - offset_line[i-1]
            gap_after = offset_line[i] - stress[i]
            fraction = gap_before / (gap_before + gap_after)
            sigma_p = stress[i-1] + fraction * (stress[i] - stress[i-1])
            eps_p = strain[i-1] + fraction * (strain[i] - strain[i-1])
            break

    # 7. Maximum flexural stress and its strain, Eq. 5
    sigma_M = stress.max()
    eps_M = strain[stress.idxmax()]

    # 8. Modulus of resilience, Eq. 6
    u_r = sigma_p**2 / (2 * E_B)

    print(name, "E_B =", round(E_B), "psi, sigma_p =", round(sigma_p), "psi, sigma_M =", round(sigma_M), "psi")

    # 9. Plot stress vs. strain
    plt.plot(strain, stress / 1000, label=name)

plt.xlabel("Flexural strain (in/in)")
plt.ylabel("Flexural stress (ksi)")
plt.legend()
plt.show()

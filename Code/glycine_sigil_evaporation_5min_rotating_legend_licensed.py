# Copyright (c) 2025 M M abdAlhamid
# 
# This file is part of the glycine vibrational sonification and sigil project.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
Zwitterionic glycine – vibrational sigil animation (5 min, rotating, with legend & enhanced visuals)

Scientific mapping:
    * Radius r ∝ wavenumber (cm^-1)
    * Quadrants encode functional groups:
        A (NH3+/CH2 stretches)   → Quadrant I
        B (COO-/backbone)        → Quadrant II
        C (skeletal / low modes) → Quadrant III
    * Marker size ∝ normalized intensity
    * Group envelopes A/B/C control opacity over normalized time u = t/T_total.

Visual additions (for video use):
    * Dark background for contrast.
    * Color-coded groups with legend (bottom center).
    * Text labels on quadrants and rings.
    * Slow global rotation (1 full turn over 5 minutes).
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

# ------------------------------
# 1. Glycine vibrational data
# ------------------------------
peaks = [
    (3330, 0.55), (3200, 0.60), (3020, 0.25), (2940, 0.30),
    (1650, 1.00), (1498, 0.75), (1410, 0.90), (1330, 0.40),
    (1232, 0.40), (1209, 0.30), (1040, 0.80), (929, 0.30),
    (889, 0.30), (616, 0.50), (513, 0.40),
]

# Normalize intensities
I_sum = sum(p[1] for p in peaks)
peaks = [(cm, i / I_sum) for cm, i in peaks]

cm_arr    = np.array([cm for cm, _ in peaks])
intensity = np.array([i for _, i in peaks])

cm_min, cm_max = cm_arr.min(), cm_arr.max()

# ------------------------------
# 2. Functional groups & polar geometry
# ------------------------------
def classify_group(cm):
    if cm >= 2900:
        return "A"  # NH3+/CH2 (outer)
    elif cm >= 1200:
        return "B"  # COO-/backbone (middle)
    else:
        return "C"  # skeletal / low (inner)

groups = np.array([classify_group(cm) for cm in cm_arr])

r_min, r_max = 0.30, 1.00
r_base = r_min + (r_max - r_min) * (cm_arr - cm_min) / (cm_max - cm_min)

quad_centers = {
    "A": np.deg2rad(45),   # Quadrant I
    "B": np.deg2rad(135),  # Quadrant II
    "C": np.deg2rad(225),  # Quadrant III
}

theta_base = np.zeros_like(r_base, dtype=float)
for g in ["A", "B", "C"]:
    idx = np.where(groups == g)[0]
    n = len(idx)
    if n == 0:
        continue
    spread = np.deg2rad(30)
    offsets = np.linspace(-spread / 2, spread / 2, n)
    theta_base[idx] = quad_centers[g] + offsets

s_min, s_max = 80, 400
sizes = s_min + (s_max - s_min) * (intensity / intensity.max())

# ------------------------------
# 3. Time axis & envelopes (5 min)
# ------------------------------
T_total = 300.0   # seconds (5 minutes)
fps = 8           # 8 fps keeps file size reasonable
n_frames = int(T_total * fps)
t = np.linspace(0.0, T_total, n_frames)
u = t / T_total   # normalized time in [0, 1]

def envelope_A(u):
    """NH3+/CH2 group: strong at start, fades by u≈0.4."""
    return np.clip(1.0 - u / 0.4, 0.0, 1.0)

def envelope_B(u):
    """COO-/backbone group: peaks around u≈0.5."""
    return np.exp(-((u - 0.5) ** 2) / (2 * 0.15 ** 2))

def envelope_C(u):
    """Skeletal group: rises after u≈0.2, persists toward the end."""
    rise = np.clip((u - 0.2) / 0.4, 0.0, 1.0)    # grows 0.2→0.6
    fall = np.clip((1.0 - u) / 0.4, 0.0, 1.0)    # fades 0.6→1.0
    return np.minimum(rise, fall)

env_A = envelope_A(u)
env_B = envelope_B(u)
env_C = envelope_C(u)

alpha_max = 0.95
alpha = np.zeros((n_frames, len(peaks)))
for fi in range(n_frames):
    for i, g in enumerate(groups):
        if g == "A":
            alpha[fi, i] = alpha_max * env_A[fi]
        elif g == "B":
            alpha[fi, i] = alpha_max * env_B[fi]
        else:
            alpha[fi, i] = alpha_max * env_C[fi]

# ------------------------------
# 4. Rotation parameters
# ------------------------------
ROTATE = True          # set False for no rotation
N_ROTATIONS = 1.0      # number of full turns over the full 5 minutes
omega = 2.0 * np.pi * N_ROTATIONS / T_total if ROTATE else 0.0

# ------------------------------
# 5. Plot & animation
# ------------------------------
# Colors for groups
col_A = [1.0, 0.6, 0.6, 1.0]  # NH3+/CH2
col_B = [0.6, 0.9, 1.0, 1.0]  # COO-/backbone
col_C = [0.8, 0.8, 0.8, 1.0]  # skeletal

fig = plt.figure(figsize=(6, 6), facecolor="black")
ax = fig.add_subplot(111, polar=True, facecolor="black")
ax.set_theta_zero_location("E")
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])

# Guide rings
for rr, label in zip(
    [r_min, (r_min + r_max) / 2, r_max],
    ["Skeletal / low ν", "COO-/backbone", "NH3+/CH2 stretches"],
):
    ax.plot(
        np.linspace(0, 2 * np.pi, 300),
        np.full(300, rr),
        linewidth=0.4,
        alpha=0.25,
        color="white",
    )
    # place label at -90° (downwards)
    ax.text(
        np.deg2rad(-90),
        rr,
        label,
        color="white",
        fontsize=8,
        ha="center",
        va="center",
        alpha=0.7,
    )

# Base colors assigned per point
base_colors = []
for g in groups:
    if g == "A":
        base_colors.append(col_A)
    elif g == "B":
        base_colors.append(col_B)
    else:
        base_colors.append(col_C)
base_colors = np.array(base_colors)

# Initial geometry
theta0 = theta_base + omega * t[0]
r0 = r_base
offsets0 = np.vstack([theta0, r0]).T

scatter = ax.scatter(
    theta0,
    r0,
    s=sizes,
    facecolors=base_colors,
    edgecolors="none",
)

# Quadrant labels near outer radius
ax.text(
    quad_centers["A"],
    r_max * 1.07,
    "NH$_3^+$/CH$_2$",
    color=col_A,
    fontsize=10,
    ha="center",
    va="center",
)
ax.text(
    quad_centers["B"],
    r_max * 1.07,
    "COO$^-$/backbone",
    color=col_B,
    fontsize=10,
    ha="center",
    va="center",
)
ax.text(
    quad_centers["C"],
    r_max * 1.07,
    "Skeletal modes",
    color=col_C,
    fontsize=10,
    ha="center",
    va="center",
)

# Title (slightly smaller to leave room below for legend)
ax.set_title(
    "Zwitterionic Glycine – Vibrational Sigil Evaporation",
    va="bottom",
    color="white",
    fontsize=11,
    pad=20,
)

# Legend at bottom center
legend_elements = [
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="None",
        markersize=8,
        markerfacecolor=col_A,
        markeredgecolor="none",
        label="NH$_3^+$/CH$_2$ stretches",
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="None",
        markersize=8,
        markerfacecolor=col_B,
        markeredgecolor="none",
        label="COO$^-$/backbone modes",
    ),
    Line2D(
        [0],
        [0],
        marker="o",
        linestyle="None",
        markersize=8,
        markerfacecolor=col_C,
        markeredgecolor="none",
        label="Skeletal / low-frequency modes",
    ),
]

leg = ax.legend(
    handles=legend_elements,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.22),
    frameon=False,
    fontsize=8,
)
for text in leg.get_texts():
    text.set_color("white")

plt.tight_layout()

def update(frame):
    # Geometry with rotation
    theta_t = theta_base + omega * t[frame]
    r_t = r_base
    offsets = np.vstack([theta_t, r_t]).T
    scatter.set_offsets(offsets)

    # Update opacity
    colors = base_colors.copy()
    colors[:, 3] = alpha[frame]
    scatter.set_facecolors(colors)

    return scatter,

anim = FuncAnimation(fig, update, frames=n_frames, interval=1000.0 / fps, blit=True)

def main(output="glycine_sigil_evaporation_5min_rotating_legend.mp4"):
    anim.save(output, fps=fps, dpi=150, codec="libx264")
    plt.close(fig)
    print(f"Wrote {output}")

if __name__ == "__main__":
    main()

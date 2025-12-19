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
Zwitterionic glycine – pharmacokinetic sigil animation (5 min, rotating)

This script generates a 5-minute MP4 animation of a concentric
"sigil" for zwitterionic glycine linked to the pharmacokinetic (PK)
audio model.

Key design points:

    * Radius r ∝ wavenumber (cm^-1).
    * All vibrational modes are treated identically with respect to PK:
      a single global PK envelope is applied; no explicit chemical
      group categories are used and no legend is drawn.
    * Marker size ∝ normalized intensity.
    * Global opacity over time follows a pharmacokinetic envelope
      E_PK(t_phys) compressed from a 0–4 h physiological window
      into a 5-minute (300 s) animation.
    * The whole pattern makes one full rotation over the 5 minutes.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# ------------------------------
# 1. Vibrational data
# ------------------------------
# Same zwitterionic glycine modes as used in the audio scripts:
# (wavenumber in cm^-1, relative intensity in arbitrary units)
peaks = [
    (3330, 0.55),
    (3200, 0.60),
    (3020, 0.25),
    (2940, 0.30),
    (1650, 1.00),
    (1498, 0.75),
    (1410, 0.90),
    (1330, 0.40),
    (1232, 0.40),
    (1209, 0.30),
    (1040, 0.80),
    (929,  0.30),
    (889,  0.30),
    (616,  0.50),
    (513,  0.40),
]

# Normalize intensities so their sum is 1 (clean scaling)
I_sum = sum(i for _, i in peaks)
peaks = [(cm, i / I_sum) for cm, i in peaks]

cm_arr = np.array([cm for cm, _ in peaks], dtype=float)
intensity = np.array([i for _, i in peaks], dtype=float)

nu_min = cm_arr.min()
nu_max = cm_arr.max()

# ------------------------------
# 2. Geometry (no explicit chemical groups)
# ------------------------------
# Radius mapping: inner/outer bounds of ring field
r_min = 0.25
r_max = 0.95

radii = r_min + (r_max - r_min) * (cm_arr - nu_min) / (nu_max - nu_min)

# Base polar angles: distribute modes approximately evenly around circle
# with a small random jitter to avoid perfect symmetry.
rng = np.random.default_rng(42)
base_angles = np.linspace(0.0, 2.0 * np.pi, len(peaks), endpoint=False)
jitter = rng.uniform(-np.pi / 24.0, np.pi / 24.0, size=len(peaks))
theta0 = base_angles + jitter

# Marker sizes: simple function of intensity
size_min = 40.0
size_max = 200.0
sizes = size_min + (size_max - size_min) * intensity

# ------------------------------
# 3. Pharmacokinetic envelope (0–4 h → 5 min)
# ------------------------------
T_total = 5.0 * 60.0        # 5 minutes in seconds
fps = 30
n_frames = int(T_total * fps)

t_audio = np.linspace(0.0, T_total, n_frames)

# Map audio time (0–300 s) to physiological time (0–4 h)
T_phys_window = 4.0 * 3600.0     # 0–4 h in seconds
t_phys = (t_audio / T_total) * T_phys_window

# Simple absorption–elimination model C(t) ∝ e^{-k_e t} - e^{-k_a t}
# Use elimination half-life ~40 min, absorption slightly faster
t_half = 40.0 * 60.0              # 40 minutes in seconds
k_e = np.log(2.0) / t_half
k_a = 1.5 * k_e                   # absorption a bit faster than elimination

C = np.exp(-k_e * t_phys) - np.exp(-k_a * t_phys)
C[C < 0.0] = 0.0                  # negative tail → zero
if C.max() > 0:
    E_PK = C / C.max()            # normalize to [0, 1]
else:
    E_PK = C

# Global opacity envelope, with per-mode intensity weighting
alpha_min = 0.10
alpha_max = 1.00

# Shape: (n_frames, n_modes)
alpha_global = alpha_min + (alpha_max - alpha_min) * E_PK
alpha_frames = alpha_global[:, None] * (0.5 + 0.5 * intensity[None, :])
alpha_frames = np.clip(alpha_frames, 0.0, 1.0)

# ------------------------------
# 4. Rotation parameters
# ------------------------------
ROTATE = True
N_ROTATIONS = 1.0                    # 1 full turn over 5 minutes
omega = 2.0 * np.pi * N_ROTATIONS / T_total if ROTATE else 0.0

# ------------------------------
# 5. Figure & initial scatter
# ------------------------------
fig = plt.figure(figsize=(6, 6), facecolor="black")
ax = fig.add_subplot(111, polar=True, facecolor="black")

ax.set_theta_zero_location("E")
ax.set_theta_direction(-1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylim(0.0, 1.0)

# Base RGBA color: single neutral color for all markers
base_color = np.array([0.8, 0.9, 1.0, 1.0])  # pale cyan/white
base_colors = np.tile(base_color, (len(peaks), 1))

# Initial positions at t=0
theta_init = theta0.copy()
scatter = ax.scatter(theta_init, radii, s=sizes, c=base_colors, linewidths=0.0)

# ------------------------------
# 6. Animation update
# ------------------------------
def update(frame):
    """Update function for FuncAnimation."""
    t = t_audio[frame]
    theta = theta0 + omega * t

    # Update marker positions
    offsets = np.column_stack([theta, radii])
    scatter.set_offsets(offsets)

    # Update alpha channel from PK envelope
    colors = scatter.get_facecolors()
    colors[:, 3] = alpha_frames[frame]
    scatter.set_facecolors(colors)

    return scatter,

anim = FuncAnimation(
    fig,
    update,
    frames=n_frames,
    interval=1000.0 / fps,
    blit=True,
)

# ------------------------------
# 7. Entry point
# ------------------------------
def main(output="glycine_sigil_pk_5min_rotating.mp4"):
    writer = FFMpegWriter(fps=fps, bitrate=4000)
    anim.save(output, writer=writer, dpi=150)
    plt.close(fig)
    print(f"Wrote {output}")

if __name__ == "__main__":
    main()

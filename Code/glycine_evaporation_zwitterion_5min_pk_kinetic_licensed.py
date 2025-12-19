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
Glycine evaporation – zwitterionic form (conservative PK-based kinetic model)

This script generates a 5-minute stereo WAV file in which the amplitude
of all vibrational modes follows a shared, pharmacokinetically-inspired
timecourse (oral-like absorption + elimination), compressed into 5 minutes.

Design principles:
  - Frequencies come directly from zwitterionic glycine IR/Raman peaks,
    using the same linear mapping as the original evaporation script
    (1600 cm^-1 -> 300 Hz).
  - A *single* global envelope E_pk(t) is used for all modes to avoid
    claiming group-specific kinetics that are not empirically measured.
  - E_pk(t) is constructed as a classic 1-compartment oral PK curve:
        C(t) ∝ e^{-k_e t} - e^{-k_a t}
    with k_e derived from a published elimination half-life (~41 min) for
    an intravenous glycine load, and k_a chosen to give a physiological
    t_max on the order of ~1 h. The entire 0–4 h window is then mapped
    onto 300 s of audio time by a constant compression factor.
  - No jitter, dephasing or solvent noise is included: this is a strict,
    conservative kinetic prototype.

Output: glycine_evaporation_zwitterion_5min_pk_kinetic.wav
"""

import numpy as np
import wave
import math

# ---------------- core parameters ----------------
sr = 22050              # sample rate (Hz), as in the original script
T_audio = 5 * 60        # total duration in seconds (5 min)
t_audio = np.arange(int(sr * T_audio)) / sr

# Speed of light in cm/s (for consistency with original mapping)
c = 2.99792458e10

# Linear mapping: 1600 cm^-1 -> 300 Hz, identical to original version
K = (1600.0 * c) / 300.0

# ---------------- vibrational modes ----------------
# Zwitterionic glycine modes: (wavenumber in cm^-1, relative intensity)
peaks = [
    (3330, 0.55), (3200, 0.60), (3020, 0.25), (2940, 0.30),
    (1650, 1.00), (1498, 0.75), (1410, 0.90), (1330, 0.40),
    (1232, 0.40), (1209, 0.30), (1040, 0.80), (929, 0.30),
    (889, 0.30), (616, 0.50), (513, 0.40),
]

# Normalize intensities so that sum of relative intensities = 1
I_sum = sum(i for _, i in peaks)
peaks = [(cm, i / I_sum) for cm, i in peaks]

# ---------------- PK-based global envelope ----------------
# We consider a 0–4 h physiological window and compress it into 300 s.
T_phys = 4.0 * 60.0 * 60.0      # 4 h in seconds
compression = T_phys / T_audio  # mapping factor t_phys = t_audio * compression

# Elimination half-life from IV glycine load (elderly TURP patients): ~41 min.
# k_e is the elimination rate constant.
t_half_elim = 41.0 * 60.0                     # seconds
k_e = math.log(2.0) / t_half_elim             # 1/s

# Choose an absorption rate constant k_a slightly faster than k_e so that
# t_max ≈ 1 h in physiological time for the oral-like profile.
# For a 1-compartment oral model C(t) ∝ e^{-k_e t} - e^{-k_a t},
# t_max = ln(k_a / k_e) / (k_a - k_e).  Here we choose k_a = 1.2 * k_e.
k_a = 1.2 * k_e

# Compute the unnormalized PK envelope in physiological time
t_phys = t_audio * compression  # seconds in the 0–4 h window
E_pk = np.exp(-k_e * t_phys) - np.exp(-k_a * t_phys)

# Ensure no negative values (due to numerical noise very close to t=0)
E_pk = np.maximum(E_pk, 0.0)

# Normalize envelope to have a maximum of 1.0
max_pk = np.max(E_pk) if np.max(E_pk) > 1e-12 else 1.0
E_pk /= max_pk

# Short technical fade-in/out to avoid digital clicks (no biological meaning)
fi = int(0.05 * sr)  # 50 ms fade-in
fo = int(0.05 * sr)  # 50 ms fade-out
tech_fade = np.ones_like(t_audio)
tech_fade[:fi] = np.linspace(0.0, 1.0, fi)
tech_fade[-fo:] = np.linspace(1.0, 0.0, fo)

E = E_pk * tech_fade

# ---------------- synthesis ----------------
L = np.zeros_like(t_audio)
R = np.zeros_like(t_audio)

for cm, rel_int in peaks:
    # Audio frequency derived directly from wavenumber
    f = (c * cm) / K  # Hz

    phase = 2.0 * np.pi * f * t_audio
    sig = np.sin(phase)

    L += sig * E * rel_int
    R += sig * E * rel_int

# ---------------- normalization and export ----------------
peak = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = np.clip(0.85 * L / peak, -1.0, 1.0)
R = np.clip(0.85 * R / peak, -1.0, 1.0)

stereo = np.int16(np.vstack([L, R]).T * 32767)

out_name = "glycine_evaporation_zwitterion_5min_pk_kinetic.wav"
with wave.open(out_name, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)   # 16-bit PCM
    wf.setframerate(sr)
    wf.writeframes(stereo.tobytes())

print("Wrote:", out_name)

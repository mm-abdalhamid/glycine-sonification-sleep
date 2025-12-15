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

import numpy as np
import wave

# Glycine evaporation – zwitterionic form
# Sharp NH3+/CH2 edges → COO- identity → skeletal memory → bath

# --------- parameters ----------
sr = 22050          # sample rate (Hz)
T  = 5 * 60         # total duration (seconds)
t  = np.arange(int(sr*T)) / sr
c  = 2.99792458e10  # speed of light in cm/s

# Map 1600 cm^-1 -> 300 Hz (uniform scaling)
K  = (1600 * c) / 300.0

# Glycine zwitterion modes: (cm^-1, relative intensity)
peaks = [
    (3330, 0.55), (3200, 0.60), (3020, 0.25), (2940, 0.30),
    (1650, 1.00), (1498, 0.75), (1410, 0.90), (1330, 0.40),
    (1232, 0.40), (1209, 0.30), (1040, 0.80), (929, 0.30),
    (889, 0.30), (616, 0.50), (513, 0.40)
]

# Normalize intensities so their sum = 1 (clean global gain)
I_sum = sum(p[1] for p in peaks)
peaks = [(cm, i / I_sum) for cm, i in peaks]

cm_min = min(cm for cm, _ in peaks)
cm_max = max(cm for cm, _ in peaks)

def half_life(cm, hl_hi=40.0, hl_lo=240.0):
    """
    Map wavenumber to half-life (seconds):
      - highest cm^-1 -> shortest half-life (hl_hi)
      - lowest cm^-1  -> longest half-life (hl_lo)
    """
    u = (cm - cm_min) / (cm_max - cm_min + 1e-12)  # 0..1
    return hl_hi + (hl_lo - hl_hi) * (1.0 - u)

rng = np.random.default_rng(42)

def smooth_noise(n, block=500, scale=0.005):
    """
    Slow, smooth noise for frequency jitter (dephasing).
    'block' controls the timescale, 'scale' the depth.
    """
    block = max(1, block)
    nblocks = int(np.ceil(n / block)) + 1
    vals = rng.normal(0, 1, nblocks)
    out = np.zeros(n)
    idx = 0
    for b in range(nblocks - 1):
        v0, v1 = vals[b], vals[b + 1]
        for k in range(block):
            if idx >= n:
                break
            u = k / block
            u_s = (1 - np.cos(np.pi * u)) * 0.5  # cosine interpolation
            out[idx] = (1 - u_s) * v0 + u_s * v1
            idx += 1
    m = np.max(np.abs(out))
    if m > 1e-9:
        out /= m
    return out * scale

# Shared slow jitter field for all modes
jitter = smooth_noise(len(t), block=500, scale=0.005)

L = np.zeros_like(t)
R = np.zeros_like(t)

# Build glycine tone with evaporation
for cm, intrel in peaks:
    # Vibrational frequency mapped to audio (Hz)
    f_center = (c * cm) / K
    f_center *= (1.0 + rng.normal(0, 0.001))  # tiny per-mode detune

    # Exponential half-life envelope
    hl = half_life(cm)
    env = np.exp(-np.log(2) * t / hl)

    # Soft global fade in/out
    fi = int(0.1 * sr)
    fo = int(0.1 * sr)
    fade = np.ones_like(t)
    fade[:fi] = np.linspace(0, 1, fi)
    fade[-fo:] = np.linspace(1, 0, fo)
    env *= fade

    # Jittered instantaneous frequency (simulated dephasing)
    inst_freq = f_center * (1.0 + jitter)
    phase = 2 * np.pi * np.cumsum(inst_freq) / sr

    # Tiny L/R detune for stereo width
    det = 1e-3
    sig_L = np.sin(phase * (1 - det / 2))
    sig_R = np.sin(phase * (1 + det / 2))

    L += sig_L * env * intrel
    R += sig_R * env * intrel

# Thermal bath / solvent continuum: low-passed noise rising at the end
noise = rng.normal(0, 1, len(t))
cutoff = 200.0
alpha = (2 * np.pi * cutoff) / (2 * np.pi * cutoff + sr)
y = np.zeros_like(noise)
for n in range(1, len(t)):
    y[n] = y[n - 1] + alpha * (noise[n] - y[n - 1])

m = np.max(np.abs(y))
if m > 1e-9:
    y /= m

# Last 60 s: rise into bath-only state
rise = np.clip((t - (T - 60.0)) / 60.0, 0.0, 1.0)
L += 0.04 * rise * y
R += 0.04 * rise * y

# Normalize and write to WAV
peak = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
L = np.clip(0.85 * L / peak, -1, 1)
R = np.clip(0.85 * R / peak, -1, 1)

stereo = np.int16(np.vstack([L, R]).T * 32767)

out_name = "glycine_evaporation_zwitterion_5min.wav"
with wave.open(out_name, "wb") as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    wf.writeframes(stereo.tobytes())

print("Wrote:", out_name)

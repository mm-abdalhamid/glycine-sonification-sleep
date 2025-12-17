# Glycine Vibrational Sonification and Sleep-Linked Stimuli
![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17948540.svg)](https://doi.org/10.5281/zenodo.17948540)

This repository contains the code, audio files, visual sigils, and narration text used to generate and evaluate a zwitterionic glycine vibrational sonification sequence and its corresponding five-minute rotating sigil.

The materials are intended for researchers interested in:
- Molecule-specific sonification based on vibrational spectra
- Pre-sleep glycine intake, nitric oxide (NO) and thermoregulation
- Sleep-related auditory stimulation and audio-visual experimental tools

---

## Repository structure

A suggested structure for this repository is:

- `Code/`
  - Python scripts used to generate the audio stimuli and sigil videos, for example:
    - `glycine_evaporation_zwitterion_5min.py`
    - `glycine_sigil_evaporation_5min_rotating_legend.py`
    - `glycine_sigil_narration.py`
    - `glycine_combine_video_audio.py`
- `Audio/`
  - Exported WAV files, e.g.:
    - `glycine_evaporation_zwitterion_5min.wav`
    - `glycine_sigil_narration.wav`
- `video/`
  - MP4 files of the sigil:
    - `sigil_5min_vib_only.mp4`
    - `sigil_5min_vib_narration.mp4`
- `text/`
  - Narration script and any supplementary text files:
    - `glycine_sigil_narration.txt`

---

## Requirements

To run the Python scripts and regenerate the audio and video, you will typically need:

- Python 3.10+  
- Recommended packages:
  - `numpy`
  - `scipy`
  - `soundfile` or a similar audio I/O library
  - `matplotlib` (for plots, if used)
  - `moviepy` or `ffmpeg` (installed on the system) for combining audio and video

Install dependencies, for example:

```bash
pip install numpy scipy soundfile matplotlib moviepy
```

You may also need a working `ffmpeg` installation available on your system path.

---

## Reproducing the audio stimulus

1. Navigate to the `Code/` folder.
2. Run the glycine evaporation script, for example:

```bash
python glycine_evaporation_zwitterion_5min.py
```

3. The script will:
   - Load the predefined vibrational peak list for zwitterionic glycine.
   - Map peaks to audio frequencies and envelopes.
   - Render a five-minute stereo WAV file.
4. The output file (e.g. `glycine_evaporation_zwitterion_5min.wav`) will be placed in the `audio/` directory.

Please refer to the inline comments in the script for parameter details (amplitude, envelopes, fade-in/out, and any evaporation-style modulation).

---

## Reproducing the rotating sigil

1. Navigate to the `Code/` folder.
2. Run the sigil generation script:

```bash
python glycine_sigil_evaporation_5min_rotating_legend.py
```

This script generates a five-minute MP4 video of the glycine-derived sigil with a rotating layout and legend, saving it to the `video/` directory (e.g. `sigil_5min_vib_only.mp4`).

To add narration to the sigil:

1. Ensure you have:
   - The narration audio file in `audio/` (e.g. `glycine_sigil_narration.wav`)
   - The silent sigil video in `video/` (e.g. `sigil_5min_vib_only.mp4`)
2. Run the combination script:

```bash
python glycine_combine_video_audio.py
```

This script (or an equivalent `ffmpeg` command inside it) will mux the narration onto the sigil video and produce `sigil_5min_vib_narration.mp4` in the `video/` directory.

---

## Data and code availability

A citable, versioned archive of this repository (code, audio, video, and text files) is provided via Zenodo:

* DOI: 10.5281/zenodo.17948540

The GitHub repository and the Zenodo snapshot contain the same core materials. The manuscript cites the Zenodo record as the primary data and code availability reference.

---

## Licensing

- **Code (Python scripts and parameter files)**: MIT License (see `LICENSE`).
- **Manuscript-style text and static figures (if included)**: CC BY 4.0.
- **Audio and video stimuli (WAV and MP4 files)**: CC BY-NC 4.0 (see `LICENSE`).

You are free to share and adapt the audio and video materials for **non-commercial** purposes, provided you give appropriate credit and indicate if changes were made.

> **Important:** Commercial use of the audio and video materials is **not permitted** without prior written permission from the corresponding author.

---

## Citation

If you use this repository or its derived stimuli in academic work, please cite the Zenodo record, for example:

> AbdAlhamid MM. Zwitterionic glycine vibrational sonification and sleep-linked audio–visual stimuli (code, audio, sigil) [Dataset]. Zenodo. 2025. DOI: 10.5281/zenodo.17948540.

In addition, please cite the main manuscript describing the methods and results once published.

---

## Copyright

© 2025 M M abdAlhamid.

Except where a specific open license is indicated in the *Licensing* section above (MIT, CC BY 4.0, or CC BY-NC 4.0), all other rights in this repository are reserved by the author. Any use outside the scope of those licenses requires prior written permission from the corresponding author.

---

## Contact

For questions about the code, audio stimuli, licensing, or potential collaborations, please contact:

**M M abdAlhamid**  
Corresponding author  
Email: `mm.abdalhamid@icloud.com`

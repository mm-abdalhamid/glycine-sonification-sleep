# Glycine Vibrational Sonification and Sleep-Linked Stimuli
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17948540.svg)](https://doi.org/10.5281/zenodo.17948540)

This repository contains the code, audio files, visual sigils, and narration text used to generate and evaluate a zwitterionic glycine vibrational sonification sequence and its corresponding five-minute rotating sigil.

The materials are intended for researchers interested in:
- Molecule-specific sonification based on vibrational spectra
- Pre-sleep glycine intake, nitric oxide (NO) and thermoregulation
- Sleep-related auditory stimulation and audio-visual experimental tools

---

## Repository structure

This repository is organized as:

- `Code/`
  - Python scripts used to generate the audio stimuli and sigil videos, for example:
    - `glycine_evaporation_zwitterion_5min_pk_kinetic_licensed.py`  # main five-minute PK-based stimulus
    - `glycine_evaporation_zwitterion_5min.py`  # original evaporation-only prototype
    - `glycine_sigil_pk_5min_rotating_licensed.py`  # PK-envelope rotating sigil
    - `glycine_sigil_evaporation_5min_rotating_legend.py`  # original evaporation-based sigil (legacy)
    - `glycine_sigil_narration.py`
- `Audio/`
  - Exported WAV files, e.g.:
    - `glycine_evaporation_zwitterion_5min_pk_kinetic.wav`  # main PK-based stimulus
    - `glycine_evaporation_zwitterion_5min.wav`  # original evaporation-only prototype
    - `glycine_sigil_narration.wav`  # narration audio track
- `video/`
  - MP4 files of the sigil:
    - `glycine_sigil_pk_5min_rotating.mp4`  # PK-envelope rotating sigil
    - `sigil_5min_vib_only_v2.mp4`  # vibration-only sigil (legacy)
    - `sigil_5min_vib_narration_v2.mp4`  # narrated sigil (legacy)
- `text/`
  - Narration script and any supplementary text files:
    - `glycine_sigil_narration.txt`
- `docs/`
  - This note is written for researchers who may want to test the glycine sonification and sigil as experimental stimuli:
    - `for_experimenters.md`
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
2. Run the PK-based glycine evaporation script:

```bash
python glycine_evaporation_zwitterion_5min_pk_kinetic_licensed.py
```

3. The script will:
   - Load the predefined vibrational peak list for zwitterionic glycine.
   - Map peaks to audio frequencies and apply the pharmacokinetic (PK) envelope described in the manuscript.
   - Render a five-minute stereo WAV file.
4. The output file (e.g. `glycine_evaporation_zwitterion_5min_pk_kinetic.wav`) will be placed in the `audio/` directory.

If you wish to reproduce the original evaporation-only prototype instead, you can run:

```bash
python glycine_evaporation_zwitterion_5min.py
```

This legacy script uses the same vibrational mapping but a simpler evaporation-style amplitude envelope, without a pharmacokinetic model.

Please refer to the inline comments in the script for parameter details (amplitude, envelopes, fade-in/out, and any evaporation-style modulation).

---

## Reproducing the rotating sigil

1. Navigate to the `Code/` folder.
2. Run the sigil generation script:

```bash
python glycine_sigil_pk_5min_rotating_licensed.py
```

This script generates a five-minute MP4 video of the glycine sigil using the same PK envelope (and one slow rotation), writing it to the `video/` directory (e.g. `sigil_5min_vib_only.mp4`).

To add narration to the sigil:

1. Ensure you have:
   - The narration audio file in `audio/` (e.g. `glycine_sigil_narration.wav`)

The original evaporation-based sigil script (`glycine_sigil_evaporation_5min_rotating_legend.py`)
is also included for historical and comparative purposes.
   - The silent sigil video in `video/` (e.g. `sigil_5min_vib_only.mp4`)
2. Run the combination script:

```bash
python glycine_combine_video_audio.py
```

This script (or an equivalent `ffmpeg` command inside it) will mux the narration onto the sigil video and produce `sigil_5min_vib_narration.mp4` in the `video/` directory.

---

### For experimenters (prototype use only)

The glycine sonification and sigil in this repository are **prototype stimuli** intended for exploratory research on pre-sleep state and thermoregulation.  
They are **not** medical treatments and have **no established efficacy**.

Very short guidance:

- Use first in **healthy adults** under an approved protocol.
- Play the **5-minute audio once, 30–60 min before usual bedtime**.
- Prefer **chest-level speakers** or near-field monitors at comfortable, conversational loudness; avoid high-volume headphones.
- Always compare against at least one **control condition** (e.g. spectrally matched random sound, noise, or usual routine).
- Focus on **exploratory outcomes** such as subjective thermal comfort, simple sleep diaries, actigraphy, and basic cardiovascular / skin-temperature markers if available.

For a more detailed, non-prescriptive guide to possible study designs and outcome measures, see:  
`docs/for_experimenters.md`

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

- **Logo:** Glycine PK sigil logo copyright (c) 2025 M M abdAlhamid.  
  All rights reserved; see LOGO_LICENSE.txt.

---

## Contact

For questions about the code, audio stimuli, licensing, or potential collaborations, please contact:

**M M abdAlhamid**  
Corresponding author  
Email: `mm.abdalhamid@icloud.com`

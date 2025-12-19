# Glycine Sonification – Audio Folder

This folder contains the core sonification audio files and supporting documentation for the glycine
project.

## Files

- `glycine_evaporation_zwitterion_5min_pk_kinetic.wav`  
  Main five-minute glycine sonification used in the current manuscript. This waveform is generated
  by `glycine_evaporation_zwitterion_5min_pk_kinetic_licensed.py`, which maps zwitterionic glycine
  vibrational peaks to audio frequencies and applies a one-compartment oral pharmacokinetic (PK)
  envelope (0–4 hours compressed into 300 seconds) to shape the overall amplitude.

- `glycine_evaporation_zwitterion_5min.wav`  
  Original five-minute evaporation-only prototype. Uses the same vibrational mapping but a simpler
  evaporation-style amplitude envelope, without a PK model. Kept as a legacy stimulus for comparison
  and exploratory work.

- `glycine_audio_technical_profile.txt`  
  Plain-text technical profile of the legacy WAV file, including:
  - sampling rate, channels, and duration  
  - RMS and peak levels  
  - approximate spectral power distribution  
  - loudness envelope characteristics  
  This file is intended to give researchers a quick engineering-level view of the signal and its
  mid-band, non-harsh profile.

## Playback considerations

- Use speakers placed at chest level or slightly below rather than headphones, to avoid excessive
  head-localized stimulation.
- Keep playback volume in a comfortable range, roughly similar to soft speech or quiet background
  music in the room.
- If using the stimuli before sleep in an experimental context, typical timing in early-stage
  protocols is a single 5-minute exposure within the 30–60 minutes before habitual bedtime.

## Interpretation and intended use

These audio files are intended as **experimental stimuli** for studying ideas around molecule-anchored
sonification, thermoregulation, and sleep. They are:

- designed to be precisely reproducible,  
- documented in the accompanying manuscript and code,  
- suitable for small, carefully monitored pilot studies.

They are **not** validated as clinical interventions, and no therapeutic effect should be assumed.
Any observed changes in sleep or thermal comfort should be treated as preliminary and reported
cautiously.

## License

As per project licensing summary:

- `/audio/` (WAV files and associated audio content) → **CC BY-NC 4.0**  

You are free to:
- share and adapt the material for non-commercial purposes,  
- provided that appropriate credit is given and changes are indicated,  
- and that no additional restrictions beyond CC BY-NC 4.0 are applied.

For full terms, please refer to the Creative Commons Attribution-NonCommercial 4.0 International
license.

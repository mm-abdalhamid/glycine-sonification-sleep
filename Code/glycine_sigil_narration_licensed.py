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
Generate narration audio for the glycine sigil video using macOS TTS.

Pipeline (reproducible):
1. Read narration text from a .txt file.
2. Use macOS `say` with a chosen system voice (default: Ava Enhanced).
3. Export AIFF.
4. Convert AIFF → WAV with ffmpeg for easy use in video editors.

Requirements:
- macOS
- `say` available (built into macOS)
- `ffmpeg` installed and on PATH
    e.g. `brew install ffmpeg`
"""

import subprocess
from pathlib import Path

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
# Voice choice:
# Community feedback (especially from visually impaired users) often
# rates Ava (Enhanced) as clear and relatively natural, especially
# at higher speech rates, though Alex is also popular. Here we
# default to Ava (Enhanced) for clarity.
#
# If "Ava (Enhanced)" is not installed on your Mac, run:
#   say -v '?' | grep Ava
# and pick one of the available Ava variants, then update VOICE_NAME.
VOICE_NAME = "Ava (Enhanced)"

# Speech rate (words per minute). macOS default is ~175.
SPEECH_RATE = "165"

# Input narration file and output audio filenames
TEXT_FILE = Path("glycine_sigil_narration_short.txt")
AIFF_FILE = Path("glycine_sigil_narration.aiff")
WAV_FILE  = Path("glycine_sigil_narration.wav")


def generate_narration():
    if not TEXT_FILE.exists():
        raise FileNotFoundError(f"Text file not found: {TEXT_FILE}")

    # 1) Use macOS TTS via `say` to generate AIFF
    print(f"Generating AIFF with voice: {VOICE_NAME} at {SPEECH_RATE} wpm")
    subprocess.run(
        [
            "say",
            "-v", VOICE_NAME,
            "-r", SPEECH_RATE,
            "-o", str(AIFF_FILE),
            "-f", str(TEXT_FILE),
        ],
        check=True,
    )

    # 2) Convert AIFF → WAV using ffmpeg
    print(f"Converting {AIFF_FILE} → {WAV_FILE} via ffmpeg")
    subprocess.run(
        [
            "ffmpeg",
            "-y",             # overwrite existing
            "-i", str(AIFF_FILE),
            "-acodec", "pcm_s16le",
            str(WAV_FILE),
        ],
        check=True,
    )

    print(f"Done. Wrote {WAV_FILE}")


if __name__ == "__main__":
    generate_narration()

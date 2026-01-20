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
Refined combination of glycine sigil video with vibrational audio and narration using ffmpeg.

Fixes vs v1:
  - Explicitly maps video and audio streams so vibrational-only output actually has sound.
  - Lowers vibrational audio much more under narration (0.25) so Ava remains clearly intelligible.
  - Uses amix normalization to avoid the mixed audio being excessively loud at the start.

Inputs (same folder as this script, or adjust paths below):
  - sigil_5min.mp4             : 5-minute glycine sigil video
  - glycine_vib_5min.wav       : 5-minute vibrational audio
  - glycine_narration.wav      : short narration audio (Ava Enhanced)

Outputs:
  - sigil_5min_vib_only_v2.mp4        : video + vibrational audio only
  - sigil_5min_vib_narration_v2.mp4   : video + vibrational audio + narration mix

Requirements:
  - ffmpeg installed and on PATH
    (e.g. on macOS: `brew install ffmpeg`)
"""

import subprocess
from pathlib import Path

# ------------------------------------------------------------------
# File paths (edit if your names differ)
# ------------------------------------------------------------------
VIDEO_IN      = Path("sigil_5min.mp4")
VIB_AUDIO_IN  = Path("glycine_vib_5min.wav")
NARR_AUDIO_IN = Path("glycine_narration.wav")

VIB_ONLY_OUT  = Path("sigil_5min_vib_only_v2.mp4")
VIB_NARR_OUT  = Path("sigil_5min_vib_narration_v2.mp4")


def run(cmd):
    """Run a subprocess command with basic logging."""
    print("Running:", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True)


def make_vib_only():
    """
    Attach vibrational audio as the only audio track on the video.
    Any existing audio in VIDEO_IN is ignored by explicit mapping.
    """
    cmd = [
        "ffmpeg",
        "-y",                   # overwrite output if it exists
        "-i", str(VIDEO_IN),    # input 0: video
        "-i", str(VIB_AUDIO_IN),# input 1: vib audio
        "-map", "0:v:0",        # take video stream from input 0
        "-map", "1:a:0",        # take audio stream from input 1
        "-c:v", "copy",         # copy video stream without re-encoding
        "-c:a", "aac",          # encode audio as AAC
        "-shortest",            # stop when the shorter of video/audio ends
        str(VIB_ONLY_OUT),
    ]
    run(cmd)
    print("Wrote", VIB_ONLY_OUT)


def make_vib_plus_narr():
    """
    Mix vibrational audio + narration and attach to the video.

    - Vibrational audio is reduced to 0.25 (25%) under narration.
    - Narration remains at full level.
    - amix 'normalize=1' avoids the mix being excessively loud
      when both are active.
    - After narration ends, only vibrational audio continues.
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(VIDEO_IN),       # input 0: video
        "-i", str(VIB_AUDIO_IN),   # input 1: vib audio
        "-i", str(NARR_AUDIO_IN),  # input 2: narration
        "-filter_complex",
        (
            "[1:a]volume=0.25[a_vib];"
            "[2:a]volume=1.0[a_narr];"
            "[a_vib][a_narr]amix=inputs=2:duration=longest:"
            "dropout_transition=2:normalize=1[a_mix]"
        ),
        "-map", "0:v:0",        # video from first input
        "-map", "[a_mix]",      # mixed audio
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(VIB_NARR_OUT),
    ]
    run(cmd)
    print("Wrote", VIB_NARR_OUT)


if __name__ == "__main__":
    make_vib_only()
    make_vib_plus_narr()

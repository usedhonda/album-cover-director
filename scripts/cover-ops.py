#!/usr/bin/env python3
"""Compatibility wrapper for the self-contained Album Cover Director utility."""

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[1] / "skills/album-cover-director/scripts/cover-ops.py"), run_name="__main__")

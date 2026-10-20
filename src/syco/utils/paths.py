"""Path helpers. All paths are relative to the installed package / cwd.

Nothing here hardcodes an absolute path so the repo can be dropped into
another project (e.g. TMI's main repo) without surprises.
"""

from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    """Return the current working directory as the project root.

    We intentionally use cwd rather than walking up from __file__, so that
    experiments launched from inside a merged monorepo still write results
    into whichever directory the user runs the CLI from.
    """
    return Path.cwd()


def results_dir() -> Path:
    """Where runs are written. Overridable via SYCO_RESULTS_DIR."""
    override = os.environ.get("SYCO_RESULTS_DIR")
    base = Path(override) if override else project_root() / "results"
    base.mkdir(parents=True, exist_ok=True)
    return base


def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

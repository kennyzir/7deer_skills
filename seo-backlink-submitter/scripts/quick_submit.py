#!/usr/bin/env python3
"""Compatibility entry point for the safe single-directory submitter CLI."""

from __future__ import annotations

from typing import Sequence

import submit_to_directory


def main(argv: Sequence[str] | None = None) -> int:
    return submit_to_directory.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())

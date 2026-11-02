"""Shims so transformers>=5.2 can run on Mac Intel with torch==2.2.x."""
from __future__ import annotations

import torch


def apply_torch_compat_shims() -> None:
    for name, fallback in (
        ("uint16", torch.int32),
        ("uint32", torch.int64),
        ("uint64", torch.int64),
    ):
        if not hasattr(torch, name):
            setattr(torch, name, fallback)

    if not hasattr(torch, "get_default_device"):
        torch.get_default_device = lambda: torch.device("cpu")  # type: ignore[attr-defined]

    # Keep original for no-arg calls; accept optional device_type from newer transformers.
    _orig = torch.is_autocast_enabled

    def _is_autocast_enabled(device_type=None):
        try:
            return _orig(device_type) if device_type is not None else _orig()
        except TypeError:
            return _orig()

    torch.is_autocast_enabled = _is_autocast_enabled  # type: ignore[assignment]


apply_torch_compat_shims()

"""Apply small compatibility patches for transformers 5.2 + torch 2.2 (Mac Intel)."""
from __future__ import annotations

from pathlib import Path

import transformers


def _patch_file(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text()
    if new in text:
        print(f"OK already patched: {label}")
        return
    if old not in text:
        print(f"SKIP (pattern not found): {label}")
        return
    path.write_text(text.replace(old, new, 1))
    print(f"PATCHED: {label}")


def main() -> None:
    root = Path(transformers.__file__).resolve().parent

    _patch_file(
        root / "utils" / "import_utils.py",
        '''        if is_available and parsed_version < version.parse("2.4.0"):
            logger.warning_once(f"Disabling PyTorch because PyTorch >= 2.4 is required but found {torch_version}")
        return is_available and version.parse(torch_version) >= version.parse("2.4.0")''',
        '''        # Mac Intel: official torch wheels stop at 2.2.x
        if is_available and parsed_version < version.parse("2.2.0"):
            logger.warning_once(f"Disabling PyTorch because PyTorch >= 2.2 is required but found {torch_version}")
        return is_available and version.parse(torch_version) >= version.parse("2.2.0")''',
        "torch version gate",
    )

    _patch_file(
        root / "utils" / "generic.py",
        "    if torch.is_autocast_enabled(device_type) or enabled:",
        '''    try:
        autocast_on = torch.is_autocast_enabled(device_type)
    except TypeError:
        autocast_on = torch.is_autocast_enabled()
    if autocast_on or enabled:''',
        "maybe_autocast",
    )


if __name__ == "__main__":
    main()

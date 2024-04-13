from pathlib import Path
from typing import Literal


# You can use an enum too
def find_compiled_modules(
    source_dir: str, os: Literal["Windows", "GNU/Linux", "MacOS"]
) -> list[str]:
    if os == "Windows":
        filetype = "dll"
    elif os == "GNU/Linux":
        filetype = "so"
    elif os == "MacOS":
        filetype = "dylib"
    dir = Path(source_dir)
    # Docker like syntax, filepath on host matched by filepath on binary
    return [(f, source_dir) for f in dir.rglob(f"*.{filetype}")]

import ast
import asyncio
import logging
from pathlib import Path
from typing import AsyncGenerator
import aiofiles

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Useful for Pyinstaller bundling avoiding missing used dependencies
async def __extract_imports_from_file(file_path: Path) -> AsyncGenerator[str, None]:
    """Extract imported module names from a Python file asynchronously."""
    async with aiofiles.open(file_path, "r", encoding="utf-8") as file:
        root = ast.parse(await file.read(), str(file_path))

    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for node_name in node.names:
                yield node_name.name
        elif isinstance(node, ast.ImportFrom):
            yield node.module


async def __find_python_files(
    directory: Path, types: list[str] = ["py"]
) -> AsyncGenerator[Path, None]:
    """Find all Python files in the given directory asynchronously."""
    for file_type in types:
        for file_path in directory.rglob(f"*.{file_type}"):
            yield file_path


async def __find_imports(source_dir: str) -> set[str]:
    source_dir_path = Path(source_dir).resolve()
    script_path = Path(__file__).resolve(strict=False)
    hidden_imports = set()

    async for file in __find_python_files(source_dir_path):
        if file.resolve(strict=False) == script_path:
            continue
        async for module_name in __extract_imports_from_file(file):
            hidden_imports.add(module_name)

    return hidden_imports


async def find_imports(source_dir: str) -> set[str]:
    return await __find_imports(source_dir)


# Example usage
imports = asyncio.run(find_imports("."))
logger.info(imports)

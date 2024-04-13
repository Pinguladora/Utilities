from setuptools import Extension
from pathlib import Path


# Useful for Cython bundling
def find_module_extensions(
    rel_dir_path: str | Path, types: list[str] = ["py"]
) -> list[Extension]:
    """
    Find Python files in the specified directory and create Extension objects for each file.

    Args:
        rel_dir_path (str | Path): The relative directory path to search for Python files.
        types (list[str]): List of file extensions to search for. Defaults to ["py"].

    Returns:
        list[Extension]: A list of Extension objects.
    """
    dir_path = Path(rel_dir_path)
    script_path = Path(__file__).resolve(strict=False)
    extensions = []
    for file_type in types:
        filepaths = dir_path.rglob(f"*.{file_type}")
        for path in filepaths:
            # Normalize path for current OS
            normalized_path = path.resolve()
            if normalized_path == script_path:
                continue
            # Create module name using file stem
            module_name = path.with_suffix("").as_posix().replace("/", ".")

            # Create an Extension object for each file
            extensions.append(Extension(module_name, [str(normalized_path)]))
    return extensions


# Example usage
files = find_module_extensions(".")
print(files)

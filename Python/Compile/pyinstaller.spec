# -*- mode: python ; coding: utf-8 -*-

from imports_finder import find_imports
from compile_finder import find_compiled_modules

BINARY_NAME="main"
# An entrypoint is ALWAYS required for Pyinstaller to work. 
# The rest of the code can be compiled such as .so, .dll or .dylib files.
ENTRYPOINTS=['main.py']
# Valid values are x86_64, arm64, and universal2.
# https://pyinstaller.org/en/stable/feature-notes.html?highlight=target_arch#macos-multi-arch-support
ARCH="x86_64"
# Windows target only
UPX=False
# Remove tails
# Not recommended for Windows
STRIP=True
# https://pyinstaller.org/en/stable/operating-mode.html?highlight=console#using-a-console-window
CONSOLE=False
# https://pyinstaller.org/en/stable/when-things-go-wrong.html?highlight=debug#getting-debug-messages
DEBUG=False

# Options such as PYTHONDONTWRITEBYTECODE, PYTHONUNBUFFERED, etc. are INHERITED from the interpreter used
# to generate the app, unless explicitly overridden.
# Optimize debug and docstrings.
options = [
    ('OO', None, 'OPTION')
]

analysis = Analysis(
    ENTRYPOINTS,
    pathex=[],
    # Cython C compiled modules
    binaries=list(find_compiled(".")),
    datas=[],
    # Python imports which has been compiled with Cython MUST be specified as hiddenimports
    hiddenimports=list(find_imports(".")),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(analysis.pure)

exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    options=options,
    name=BINARY_NAME,
    debug=DEBUG,
    bootloader_ignore_signals=False,
    strip=STRIP,
    upx=UPX,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=CONSOLE,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=ARCH,
    codesign_identity=None,
    entitlements_file=None,
)

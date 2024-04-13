from setuptools import setup
from Cython.Build import cythonize
from Cython.Distutils import build_ext
from extension_finder import find_module_extensions

extensions = find_module_extensions()

setup(
    name="C-binary app",
    version="1.0.0",
    author="Pinguladora",
    author_email="pinguladora@example.com",
    description="An example on how to generate a C-application using Cython and Pyinstaller.",
    ext_modules=cythonize(extensions, build_dir="build", language_level="3str"),
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    include_package_data=True,
)

import sys

from pybind11 import get_cmake_dir
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

__version__ = "0.0.3"

ext_modules = [
    Pybind11Extension("cpp_stoch",
        ["src/wrapper.cpp", "src/mandelbrot.cpp"],
        define_macros=[('VERSION_INFO', __version__)],
        extra_compile_args=["-fopenmp"],
        extra_link_args=["-fopenmp"]
    )
]

setup(
    name="cpp_stoch",
    version=__version__,
    author="Steven Oud",
    author_email="soud@pm.me",
    description="C++ bindings for Stochastic Simulation",
    long_description="",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    python_requires=">=3.6",
)

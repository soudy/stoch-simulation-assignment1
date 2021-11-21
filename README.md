# Stochastic Simulations Assignment 1: Approximating the Area of the Mandelbrot Set Through Monte Carlo Methods
This repository contains all the code used for the first assignment of
Stochastic Simulations.
It is organized in two folders:
- `cpp_stoch`
- `notebooks`
The `cpp_stoch` folder contains the C++ code used for calculating the Mandelbrot
set.
It uses [pybind11](https://github.com/pybind/pybind11) to create Python
bindings, which is used in the `notebooks` folder for running and visualizing
experiments.
The libraries and software required to run our code is described below.

## Prerequisites
The notebooks are written in Python (3.7+) and uses the following libraries:
- numpy
- matplotlib
- seaborn
- pandas
- scipy
- statsmodels
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- shelve (for persisting data)

## C++ Bindings Installation
In addition to the libraries listed in the prerequisites, a C++11 compiler is
required for installing the C++ bindings (`gcc` on Linux, `clang` on macOS,
MinGW or Visual Studio on windows).
Once a C++11 compiler is present, you can install pybid11 as follows:
```bash
pip install pybind11
```
Then, to install the Python C++ bindings, run the following in the root
directory of this repository:
```
pip install cpp_stoch/
```
_Note: the forward slash is required!_
This installs the `cpp_stoch` Python library which we use in our notebooks.

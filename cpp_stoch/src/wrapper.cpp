#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include "mandelbrot.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(cpp_stoch, m) {
    m.def("f_c", &f_c, R"pbdoc(Calculate z_n sequence)pbdoc",
          py::arg("c"), py::arg("max_iter") = MAX_ITER, py::arg("d") = 2);
    m.def(
        "mandelbrot_grid", &mandelbrot_grid, py::call_guard<py::gil_scoped_release>(),
        R"pbdoc(Calculate f_c for grid with dimensions width x height)pbdoc",
        py::arg("width"), py::arg("height"),
        py::arg("start") = std::complex<double>(-2, -1.12),
        py::arg("end") = std::complex<double>(1, 1.12),
        py::arg("max_iter") = MAX_ITER,
        py::arg("d") = 2
    );
    m.def("set_num_threads", &omp_set_num_threads, "Set number of threads");
    m.def("get_num_threads", &omp_get_num_threads, "Get number of threads");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}

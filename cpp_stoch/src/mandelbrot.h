#include <complex>
#include <vector>
#include <omp.h>

#define MAX_ITER 256

typedef std::pair<std::complex<double>, int> ZIterPair;

ZIterPair f_c(std::complex<double> c, int max_iter, int d);
std::vector<std::vector<ZIterPair>> mandelbrot_grid(
    int width, int height, std::complex<double> start, std::complex<double> end,
    int max_iter, int d
);

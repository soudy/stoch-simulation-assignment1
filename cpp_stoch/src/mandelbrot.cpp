#include "mandelbrot.h"
#include <cmath>

ZIterPair f_c(std::complex<double> c, int max_iter = MAX_ITER, int d = 2) {
    double x = c.real();
    double y = c.imag();
    double x2 = 0;
    double y2 = 0;
    double w = 0;
    double i = 0;

    while ((x2 + y2) <= 4 && i < max_iter) {
        if (d == 2) {
            x = x2 - y2 + c.real();
            y = w - x2 - y2 + c.imag();

            x2 = x*x;
            y2 = y*y;
            w = (x + y)*(x + y);
        } else {
            std::complex<double> z(x2, y2);
            z = std::pow(z, d) + c;
            x2 = z.real();
            y2 = z.imag();
        }
        i++;
    }

    std::complex<double> z(x2, y2);

    return std::make_pair(z, i);
}

std::vector<std::vector<ZIterPair>> mandelbrot_grid(
    int width, int height,
    std::complex<double> start = std::complex<double>(-2, -1.12),
    std::complex<double> end = std::complex<double>(1, 1.12),
    int max_iter = MAX_ITER,
    int d = 2
) {
    omp_set_num_threads(8);
    std::vector<std::vector<ZIterPair>> grid(width, std::vector<ZIterPair>(height));

#pragma omp parallel for
    for (int x = 0; x < width; x++) {
        for (int y = 0; y < height; y++) {
            std::complex<double> c(
                start.real() + ((float)x/width * (end.real() - start.real())),
                start.imag() + ((float)y/height * (end.imag() - start.imag()))
            );

            ZIterPair zi = f_c(c, max_iter, d);
            grid[x][y] = zi;
        }
    }

    return grid;
}

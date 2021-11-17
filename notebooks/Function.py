import numpy as np
import queue
from scipy.stats import qmc
from cpp_stoch import (
    f_c as f_c_cpp,
    mandelbrot_grid,
    set_num_threads,
    get_num_threads
)
from orthogonal_sampler import orthogonal_sampler_2d, optimal_orthogonal_sampler_2d


def uniform_sampler(rng, lows, highs, n_samples):
    return rng.uniform(low=lows, high=highs, size=(n_samples, len(lows)))


def latin_square_sampler(rng, lows, highs, n_samples):
    sampler = qmc.LatinHypercube(d=2, seed=rng)
    sample = sampler.random(n_samples)
    scaled = qmc.scale(sample, lows, highs)

    return scaled


def scrambled_sobol_sampler(rng, lows, highs, n_samples):
    m = np.log2(n_samples)
    if np.mod(m, 1) != 0:
        raise Exception(f"n_samples not a power of 2: {n_samples} (required for generating Sobol sequence)")

    sampler = qmc.Sobol(d=2, seed=rng)
    sample = sampler.random_base2(n_samples)
    scaled = qmc.scale(sample, lows, highs)

    return scaled


def orthogonal_sampler(rng, lows, highs, n_samples):
    sample = orthogonal_sampler_2d(rng, n_samples)
    xs = (highs[0] - lows[0])*sample[:,0] + lows[0]
    ys = (highs[1] - lows[1])*sample[:,1] + lows[1]

    return np.array([xs, ys]).T


def optimal_orthogonal_sampler(rng, lows, highs, n_samples):
    sample = optimal_orthogonal_sampler_2d(rng, n_samples)
    xs = (highs[0] - lows[0])*sample[:,0] + lows[0]
    ys = (highs[1] - lows[1])*sample[:,1] + lows[1]

    return np.array([xs, ys]).T


def Monte_carlo(sample_size, max_iter, rng, sampler):
    X_LB, X_UP = -2, 1
    Y_LB, Y_UP = -1.12, 1.12

    samples_in_set = 0
    random_numbers = sampler(rng, (X_LB, Y_LB), (X_UP, Y_UP), sample_size)
    for i in range(sample_size):
        x, y = random_numbers[i]
        c = complex(x, y)

        (z, j) = f_c_cpp(c, max_iter, 2)

        #Check if it is in set:  |z| <= 2
        if (j == max_iter):
            samples_in_set += 1

    fraction = samples_in_set/sample_size
    Approx_area = (X_UP - X_LB)*(Y_UP - Y_LB)*fraction

    return Approx_area


def I_iter_worker(q, d, sample_size, rng, sampler):
    while True:
        try:
            max_iter, i = q.get_nowait()
        except queue.Empty:
            break

        Approx_area = Monte_carlo(
            sample_size = sample_size, max_iter = max_iter, rng=rng,
            sampler=sampler
        )
        d[i].append(Approx_area)


def S_iter_worker(q, d, max_iter, rng, sampler):
    while True:
        try:
            sample_size, i = q.get_nowait()
        except queue.Empty:
            break

        Approx_area = Monte_carlo(
            sample_size = sample_size, max_iter = max_iter, rng=rng,
            sampler=sampler
        )
        d[i].append(Approx_area)

def N_iter_worker(q, d, sample_size, max_iter, rng, sampler):
    while True:
        try:
            n_runs, i = q.get_nowait()
        except queue.Empty:
            break

        Approx_area = Monte_carlo(
            sample_size = sample_size, max_iter = max_iter, rng=rng,
            sampler=sampler
        )
        d[n_runs].append(Approx_area)

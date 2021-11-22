import numpy as np
from itertools import product


def orthogonal_sampler_2d(rng, n_samples):
    """
    Generates random points in a 2-dimensional space by constructing Latin
    hypercubes with orthogonal arrays. This function implements the algorithm
    described by https://www.tandfonline.com/doi/pdf/10.1080/0266476032000053691
    in Section 2.

    Returns:
        (n_samples, 2) ndarray of random samples
    """
    r = 2
    m = 2
    s = int(np.ceil(np.sqrt(n_samples)))

    oa = np.array(list(product(list(range(1, s+1)), repeat=m)))
    lh = np.zeros(oa.shape)

    for c in range(oa.shape[1]):
        for k in range(1, s+1):
            idxs = np.where(oa[:, c] == k)
            col = oa[idxs]
            new_col = np.zeros(len(idxs[0]))

            for i in range(1, col.shape[0]+1):
                new_col[i-1] = (k - 1)*s + i

            rng.shuffle(new_col)

            lh[idxs[0], c] = new_col

    samples = rng.uniform(size=oa.shape)
    lh = (lh - samples)/np.max(lh)

    extra_samples = lh.shape[0] - n_samples
    if extra_samples == 0:
        return lh
    else:
        rand_rows = rng.choice(lh.shape[0], extra_samples, replace=False)
        return np.delete(lh, rand_rows, axis=0)


def optimal_orthogonal_sampler_2d(rng, n_samples):
    r = 2
    m = 2
    s = int(np.ceil(np.sqrt(n_samples)))

    oa = np.array(list(product(list(range(1, s+1)), repeat=m)))
    lh = np.zeros(oa.shape)

    for c in range(oa.shape[1]):
        for k in range(1, s+1):
            idxs = np.where(oa[:, c] == k)
            col = oa[idxs]
            new_col = np.zeros(len(idxs[0]))

            for i in range(1, col.shape[0]+1):
                new_col[i-1] = (k - 1)*s + i

            rng.shuffle(new_col)

            lh[idxs[0], c] = new_col

    # search for optimal OA
    # just for column 0??
    for k in range(1, s+1):
        row_idxs = np.where(oa[:, 0] == k)[0]
        base_idx = row_idxs[0]
        row_idxs = row_idxs[1:]
        rand_row = rng.choice(row_idxs)
        lh[base_idx][0], lh[rand_row][0] = lh[rand_row][0], lh[base_idx][0]

    samples = rng.uniform(size=oa.shape)
    lh = (lh - samples)/np.max(lh)

    extra_samples = lh.shape[0] - n_samples
    if extra_samples == 0:
        return lh
    else:
        rand_rows = rng.choice(lh.shape[0], extra_samples, replace=False)
        return np.delete(lh, rand_rows, axis=0)

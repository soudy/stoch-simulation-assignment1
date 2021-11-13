import numpy as np
from itertools import product

def orthogonal_sampler_2d(rng, n_samples):
    r = 2
    m = 2
    s = int(np.ceil(np.sqrt(n_samples)))

    oa = np.array(list(product(list(range(1, s+1)), repeat=m)))
    lh = np.zeros(oa.shape)

    for c in range(oa.shape[1]):
        # Yes, I overcomplicated this, and no, I'm not going to fix it
        for k in range(1, (oa.shape[0]//s)+1):
            col = oa[(k-1)*s:k*s:,c]
            new_col = np.zeros(col.shape)

            for i in range(1, s+1):
                new_col[i-1] = (col[k - 1] - 1)*s + i

            lh[(k-1)*s:k*s:,c] = new_col

    for c in range(oa.shape[1]):
        rng.shuffle(lh[:,c])

    samples = rng.uniform(size=oa.shape)
    lh = (lh - samples)/np.max(lh)

    return lh

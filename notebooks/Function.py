

#imports
import numpy as np
from cpp_stoch import (
    f_c as f_c_cpp,
    mandelbrot_grid,
    set_num_threads,
    get_num_threads
)



def Monte_carlo(sample_size, max_iter):
    X_LB, X_UP = -2, 1
    Y_LB, Y_UP = -1.12, 1.12
    
    samples_in_set = 0
    for i in range(sample_size):
        x = np.random.uniform(X_LB, X_UP)
        y = np.random.uniform(Y_LB, Y_UP)
        c = complex(x, y)
        
        (z, j) = f_c_cpp(c, max_iter, 2)
        
        #Check if it is in set:  |z| <= 2
        if (j == max_iter):
            samples_in_set += 1
    
    fraction = samples_in_set/sample_size
    Approx_area = (X_UP - X_LB)*(Y_UP - Y_LB)*fraction
    return Approx_area 


def I_iter_worker(q, d, sample_size):
    print('hwwyo')
    while True:
        try:
            max_iter, i = q.get_nowait()
            print(max_iter, i)
        except queue.Empty:
            break

        Approx_area = Monte_carlo(sample_size = sample_size, max_iter = max_iter)
        d[i].append(Approx_area)

def S_iter_worker(q, d, max_iter):
    while True:
        try:
            sample_size, i = q.get_nowait()
        except queue.Empty:
            break
            
        Approx_area = Monte_carlo(sample_size = sample_size, max_iter = max_iter)
        d[i].append(Approx_area)          


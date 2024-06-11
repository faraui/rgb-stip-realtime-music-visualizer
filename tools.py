import numpy as np
import math

class DataBuffer:
    def __init__(self, n_windows, samples_per_window, dtype=np.float32):
        self.n_windows = n_windows
        self.samples_per_window = samples_per_window
        self.buffer = np.zeros(n_windows * samples_per_window, dtype=dtype)

    def append(self, window):
        self.buffer = np.concatenate((self.buffer[self.samples_per_window:], window))

    def get(self):
        return self.buffer

round_up_to_even = lambda x: int(math.ceil(x / 2.) * 2)

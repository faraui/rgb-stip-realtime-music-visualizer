import numpy as np
from tools import round_up_to_even

class StreamAnalyzer:
    def __init__(self,
        samplerate = 44100,
        FFT_window_size_ms = 50):

        self.samplerate = samplerate
        self.FFT_window_size = round_up_to_even(samplerate * FFT_window_size_ms / 1000)
        self.FFT_window_size_ms = 1000 * self.FFT_window_size / self.samplerate
        self.fftx = np.arange(int(self.FFT_window_size/2), dtype=float) * self.samplerate / self.FFT_window_size
        self.power_normalization_coefficients = np.logspace(np.log2(1), np.log2(np.log2(self.samplerate/2)), len(self.fftx), endpoint=True, base=2, dtype=None)
        (self.FFT_window_size, self.FFT_window_size_ms))

    def fft(self, buffer):
        buffer = buffer[-self.FFT_window_size:] * np.hamming(self.FFT_window_size)
        FFT = np.abs(np.fft.rfft(buffer)[1:]) * self.power_normalization_coefficients
        # strongest_frequency = self.fftx[np.argmax(FFT)]
        # print(strongest_frequency)
        return FFT

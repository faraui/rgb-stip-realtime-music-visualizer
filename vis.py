from rgb_strip import RGBStrip
from src.stream_analyzer import Stream_Analyzer
import time
import numpy as np

def main():
    led = RGBStrip('/dev/ttyUSB0')
    ear = Stream_Analyzer(
                    device = None,              # Pyaudio (portaudio) device index. Default: first mic input
                    rate   = None,              # Audio sample rate. None sets the default source settings
                    FFT_window_size_ms  = 60,   # Window size used for the FFT transform
                    updates_per_second  = 1000, # How often to read the audio stream for new data
                    smoothing_length_ms = 50,   # Apply some temporal smoothing to reduce noise
                    n_frequency_bins = 400,     # The FFT features are grouped in bins
                    visualize = True,           # Visualize the FFT features with PyGame
                    verbose   = False,          # Print running statistics (latency, FPS, ...)
                    height    = 450,            # Pixel height of the visualizer window
                    window_ratio = 24.0/9.0     # Float ratio of the visualizer window. e.g. 24/9
         )

    fps = 60  #How often to update the FFT features + display
    k_correction = 10.0
    calibration = (1.0, 1.0, 1.0)
    last_update = time.time()
    while True:
        if (time.time() - last_update) > (1./fps):
            last_update = time.time()
            raw_fftx, raw_fft, binned_fftx, binned_fft = ear.get_audio_features()

            r = np.mean(raw_fft[:133]) * k_correction
            g = np.mean(raw_fft[133:133*2]) * k_correction
            b = np.mean(raw_fft[133*2:]) * k_correction

            if r > 255.0: r = 255.0
            if g > 255.0: g = 255.0
            if b > 255.0: b = 255.0
            led.setColorRgb(
                int(r * calibration[0]),
                int(g * calibration[1]),
                int(b * calibration[2]) )
            if r == 255.0 or g == 255.0 or b == 255.0: print('0xFF')
        elif False:
            time.sleep(((1./fps)-(time.time()-last_update)) * 0.99)


if __name__ == '__main__':
    main()

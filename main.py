from rgb_strip import RGBStrip
from stream_reader import StreamReader
from stream_analyzer import StreamAnalyzer
import numpy as np
import time

led = RGBStrip('/dev/ttyUSB0')
reader = StreamReader(samplerate=44100)
analyzer = StreamAnalyzer(samplerate=44100, FFT_window_size_ms = 80)

low_to_mid_f = (np.abs(analyzer.fftx - 200)).argmin()
mid_to_high_f = (np.abs(analyzer.fftx - 3000)).argmin()
print('Colors scale [R G B]:', low_to_mid_f, mid_to_high_f, len(analyzer.fftx))

k_correction = 5.0
calibration = (1.0, 1.0, 1.0)

def led_show(fft):
    r = np.mean(fft[:low_to_mid_f]) * k_correction
    g = np.mean(fft[low_to_mid_f:mid_to_high_f]) * k_correction
    b = np.mean(fft[mid_to_high_f:]) * k_correction

    if r > 255.0: r = 255.0
    if g > 255.0: g = 255.0
    if b > 255.0: b = 255.0
    if r == 255.0 or g == 255.0 or b == 255.0: print('0xFF overflow')
    led.setColorRgb(
        int(r * calibration[0]),
        int(g * calibration[1]),
        int(b * calibration[2]) )
    # led.setColorRgb(
    #     int(b * calibration[2]),
    #     int(r * calibration[0]),
    #     int(g * calibration[1]) )

fps = 30
def main():
    reader.start_stream()
    while True:
        start_time = time.time()
        led_show(analyzer.fft(reader.read()))
        time_delta = time.time() - start_time
        time.sleep(1. / fps - time_delta)
        FPS counter:
        print('%d.2 fps' % (1 / (time.time() - start_time)))

if __name__ == '__main__':
    main()

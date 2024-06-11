import numpy as np
import sounddevice as sd
from tools import DataBuffer, round_up_to_even
import math, time

class StreamReader:
    def __init__(self,
        device = None,
        samplerate = 44100,
        ups = 1000, # updates per second
        dtype=np.float32):

        print("Available audio devices:")
        device_dict = sd.query_devices()
        print(device_dict)

        self.dtype = dtype
        self.samplerate = samplerate
        self.blocksize = math.ceil(samplerate / ups / 2) * 2
        self.ups = self.samplerate / self.blocksize
        self.stream = sd.InputStream(
                                    samplerate = samplerate,
                                    blocksize = round_up_to_even(samplerate / ups),
                                    device=device,
                                    channels=1,
                                    dtype=dtype,
                                    latency='low',
                                    extra_settings=None,
                                    callback=self.on_stream_update)
        self.device = self.stream.device
        self.device_latency = device_dict[self.device]['default_low_input_latency']

        print("\n##################################################################################################")
        print("\nDefaulted to using first working mic, Running on mic %s with properties:" %str(self.device))
        print(device_dict[self.device])
        print('Which has a latency of %.2f ms' %(1000*self.device_latency))
        print("\n##################################################################################################")
        print('Recording audio at %d Hz\nUsing (non-overlapping) data-windows of %d samples (updating at %.2ffps)'
                    %(self.samplerate, self.blocksize, self.ups))

    def on_stream_update(self, indata, frames, timestamp, status):
        if status: print(status)
        self.data_buffer.append(indata[:,0])

    def read(self, n = None):
        # return self.data_buffer.buffer[-n:] if n else self.data_buffer.buffer
        return self.data_buffer.buffer

    def start_stream(self, buffer_size=None):
        self.n_windows = buffer_size if buffer_size else int(self.ups / 2)
        self.data_buffer = DataBuffer(self.n_windows, self.blocksize, dtype=self.dtype)

        print("\n--🎙  -- Starting live audio stream...\n")
        self.stream.start()
        self.stream_start_time = time.time()

    def stop_stream(self):
        print("👋  Sending stream termination command...")
        self.stream.stop()

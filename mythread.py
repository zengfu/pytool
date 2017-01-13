import threading
import time
import wave
import pyaudio
import numpy as np
import queue
from scipy import fftpack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
voice=queue.Queue()
display=queue.Queue()
'''
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
'''
wf = wave.open('4.wav', 'rb')
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

length=4096
class geti2s(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("* recoding")
        while True:
            #data = stream.read(CHUNK)
            data=wf.readframes(CHUNK)
            voice.put(data)
            stream.write(data, CHUNK)
class handle(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while True:
            data=voice.get()
            raw_data=np.frombuffer(data,np.dtype('<i2'))
            raw_data=raw_data*np.hanning(raw_data.size)
            fft_complex=fftpack.fft(raw_data,length)
            fft_data=np.abs(fft_complex)[0:length/4]
            display.put_nowait(fft_data)
            #print fft_data.size

fig, ax = plt.subplots()
line, = ax.plot(np.random.rand(length/4))
ax.set_ylim(0,5000000)
def update(data):
    line.set_ydata(data)
    return line,

def data_gen():
    while True:
        #yield np.arange(513)
        if display.empty():
            yield np.zeros(length/4)
        else:
            while not display.empty():
                data=display.get()
            yield data

class plot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass



t1=geti2s()
t1.setDaemon(True)
t1.start()
t3=handle()
t3.setDaemon(True)
t3.start()
ani = animation.FuncAnimation(fig, update, data_gen, interval=50)
plt.show()


    #raw_data = np.frombuffer(data, np.dtype('<i2'))
    #stream.write(data, CHUNK)

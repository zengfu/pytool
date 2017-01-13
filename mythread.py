import threading
import time
import pyaudio
import numpy as np
import queue
from scipy import fftpack
from matplotlib import animation,pyplot
CHUNK = 1024
WIDTH = 2
CHANNELS = 1
RATE = 44100
p = pyaudio.PyAudio()
voice=queue.Queue()
display=queue.Queue(maxsize=1)
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)


class geti2s(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("* recoding")
        while True:
            data = stream.read(CHUNK)
            voice.put(data)
            stream.write(data, CHUNK)
class handle(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        data=voice.get()
        raw_data=np.frombuffer(data,np.dtype('<i2'))
        fft_complex=fftpack.fft(raw_data)
        fft_data=np.abs(fft_complex)[0:fft_complex.size/2+1]
        display.put_nowait(fft_data)


fig,ax=pyplot.subplots()
line, = ax.plot(np.ones(10),'-r')

def update(data):
    line.set_ydata(data)
    return line,

def data_gen():
    while True:
        #if display.empty():
        yield np.random.rand(10)
        #else:
        #    yield display.get_nowait()

class plot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pass



t1=geti2s()
t1.setDaemon(True)
t1.start()
t2=plot()
t2.setDaemon(True)
t2.start()
t3=handle()
t3.setDaemon(True)
t3.start()
ani = animation.FuncAnimation(fig, update, data_gen, interval=100)
pyplot.show()

    #raw_data = np.frombuffer(data, np.dtype('<i2'))
    #stream.write(data, CHUNK)

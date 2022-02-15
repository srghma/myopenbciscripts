import math

import pythonosc
from pythonosc import dispatcher
from pythonosc import osc_server
import inspect
import sys
import soothingsounds as ss

from array import array

nbitfile = 16
nbitfloat = 32  # from generator.py
fs = 16000
nsec = 60
nmode = "pink"

samps = ss.computenoise(nmode, fs, nsec, nbitfloat, nbitfile)
m = ss.liveplay(samps, -1, fs, nsec)

# m = pygame.mixer.music
# # m.load(r"./e-flat-tibetan-singing-bowl-struck.wav")
# # m.load(r"./rain.mp3")
# m.play(-1)

def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

last_volume = 0.1
def print_volume_handler(address, volume):
    volume = clamp(volume, 0.0, 1.0)

    global last_volume
    if last_volume == volume:
        return
    last_volume = volume
    print("[Volume] ~ {0}".format(volume))

    volume = 1.0 - volume
    volume = 0.0 if volume < 0.4 else volume

    m.set_volume(volume)

dispatcher = pythonosc.dispatcher.Dispatcher()
dispatcher.map("/feedback/0", print_volume_handler)

server = pythonosc.osc_server.ThreadingOSCUDPServer(("127.0.0.1", 4546), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

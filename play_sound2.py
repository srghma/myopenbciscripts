import math

import pythonosc
from pythonosc import dispatcher
from pythonosc import osc_server
import inspect
import sys
import soothingsounds as ss
import pygame
import pygame.midi
import numpy as np
from pygame.mixer import Sound, get_init, pre_init

from array import array

nbitfile = 16
nbitfloat = 32  # from generator.py
fs = 16000
nsec = 60

pygame.mixer.pre_init(fs, channels=1)
pygame.mixer.init()

# sound = pygame.mixer.Sound('pinknoise.wav')

# channel0 = pygame.mixer.Channel(0)
# channel0.play(sound)
# channel0.set_volume(1.0, 0.0)

# channel1 = pygame.mixer.Channel(1)
# channel1.play(sound)
# channel1.set_volume(0.0, 1.0)

# pygame.midi.init()

# sound_data  = ss.computenoise("pink", fs, nsec, nbitfloat, nbitfile)
# sound_data  = sound_data.reshape(480000, 2)

sound = pygame.mixer.Sound('pinknoise.wav')
sound.play(-1)
sound.set_volume(0.5)

# class Note(Sound):
#     def __init__(self, frequency, volume=.1):
#         self.frequency = frequency
#         Sound.__init__(self, self.build_samples())
#         self.set_volume(volume)
#     def build_samples(self):
#         period = int(round(get_init()[0] / self.frequency))
#         samples = array("h", [0] * period)
#         amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
#         amplitude = int(amplitude / 20)
#         for time in range(period):
#             if time < period / 2:
#                 samples[time] = amplitude
#             else:
#                 samples[time] = -amplitude
#         return samples

# sound1 = Note(440)

# sound1 = pygame.mixer.Sound('main-birds.wav')
sound1 = pygame.mixer.Sound('main-crickets.wav')
sound1.play(-1)
sound1.set_volume(1.0)

# full time is 58.123
# ffmpeg -i main-crickets.mp4 -ac 2 -f wav -ss 1 -t 56 main-crickets.wav

def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

def print_volume_handler(channel, is_0):
    last_volume = 0.1

    def print_volume_handler_x(address, volume):
        volume = clamp(volume, 0.0, 1.0)

        nonlocal last_volume
        if last_volume == volume:
            return
        print("input_v={0}, channel_v={1}, last_v={2}".format(volume, channel.get_volume(), last_volume))
        last_volume = volume

        volume = 1.0 - volume
        volume = 0.0 if volume < 0.2 else volume

        # if is_0:
        #     volume = volume / 2

        channel.set_volume(volume)

    return print_volume_handler_x

fn0 = print_volume_handler(sound, True)
fn1 = print_volume_handler(sound1, False)
dispatcher = pythonosc.dispatcher.Dispatcher()
dispatcher.map("/feedback/0", fn0)
dispatcher.map("/feedback/1", fn1)

server = pythonosc.osc_server.ThreadingOSCUDPServer(("127.0.0.1", 4546), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

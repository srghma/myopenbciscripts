import math

import pythonosc
from pythonosc import dispatcher
from pythonosc import osc_server
import inspect
import sys
import soothingsounds as ss
import pygame

from array import array

nbitfile = 16
nbitfloat = 32  # from generator.py
fs = 16000
nsec = 60

# m = ss.liveplay(samps, fs, nsec)

pygame.mixer.pre_init(fs, channels=2)
pygame.mixer.init()

sound = pygame.mixer.Sound('pinknoise.wav')

channel0 = pygame.mixer.Channel(0)
channel0.play(sound)
channel0.set_volume(1.0, 0.0)

channel1 = pygame.mixer.Channel(1)
channel1.play(sound)
channel1.set_volume(0.0, 1.0)

# sound_data  = ss.computenoise("pink", fs, nsec, nbitfloat, nbitfile)
# sound_data  = sound_data.reshape(480000, 2)

# channel0 = pygame.mixer.Channel(0)
# channel1 = pygame.mixer.Channel(1)

# sound  = pygame.sndarray.make_sound(sound_data)

# channel0.play(sound, -1)
# channel1.play(sound, -1)

# channel0.set_volume(1.0, 0.0)
# channel1.set_volume(0.0, 1.0)

# sound_0 = pygame.sndarray.make_sound(sound_data)
# sound_1 = pygame.sndarray.make_sound(sound_data)
# music_0 = sound_0.play(-1)
# music_1 = sound_1.play(-1)
# print("pygame volume level: " + str(sound.get_volume()))

# print("pygame volume level: " + str(pygame.mixer.get_num_channels()))

# m = pygame.mixer.music
# # m.load(r"./e-flat-tibetan-singing-bowl-struck.wav")
# # m.load(r"./rain.mp3")
# m.play(-1)

# music_0.set_volume(1.0, 0.0)
# music_1.set_volume(0.0, 0.0)

#from pydub import AudioSegment
#from pydub.playback import play

#song = AudioSegment.from_wav("pinknoise.wav")

## pan the sound 15% to the right
#panned_right = song.pan(+0.15)

## pan the sound 50% to the left
#panned_left = song.pan(-0.50)

##Play panned left audio
#while True:
#    try:
#        play(panned_left)
#    except KeyboardInterrupt:
#        print("Stopping playing")
#        break

def clamp(val, min_, max_):
    return min_ if val < min_ else max_ if val > max_ else val

def print_volume_handler(channel, is_left):
    last_volume = 0.1

    def print_volume_handler_x(address, volume):
        volume = clamp(volume, 0.0, 1.0)

        nonlocal last_volume
        if last_volume == volume:
            return
        print("is_left={0}, input_v={1}, channel_v={2}, last_v={3}".format(is_left, volume, channel.get_volume(), last_volume))
        last_volume = volume

        volume = 1.0 - volume
        volume = 0.0 if volume < 0.4 else volume

        if is_left:
            channel.set_volume(volume, 0.0)
        else:
            channel.set_volume(0.0, volume)

    return print_volume_handler_x

fn0 = print_volume_handler(channel0, True)
fn1 = print_volume_handler(channel1, False)
dispatcher = pythonosc.dispatcher.Dispatcher()
dispatcher.map("/feedback/0", fn0)
dispatcher.map("/feedback/1", fn1)

server = pythonosc.osc_server.ThreadingOSCUDPServer(("127.0.0.1", 4546), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

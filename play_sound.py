import math

import pythonosc
from pythonosc import dispatcher
from pythonosc import osc_server
import pygame
import inspect
import sys

last_volume = 0.1

pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\srghma\Documents\rain.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

def clamp(val, min_, max_):
  return min_ if val < min_ else max_ if val > max_ else val

def print_volume_handler(address, volume):
  volume = clamp(volume, 0.0, 1.0)

  if last_volume == volume:
    return
  last_volume = volume

  # print("[Volume] ~ {0}".format(volume))

  volume = 1.0 - volume
  volume = 0.0 if volume < 0.4 else volume

  pygame.mixer.music.set_volume(volume)

dispatcher = pythonosc.dispatcher.Dispatcher()
dispatcher.map("/feedback", print_volume_handler)

server = pythonosc.osc_server.ThreadingOSCUDPServer(("127.0.0.1", 4546), dispatcher)
print("Serving on {}".format(server.server_address))
server.serve_forever()

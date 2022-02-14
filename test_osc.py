import argparse
import random
import time
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 4546)

for x in range(4):
  client.send_message("/feedback/1", random.random())
  time.sleep(1)

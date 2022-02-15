import numpy as np
import pygame
import logging
from time import time
from typing import Any
#
from .generator import noise




def computenoise(
    ntype: str, fs: int, nsec: int, nbitfloat: int, nbitfile: int, verbose: bool = False
) -> np.ndarray:
    nsamp = int(fs * nsec)
    ramused = (
        nsamp * nbitfloat // 8
    )  # bytes, assuming np.float32, does NOT account for copies!
    if ramused > 128e6:
        logging.warning(
            f"using more than {ramused//1e6:d} MB of RAM for samples, this can be too much for Raspi."
        )


    rawused = ramused // (nbitfloat // nbitfile)
    if rawused > 1e9:
        logging.warning(f"your raw output is {rawused/1e9:.1f} GB of data.")


    print(f"sound samples used at least {ramused//1e6:.0f} MB of RAM to create.")


    ntype = ntype.lower()
    tic = time()
    # TODO arbitary scaling to 16-bit, noise() outputs float64
    samps = (noise(nsamp, color=ntype) * 32768 / 8).astype(np.int16)

    if verbose:
        print(
            f"it took {time()-tic:.2f} seconds to compute {nsec:.0f} sec. of {ntype:s} noise."
        )

    return samps

def liveplay(
    samps: np.ndarray, nhours: int, fs: int, nsec: int
):
    pygame.mixer.pre_init(fs, size=-16, channels=1)
    pygame.mixer.init()
    sound = pygame.sndarray.make_sound(samps)
    sound.play(-1)
    print("pygame volume level: " + str(sound.get_volume()))

    return sound

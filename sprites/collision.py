import numpy as np
import pygame

import matplotlib.pyplot as plt
from sprites.base import SpriteBase


def detect_collision_by_alpha_channel(a: SpriteBase, b: SpriteBase, screen: pygame.Surface, plot_mask: bool = False):
    screen_size = screen.get_size()
    mask_a = a.get_screen_mask(screen_size)
    mask_b = b.get_screen_mask(screen_size)

    if plot_mask:
        plt.imshow(np.transpose(mask_a & mask_b), cmap="gray")
        plt.pause(0.0000001)
        plt.clf()

    if (mask_a & mask_b).any():
        return True
    return False

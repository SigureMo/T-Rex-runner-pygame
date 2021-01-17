import math

import pygame

from speed import Speed


class Desert:
    def __init__(self, image: pygame.Surface, speed: Speed) -> None:
        self.image = image
        self.speed = speed
        self.pos_x = 0.0

    def update(self, screen: pygame.Surface) -> None:
        w_screen, h_screen = screen.get_size()
        w_image, h_image = self.image.get_size()
        self.pos_x -= self.speed.value
        self.pos_x %= w_image

        # 计算当前屏幕需要几张背景才能全覆盖
        n_images = math.ceil(w_screen / w_image) + 1
        screen.fill((255, 255, 255))
        for i in range(n_images):
            x = self.pos_x % w_image + w_image * (i - 1)
            y = h_screen - h_image
            screen.blit(self.image, (x, y))


class Cloud:
    def __init__(self, image: pygame.Surface, x: int, y: int, speed: Speed) -> None:
        self.image = image
        self.speed = speed
        self.x = x
        self.y = y

    def update(self, screen: pygame.Surface) -> None:
        w_screen, h_screen = screen.get_size()
        w_image, h_image = self.image.get_size()
        self.x -= self.speed.value
        self.x %= w_screen + w_image
        screen.blit(self.image, (self.x - w_image, self.y))

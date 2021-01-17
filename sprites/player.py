from enum import Enum

import pygame


class Dinosaur(pygame.sprite.Sprite):
    def __init__(self, images: list[pygame.Surface]) -> None:
        super().__init__()
        self.images = images
        self.index = 0
        self.jumping_index = 0
        self.num_shift = 6
        self.status = DinosaurStatus.RUNNING

    @property
    def image(self) -> pygame.Surface:
        img: pygame.Surface
        if self.status == DinosaurStatus.CREEPING:
            img = self.images[2 + self.index // self.num_shift]
        else:
            img = self.images[self.index // self.num_shift]
        return img

    @staticmethod
    def jumping_height(t: float) -> float:
        t *= 0.01
        return 1000 * (t - 2 * t ** 2)

    def handle_event(self, pressed_keys: pygame.key.ScancodeWrapper) -> None:
        if self.status != DinosaurStatus.JUMPING:
            self.status = DinosaurStatus.RUNNING
            if pressed_keys[pygame.K_UP]:
                self.status = DinosaurStatus.JUMPING
            elif pressed_keys[pygame.K_DOWN]:
                self.status = DinosaurStatus.CREEPING

    def update(self, screen: pygame.Surface) -> None:
        w_screen, h_screen = screen.get_size()
        w_image, h_image = self.image.get_size()

        if self.status != DinosaurStatus.JUMPING:
            self.index += 1
            self.index %= self.num_shift * 2
        else:
            self.jumping_index += 1
            if Dinosaur.jumping_height(self.jumping_index) < 0:
                self.jumping_index = 0
                self.status = DinosaurStatus.RUNNING

        x = 20
        if self.status == DinosaurStatus.JUMPING:
            y = h_screen - h_image - Dinosaur.jumping_height(self.jumping_index)
        else:
            y = h_screen - h_image
        screen.blit(self.image, (x, y))


class DinosaurStatus(Enum):
    RUNNING = 0
    JUMPING = 1
    CREEPING = 2
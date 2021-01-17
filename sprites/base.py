import pygame


class SpriteBase(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

    def render(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))

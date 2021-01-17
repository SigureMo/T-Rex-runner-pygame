import math
import random
import pygame
import numpy as np
import matplotlib.pyplot as plt

from backgroud import Cloud, Desert
from events import ADD_ENEMY
from sprites.enemies import Pterodactyl, Cactus
from sprites.player import Dinosaur
from speed import Speed, SpeedRatio

assets_paths = {
    "desert": "./images/desert.png",
    "cloud": "./images/cloud.png",
    "cactuses": [
        "./images/cactus/cactus_1.png",
        "./images/cactus/cactus_2.png",
        "./images/cactus/cactus_3.png",
        "./images/cactus/cactus_4.png",
        "./images/cactus/cactus_5.png",
        "./images/cactus/cactus_6.png",
        "./images/cactus/cactus_7.png",
    ],
    "pterodactyl": [
        "./images/pterodactyl/pterodactyl_1.png",
        "./images/pterodactyl/pterodactyl_2.png",
    ],
    "dinosaur": [
        "./images/dinosaur/standing_1.png",
        "./images/dinosaur/standing_2.png",
        "./images/dinosaur/creeping_1.png",
        "./images/dinosaur/creeping_2.png",
    ],
}


def main():
    pygame.init()
    pygame.display.set_caption("T-Rex Pygame")
    size = (1000, 350)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    score = 0.0
    speed_ratio = SpeedRatio()
    background_speed = Speed(8.0, speed_ratio)
    cloud_speed = Speed(1.0, speed_ratio)

    desert_image = pygame.image.load(assets_paths["desert"])
    cloud_image = pygame.image.load(assets_paths["cloud"])
    cactus_images = [pygame.image.load(img_path) for img_path in assets_paths["cactuses"]]
    pterodactyl_images = [pygame.image.load(img_path) for img_path in assets_paths["pterodactyl"]]
    dinosaur_images = [pygame.image.load(img_path) for img_path in assets_paths["dinosaur"]]

    desert = Desert(desert_image, speed=background_speed)
    clouds = [
        Cloud(cloud_image, 10, 50, speed=cloud_speed),
        Cloud(cloud_image, 500, 70, speed=cloud_speed),
    ]
    dinosaur = Dinosaur(dinosaur_images)
    enemies = pygame.sprite.Group()
    enemies.add(Cactus(cactus_images[0], speed=background_speed))

    # print(pygame.surfarray.array_alpha(cactus_images[0]))

    done = False
    while not done:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.QUIT:
                done = True
            elif event.type == ADD_ENEMY:
                if score > 1000 and random.random() < 0.2:
                    enemies.add(Pterodactyl(pterodactyl_images, speed=background_speed))
                else:
                    cactus_image = random.choice(cactus_images)
                    enemies.add(Cactus(cactus_image, speed=background_speed))

        # print(type(pressed_keys))
        speed_ratio.update()
        score += background_speed.value * 0.1
        # print(speed_ratio.value)

        desert.update(screen)
        for enemy in enemies:
            enemy.update(screen)
        for cloud in clouds:
            cloud.update(screen)
        dinosaur.update(screen)
        pressed_keys = pygame.key.get_pressed()
        dinosaur.handle_event(pressed_keys)

        pygame.display.flip()


if __name__ == "__main__":
    main()
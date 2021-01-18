import random

import pygame

from backgroud import Cloud, Desert, Score
from events import ADD_ENEMY
from sprites.enemies import Pterodactyl, Cactus
from sprites.player import TRex
from sprites.collision import detect_collision_by_alpha_channel
from speed import Speed, SpeedRatio
from gameover import GameOver

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
        "./images/t-rex/standing_1.png",
        "./images/t-rex/standing_2.png",
        "./images/t-rex/creeping_1.png",
        "./images/t-rex/creeping_2.png",
    ],
    "gameover": "./images/gameover.png",
    "restart": "./images/restart.png",
    "font": "./fonts/DinkieBitmap-7pxDemo.ttf",
}


def main():
    pygame.init()
    pygame.display.set_caption("T-Rex Runner Pygame")
    screen_size = (1000, 350)
    fps = 60
    screen = pygame.display.set_mode(screen_size)
    screen.fill((255, 255, 255))
    clock = pygame.time.Clock()

    # score = 0.0
    speed_ratio = SpeedRatio()
    background_speed = Speed(8.0, speed_ratio)
    cloud_speed = Speed(1.0, speed_ratio)

    desert_image = pygame.image.load(assets_paths["desert"])
    cloud_image = pygame.image.load(assets_paths["cloud"])
    cactus_images = [pygame.image.load(img_path) for img_path in assets_paths["cactuses"]]
    pterodactyl_images = [pygame.image.load(img_path) for img_path in assets_paths["pterodactyl"]]
    dinosaur_images = [pygame.image.load(img_path) for img_path in assets_paths["dinosaur"]]
    gameover_image = pygame.image.load(assets_paths["gameover"])
    restart_image = pygame.image.load(assets_paths["restart"])

    desert = Desert(desert_image, speed=background_speed)
    clouds = [
        Cloud(cloud_image, 10, 50, speed=cloud_speed),
        Cloud(cloud_image, 500, 70, speed=cloud_speed),
    ]
    t_rex = TRex(dinosaur_images)
    enemies = pygame.sprite.Group()
    enemies.add(Cactus(cactus_images[0], speed=background_speed))
    score = Score(font=pygame.font.Font(assets_paths["font"], 30), speed=background_speed)
    gameover = GameOver(gameover_image, restart_image)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            elif event.type == pygame.QUIT:
                done = True
            elif event.type == ADD_ENEMY:
                if score.value > 100 and random.random() < 0.2:
                    enemies.add(Pterodactyl(pterodactyl_images, speed=background_speed))
                else:
                    cactus_image = random.choice(cactus_images)
                    enemies.add(Cactus(cactus_image, speed=background_speed))

        if gameover.is_gameover:
            gameover.update(screen)
            pressed_keys = pygame.key.get_pressed()
            gameover.handle_events(pressed_keys)
            # 开始新游戏
            if not gameover.is_gameover:
                for enemy in enemies:
                    enemy.kill()
                enemies.add(Cactus(cactus_images[0], speed=background_speed))
                score.clear()
                speed_ratio.reset()
        else:
            speed_ratio.update()

            desert.update(screen)
            for enemy in enemies:
                enemy.update(screen)
            for cloud in clouds:
                cloud.update(screen)
            t_rex.update(screen)
            score.update(screen)
            pressed_keys = pygame.key.get_pressed()
            t_rex.handle_events(pressed_keys)

            for enemy in enemies:
                if detect_collision_by_alpha_channel(t_rex, enemy, screen, plot_mask=False):
                    gameover.is_gameover = True
                    break

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()

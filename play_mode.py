import random

from pico2d import *
import game_framework

import game_world
from grass import Grass
from boy import Boy
from ball import Ball
from zombie import Zombie


# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy
    global balls, ball
    global zombies, zombie
    balls = [Ball(random.randint(100, 1600 - 100), 60, 0) for _ in range(30)]
    game_world.add_objects(balls, 1)
    for ball in balls:
        game_world.add_collision_pair('boy:ball', None, ball)
        game_world.add_collision_pair('zombie:ball', None, ball)
        game_world.add_collision_pair('ball:zombie', ball, None)

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 1)
    game_world.add_collision_pair('boy:ball', boy, None)
    game_world.add_collision_pair('boy:zombie', boy, None)
    zombies = [Zombie() for _ in range(5)]
    game_world.add_objects(zombies, 1)
    for zombie in zombies:
        game_world.add_collision_pair('zombie:ball', zombie, None)
        game_world.add_collision_pair('boy:zombie', None, zombie)
        game_world.add_collision_pair('ball:zombie', None, zombie)

    #
    # game_world.add_collision_pair('zombie:ball', None, ball)
    # game_world.add_collision_pair('zombie:ball', zombie, ball)
    # fill here

def finish():

    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    if boy not in game_world.world[1]:
        print('boy 사망!!!!!')
        game_framework.quit()  # boy가 삭제된 경우 즉시 종료

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass

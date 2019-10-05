import gym
from gym import spaces
from components import Palette, Unit
import numpy as np

import pyglet
import time
from pyglet.window import key
import random
from math import sqrt


# python -m baselines.run --alg=ppo2 --env=single_demo_env --num_timesteps=2e7 --save_path=~/Projects/LogisticGym/models/single_ppo_092901 --log_path=~/Projects/LogisticGym/models/single_ppo_092901
# python -m baselines.run --alg=ppo2 --env=obstacle_demo_env --num_timesteps=2e7 --save_path=models/obstacle_ppo_100401 --log_path=logs/obstacle_ppo_100401
# python -m baselines.run --alg=ppo2 --env=single_demo_env --num_timesteps=0 --load_path=models/single_ppo_092902 --play
num_obstacles = 1
num_palettes = 1

game_windows = []
for _ in range(num_palettes):
    game_windows.append(pyglet.window.Window(800, 600))



class DemoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.display = True
        if self.display:
            self.game_windows = game_windows
            self.main_batch = pyglet.graphics.Batch()
            self.SCALE = 100

        else:
            self.game_window = None
            self.main_batch = None
            self.viewer = None
            self.SCALE = 1
        self.k_action = 0

        self.units_x = np.array([2, 3, 4, 5, 6, 4, 5]) * self.SCALE
        self.units_y = np.array([3, 3, 3, 3, 3, 2, 2]) * self.SCALE

        self.num_steps = 0
        self.max_steps = 200

        self.units = []
        self.palettes = []
        self.obstacles = []
        self.num_obstacles = num_obstacles
        self.num_palettes = num_palettes
        self.num_inspector = 2
        self.num_normal_units = len(self.units_x) - self.num_inspector
        self.action_space = spaces.Discrete(len(self.units_x))
        # obs = [on_unit, palette.is_moving, palette.inspected, palette.sprite.x, palette.sprite.y, palet]

        low = np.array([0, 0, 0, 0, 2, 5])
        high = np.array([6, 1, 1, 5, 3, 10])
        obs_box = spaces.Box(low=low, high=high)
        self.observation_space = obs_box

        for i in range(self.num_palettes):
            self.palettes.append(Palette(self.units_x[0], self.units_y[0], image_name="palette.png", batch=self.main_batch))

        for i in range(self.num_obstacles):
            self.obstacles.append(Palette(self.units_x[0], self.units_y[0], image_name="obstacle.png", is_obstacle=True, batch=self.main_batch))

        for i in range(len(self.units_x)):
            is_inspector = (i >= self.num_normal_units)
            new_unit = Unit(self.units_x[i], self.units_y[i], is_inspector, batch=self.main_batch)
            self.units.append(new_unit)

        self.done = False

        self.keyboard_actions = [0 for _ in range(self.num_obstacles + self.num_palettes)]

    def reset(self):
        self.done = False
        self.keyboard_actions = []
        self.num_steps = 0
        for p in self.palettes:
            p.reset(self.units_x[0], self.units_y[0])

        # obs = [on_unit, palette.is_moving, palette.inspected, palette.sprite.x, palette.sprite.y]

        self.keyboard_actions = [0 for _ in range(self.num_obstacles + self.num_palettes)]
        state = [0, 0, 0, self.units_x[0], self.units_y[0], self.palettes[0].inspection_time]

        return np.array(state)

    def step(self, action):

        #action = [action]
        reward = 0

        ############# move #############
        for i in range(self.num_palettes + self.num_obstacles):
            palette = (self.palettes + self.obstacles)[i]
            # destination = action[i]
            on_unit = palette.on_unit(self.units)

            if palette.is_obstacle:
                '''
                if palette.inspected:
                    if random.random() > 0.95:
                        destination = 4
                    else:
                        destination = on_unit
                elif on_unit == 5 or on_unit == 6:
                    if palette.inspected:
                        if random.random() > 0.95:
                            destination = 4
                        else:
                            destination = on_unit
                else:
                    destination = random.randint(5, 6)
                '''
                destination = random.randint(0, 6)

                # print(destination, palette.inspected)

            else:
                destination = action[i]

            palette.set_destination(self, destination)


            # print("x: {} y: {}".format(palette.sprite.x, palette.sprite.y))

            palette.prev_move = [0, 0]
            if palette.intersection_check:
                sign = int(np.sign(on_unit - palette.destination))
                palette.sprite.y += sign * 0.2 * self.SCALE
                palette.prev_move[1] = sign * 0.2 * self.SCALE

                if sign == 0:
                    palette.act_gravity(self.units, False)

            else:
                sign = int(np.sign(palette.intersection - on_unit))
                palette.sprite.x += sign * 0.2 * self.SCALE
                palette.prev_move[0] = sign * 0.2 * self.SCALE

                if sign == 0:
                    palette.act_gravity(self.units, True)
                    palette.intersection_check = True

            #########################################

            ############### check collision #########

            for p in (self.palettes + self.obstacles):
                col = self.check_collision(palette, p)
                if col:

                    p.move_back(self.units)
                    p.is_moving = False
                    reward -= 1




            if (on_unit == 5 or on_unit == 6) and (not palette.is_moving):
                if destination == on_unit:
                    # print("inspecting..", palette.inspection_time)
                    palette.inspection_time -= 1
                    if palette.inspection_time <= 0:
                        palette.inspection_time = 0
                        palette.inspected = 1
                        print("inspection done!!!!!")

            elif on_unit == 4 and (not palette.is_moving):
                if palette.inspected:
                    reward += 100
                    print("success!!")
                else:
                    reward -= 10
                    print("fail!!")
                palette.reset(self.units_x[0], self.units_y[0])

            self.num_steps += 1
            if self.num_steps > self.max_steps:
                self.done = True

            if not palette.is_obstacle:
                    obs = np.array([on_unit, palette.is_moving, palette.inspected, palette.sprite.x / self.SCALE, palette.sprite.y / self.SCALE, palette.inspection_time])

        return obs, reward, self.done, {}

    def render(self, mode='human'):

        if self.display:
            pyglet.clock.tick()
            for i, game_window in enumerate(game_windows):
                game_window.switch_to()
                game_window.dispatch_events()
                game_window.dispatch_event('on_draw')
                # game_window.dispatch_event('on_key_press')
                game_window.flip()
                time.sleep(0.1)


    def check_collision(self, p1, p2):

        if (p1 == p2) or p1.on_unit(self.units) == 0 or p2.on_unit(self.units) == 0:
            return False

        delta_x = abs(p2.sprite.x - p1.sprite.x)
        delta_y = abs(p2.sprite.y - p1.sprite.y)
        distance = sqrt(delta_x**2 + delta_y**2)

        collide = (distance < p1.size()[0] + p2.size()[0])
        if collide:
            print("collide!")


        return collide


if __name__ == '__main__':
    env = DemoEnv()
    obs = env.reset()

    for i, game_window in enumerate(game_windows):
        @game_window.event
        def on_draw():
            game_window.clear()
            for p in (env.palettes + env.obstacles):
                p.sprite.draw()

            for u in env.units:
                u.sprite.draw()

        @game_window.event
        def on_key_press(symbol, modifiers):
            comps = env.palettes + env.obstacles
            p = comps[0]

            if symbol == key.LEFT:
                p.sprite.x -= 20
            elif symbol == key.RIGHT:
                p.sprite.x += 20
            elif symbol == key.UP:
                p.sprite.y += 20
            elif symbol == key.DOWN:
                p.sprite.y -= 20

            if 65455 < symbol < 65466:  # Num 0 to 9
                k = symbol - 65456
                p.k_action = k
                env.keyboard_actions[0] = k
            elif 96 < symbol < 104:
                p.k_action = symbol - 97



    while True:
        a = random.randint(5, 6)

        obs, rewards, done, info = env.step([env.keyboard_actions[0], a])
        # pyglet.clock.tick()
        # game_window.switch_to()
        # game_window.dispatch_events()
        # game_window.dispatch_event('on_draw')
        # game_window.flip()
        env.render()

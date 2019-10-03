import pyglet
import random
import numpy as np

# pyglet.resource.path = ["/Users/ichangmin/PycharmProjects/LogisticEnv/resources"]
pyglet.resource.path = ["/home/changmin/Projects/LogisticGym/resources"]


def resize_image(image, size=(50, 50)):
    width = size[0]
    height = size[1]

    image.width = width
    image.height = height

    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


class Palette:
    all = []
    id = 0

    def __init__(self, pos_x, pos_y, batch=None):
        self.id = Palette.id
        Palette.id += 1

        image = pyglet.resource.image("palette.png")
        resize_image(image, (50, 50))

        self.sprite = pyglet.sprite.Sprite(image, x=pos_x, y=pos_y, batch=batch)
        self.inspected = False
        self.destination = 0
        self.intersection = 0
        self.intersection_check = True
        self.is_moving = False
        self.inspection_time = random.randint(6, 10)
        self.prev_move = [0., 0.]

        Palette.all.append(self)

    def reset(self, pos_x, pos_y):
        self.sprite.x = pos_x
        self.sprite.y = pos_y
        self.inspected = False
        self.destination = 0
        self.intersection = 0
        self.intersection_check = True
        self.is_moving = False
        self.inspection_time = random.randint(6, 10)
        self.prev_move = [0., 0.]


    def act_gravity(self, units, is_moving):
        on_unit = self.on_unit(units)
        self.sprite.x = units[on_unit].sprite.x
        self.sprite.y = units[on_unit].sprite.y

        self.is_moving = is_moving

    def move(self, x, y):
        self.sprite.x += x
        self.sprite.y += y

    def on_unit(self, units):
        min_distance = 1000
        min_unit = 0
        for i, unit in enumerate(units):
            unit_pos = np.array([unit.sprite.x, unit.sprite.y])
            palette_pos = np.array([self.sprite.x, self.sprite.y])
            distance = np.sqrt(np.sum((np.square(unit_pos - palette_pos))))
            if distance < min_distance:
                min_distance = distance
                min_unit = i

        return min_unit

    def in_inspector(self, env):
        cur_unit = self.on_unit(env.units)
        num_normals = env.num_normal_units

        return cur_unit >= num_normals

    def set_destination(self, env, destination):
        if self.is_moving:
            return


        if self.in_inspector(env):
            self.intersection_check = True
            if destination != self.on_unit(env.units):
                self.destination = self.on_unit(env.units) - 3
        else:
            self.intersection_check = False
            self.destination = destination
            if destination >= env.num_normal_units:
                self.intersection = destination - 3
            else:
                self.intersection = destination
        self.is_moving = True



    # def go(self, destination):


class Unit:
    all = []
    id = 0

    def __init__(self, pos_x, pos_y, is_inspector=False, batch=None):
        self.id = Unit.id
        Unit.id += 1
        image = pyglet.resource.image("unit.png")
        resize_image(image, (10, 10))
        self.sprite = pyglet.sprite.Sprite(image, x=pos_x, y=pos_y, batch=batch)

        self.is_inspector = is_inspector

        Unit.all.append(self)


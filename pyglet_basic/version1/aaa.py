import pyglet
from pyglet.window import key
import random


game_window = pyglet.window.Window(800, 600)
pyglet.resource.path = ["../resources"]

def resize_image(image, width=50, height=50):
    image.width = width
    image.height = height

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2

def asterids(num_asteroids):
    asterids = []
    for i in range(num_asteroids):
        x = random.randint(0, 800)
        y = random.randint(0, 600)

        ast_image = pyglet.resource.image("asteroid.png")
        resize_image(ast_image)
        center_image(ast_image)
        new_astroid = pyglet.sprite.Sprite(ast_image, x=x, y=y)

        asterids.append(new_astroid)

    return asterids


astroid = asterids(1)[0]
# @game_window.event
# def on_key_press(symbol, modifiers):
#     if symbol == key.LEFT:
#         astroid.x -= 1
#     elif symbol == key.RIGHT:
#         astroid.x += 1
#     elif symbol == key.UP:
#         astroid.y += 1
#     elif symbol == key.DOWN:
#         astroid.y -= 1




@game_window.event
def on_draw():

    game_window.clear()
    # ast = asterids(5)
    # for a in ast:
    #     a.draw()
    astroid.draw()



if __name__ == '__main__':
    ast = asterids(5)
    pyglet.app.run()


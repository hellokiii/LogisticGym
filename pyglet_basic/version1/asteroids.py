import pyglet
from pyglet.window import key
import random

game_window = pyglet.window.Window(800, 600)

pyglet.resource.path = ["../resources"]
# pyglet.resource.reindex()

def resize_image(image, width=50, height=50):
    image.width = width
    image.height = height


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

def asteriods(num_asteroids):
    asteroids = []
    for i in range(num_asteroids):
        asteroid_x = random.randint(0, 800)
        asteroid_y = random.randint(0, 600)
        asteroid_image = pyglet.resource.image("asteroid.png")
        resize_image(asteroid_image)
        center_image(asteroid_image)
        new_asteroid = pyglet.sprite.Sprite(
            img=asteroid_image, x=asteroid_x, y=asteroid_y)
        new_asteroid.rotation = random.randint(0, 360)
        asteroids.append(new_asteroid)
    return asteroids




# player_image = pyglet.resource.image("player.png")
# bullet_image = pyglet.resource.image("bullet.png")


# resize_image(player_image)
# resize_image(bullet_image)



# score_label = pyglet.text.Label(text="Score: 0", x=10, y=575)
# level_label = pyglet.text.Label(text="My Amazing Game", x=400, y=575, anchor_x='center')

# player_ship = pyglet.sprite.Sprite(img=player_image, x=400, y=300)


@game_window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print("'A' was pressed")
    elif symbol == key.LEFT:
        print("left arrow")
    elif symbol == key.ENTER:
        print("Enter")



@game_window.event
def on_draw():
    game_window.clear()
    ast = asteriods(5)
    for a in ast:
        a.draw()
    # level_label.draw()
    # score_label.draw()
    # player_ship.draw()




pyglet.app.run()
print("!23123123123")




# center_image(player_image)
# center_image(bullet_image)
# center_image(asteroid_image)

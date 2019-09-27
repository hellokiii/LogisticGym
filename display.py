import pyglet

class Viewer(object):
    def __init__(self, width, height, display=None):
        # display = pyglet.canvas.Display()  # TODO: name display

        self.width = width
        self.height = height

        self.window = pyglet.window.Window(width=width, height=height, display=display)
        self.window.on_close = self.window_closed_by_user
        self.geoms = []
        self.onetime_geoms = []
        self.units = None
        self.palettes = None
        # self.transform = Transform()

    def close(self):
        self.window.close()

    def window_closed_by_user(self):
        self.close()

    # def set_bounds(self, left, right, bottom, top):
    #     assert right > left and top > bottom
    #     scalex = self.width / (right - left)
    #     scaley = self.height / (top - bottom)
    #     self.transform = Transform(
    #         translation=(-left * scalex, -bottom * scaley),
    #         scale=(scalex, scaley))

    def add_geom(self, geom):
        self.geoms.append(geom)

    def add_onetime(self, geom):
        self.onetime_geoms.append(geom)

    def render(self, return_rgb_array=False):
        # glClearColor(1, 1, 1, 1)
        print("1111111")
        self.window.clear()
        self.window.switch_to()
        self.window.dispatch_events()
        image = pyglet.resource.image("unit.png")
        ss = pyglet.sprite.Sprite(image, x=400, y=300)
        ss.draw()

        for u in self.units:
            u.sprite.draw()
            # print(u.sprite.x, u.sprite.y)

        for p in self.palettes:
            p.sprite.x = 400
            p.sprite.y = 300
            p.sprite.draw()
            # print(p.sprite.x, p.sprite.y)

        # self.window.on_draw()
        # self.transform.enable()
        # for geom in self.geoms:
        #     geom.render()
        # for geom in self.onetime_geoms:
        #     geom.render()
        # self.transform.disable()
        # arr = None
        # if return_rgb_array:
        #     buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        #     image_data = buffer.get_image_data()
        #     arr = np.fromstring(image_data.data, dtype=np.uint8, sep='')
        #     # In https://github.com/openai/gym-http-api/issues/2, we
        #     # discovered that someone using Xmonad on Arch was having
        #     # a window of size 598 x 398, though a 600 x 400 window
        #     # was requested. (Guess Xmonad was preserving a pixel for
        #     # the boundary.) So we use the buffer height/width rather
        #     # than the requested one.
        #     arr = arr.reshape(buffer.height, buffer.width, 4)
        #     arr = arr[::-1, :, 0:3]
        # self.window.flip()
        # self.onetime_geoms = []

        return None


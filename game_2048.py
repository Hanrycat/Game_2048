import pyglet

WIN_WIDTH = 530
WIN_HEIGHT = 720

class Window(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.game_init()

	def game_init(self):
		pass

win = Window(WIN_WIDTH,WIN_HEIGHT)

icon = pyglet.image.load('logo.ico')
win.set_icon(icon)

pyglet.app.run()
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy_garden.mapview import MapView


class MapViewExample(FloatLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

class Main(MDApp):
	def build(self):
		return MapViewExample()


Main().run()
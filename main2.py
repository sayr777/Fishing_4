from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy_garden.mapview import MapView
from gpshelper import GpsHelper


class MapViewExample(MDFloatLayout):
	def __init__(self):
		super(MapViewExample, self).__init__()
		m = MapView(zoom = 10, lat=50.6394, lon=3.057, on_map_relocated=self.func)
		self.add_widget(m)

	def func(self, *args):
		print(args)

class Main(MDApp):
	def build(self):
		return MapViewExample()


Main().run()
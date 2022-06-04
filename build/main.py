from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine

#for debug... REMOVE THIS, IF THIS IS PRODUCTION
#from kivy.core.window import Window
#Window.size = (480, 853) 

#subimport
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton

#define different screens
class GPSHelper(Screen):
	def __init__(self, **kwargs):
		super(GPSHelper, self).__init__(**kwargs)
		source_= 'array.geojson'

		options = {}
		layer = GeoJsonMapLayer(source=source_)
		
		lon, lat = layer.center
		options["lon"] = 45.895986557006836
		options["lat"] = 47.99296606506406
		min_lon, max_lon, min_lat, max_lat = layer.bounds
		radius = haversine(min_lon, min_lat, max_lon, max_lat)
		zoom = get_zoom_for_radius(radius, lat)
		options["zoom"] = 14

		self.view = MapView(**options)
		self.view.add_layer(layer)

		self.marker_layer = ClusteredMarkerLayer(cluster_radius=200)

		self.view.add_layer(self.marker_layer)

		# create marker if they exists
		self.count = 0

		layer.traverse_feature(self.create_marker)
		self.add_widget(self.view)

	def create_marker(self, feature):
	    geometry = feature["geometry"]
	    if geometry["type"] != "Point":
	        return
	    lon, lat = geometry["coordinates"]
	    self.marker_layer.add_marker(lon, lat )
	    self.count += 1

class Onboard(Screen, MDFloatLayout):
	pass

class RegistrationMain(Screen, MDBoxLayout):
	input_surname = ObjectProperty()
	input_name = ObjectProperty()
	input_lastname = ObjectProperty()
	input_mail = ObjectProperty()
	input_phone = ObjectProperty()

	def click_on_button_privacy_policy(self):
		pass

	def click_on_button_terms_and_agreements(self):
		pass

class RegistrationDop(Screen, MDBoxLayout):
	button_continue = ObjectProperty()
	checkbox_agree = ObjectProperty()

	def click_on_button_continue(self):
		print('Продолжение регистрации')

	def click_on_checkbox_agree(self, instance, value):
		if value:
			self.button_continue.disabled = False
		else:
			self.button_continue.disabled = True

	def click_on_back(self):
		print('Возвращение назад')

class Enter(Screen, MDBoxLayout):
	input_phone = ObjectProperty()

	def click_on_button_enter(self):
		print('Вход')

class EnterCheckPhone(Screen, MDBoxLayout):
	label_phone = ObjectProperty()
	input_code = ObjectProperty()
	phoneNumber = ''
	
	def click_on_button_confirm(self):
		print('Confirm entering')

class WindowManager(ScreenManager):
	pass

class MyApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Умная рыбалка'

	def build(self):
		self.theme_cls.theme_style = "Light"
		return Builder.load_file('my.kv')

if __name__ == '__main__':
	MyApp().run()
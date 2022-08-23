from kivymd.app import MDApp
from kivy.utils import platform
from kivymd.uix.dialog import MDDialog

class Gps():
	has_centered_map = False
	def run(self):
		#Request permissions on Android
		if platform == 'android':
			from android.permissions import Permission, request_permissions
			def callback(permission, results):
				if all([res for res in results]):
					print('Got all permissions')
				else:
					print('Did not get all permissions')

			request_permissions([Permission.ACCESS_COARSE_LOCATION, Permission.ACCESS_FINE_LOCATION], callback)
		
		#Get a reference to GpsBlinker, then call blink()
		gps_blinker = MDApp.get_running_app().root.get_screen('GPSHelper').ids.main_map.ids.blinker
		gps_blinker.blink()
		#Configure GPS
		if platform == 'android' or platform == 'ios':
			from plyer import gps
			gps.configure(on_location=self.update_blinker_position, on_status=self.on_auth_status)
			gps.start(minTime=1000, minDistance=0)

	def update_blinker_position(self, *args, **kwargs):
		my_lat = kwargs['lat']
		my_lon = kwargs['lon']
		#Update GpsBlinker position
		gps_blinker = MDApp.get_running_app().root.get_screen('GPSHelper').ids.main_map.ids.blinker
		gps_blinker.lat = my_lat
		gps_blinker.lon = my_lon

		#Center map on gps
		if not self.has_centered_map:
			map_main = MDApp.get_running_app().root.get_screen('GPSHelper').ids.main_map
			map_main.center_on(my_lat, my_lon)
			self.has_centered_map = True

	def on_auth_status(self, general_status, status_message):
		if general_status == 'provider-enabled':
			pass
		else:
			self.open_gps_access_popup()

	def open_gps_access_popup(self):
		dialog = MDDialog(title='Ошибка GPS', text="Вам нужно включить Гео-локацию")
		dialog.size_hint = [.8, .8]
		dialog.pos_hint = {'center_x': .5, 'center_y': .5}
		dialog.open()

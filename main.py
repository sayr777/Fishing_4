from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager

#define different screens
class Onboard(Screen):
	pass

class RegistrationMain(Screen):
	input_surname = ObjectProperty()
	input_name = ObjectProperty()
	input_lastname = ObjectProperty()
	input_mail = ObjectProperty()
	input_phone = ObjectProperty()

	def click_on_button_privacy_policy(self):
		pass

	def click_on_button_terms_and_agreements(self):
		pass

class WindowManager(ScreenManager):
	pass

kv = Builder.load_file('main.kv')

class MyApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Умная рыбалка'

	def build(self):
		self.theme_cls.theme_style = "Light"
		return kv

if __name__ == '__main__':
	MyApp().run()
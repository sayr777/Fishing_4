from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

#for debug... REMOVE THIS, IF THIS IS PRODUCTION
from kivy.core.window import Window
Window.size = (480, 853) 

#subimport
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton

#define different screens
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
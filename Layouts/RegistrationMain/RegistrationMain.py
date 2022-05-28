from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty

#subimport
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel

class Container(MDBoxLayout):

	input_surname: ObjectProperty()
	input_name: ObjectProperty()
	input_lastname: ObjectProperty()
	input_mail: ObjectProperty()
	input_phone: ObjectProperty()

	def click_on_button_register(self):
		print('Регистрация')



class RegistrationMainApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Регистрация'

	def build(self):
		self.theme_cls.theme_style = 'Light'
		return Container()

if __name__ == '__main__':
	RegistrationMainApp().run()
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty

#subimport
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField

class Container(MDBoxLayout):
	label_phone = ObjectProperty()
	input_code = ObjectProperty()
	phoneNumber = ''
	
	def click_on_button_confirm(self):
		print('Confirm entering')

class EnterCheckPhoneApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Подтверждение телефона'

	def build(self):
		self.theme_cls.theme_style = 'Light'
		return Container()

if __name__ == '__main__':
	EnterCheckPhoneApp().run()

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty

#subimport
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

class Container(MDBoxLayout):
	button_continue = ObjectProperty()
	checkbox_agree = ObjectProperty()

	def click_on_button_continue(self):
		print('Продолжение регистрации')

	def click_on_checkbox_agree(self):
		if checkbox_agree.value:
			button_continue.disabled = False
		else:
			button_continue.disabled = True

	def click_on_back(self):
		print('Возвращение назад')

class RegistrationDopApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Подтверждение'

	def build(self):
		self.theme_cls.theme_style = 'Light'
		return Container()

if __name__ == '__main__':
	RegistrationDopApp().run()
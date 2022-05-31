from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen

#subimport
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout

class Container(MDFloatLayout):
	def click_on_button_start(self):
		print('Продолжить')

class OnboardApp(MDApp):
	theme_cls = ThemeManager()
	title = 'Главная'

	def build(self):
		self.theme_cls.theme_style = 'Light'
		return Container()

if __name__ == '__main__':
	OnboardApp().run()
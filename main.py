from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine
from kivymd.uix.dialog import MDDialog
import re
import random

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

KIVY_FILENAME = 'main.kv'

class Data():
    phone = 0
    code = 0

class ErrorDialog(MDDialog):
    def __init__(self, text, **kwargs):
        super(ErrorDialog, self).__init__(**kwargs)
        self.dialog = MDDialog(title='Ошибка', text=text, size_hint=[.25, .25], auto_dismiss=False, buttons=[MDRoundFlatButton(text='OK', on_release=self.callback)])
        self.dialog.open()
	
    def callback(self, widget):
        self.dialog.dismiss()

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

class RegistrationMain(Screen):
    input_surname = ObjectProperty()
    input_name = ObjectProperty()
    input_lastname = ObjectProperty()
    input_mail = ObjectProperty()
    input_phone = ObjectProperty()

    def build(self, kwargs):
        super(RegistrationMain, self).__init__(**kwargs)

    def click_on_button_privacy_policy(self):
        pass

    def click_on_button_terms_and_agreements(self):
        pass

    def click_on_button_enter(self):
        self.parent.current = 'Enter'
        
    def click_on_button_register(self):
        if self.input_surname.text == '':
            ErrorDialog('Вы не ввели фамилию')
        else:
            if self.input_name.text == '':
                ErrorDialog('Вы не ввели имя')
            else:
                if self.input_lastname.text == '':
                    ErrorDialog('Вы не ввели отчество')
                else:
                    if self.input_mail.text == '':
                        ErrorDialog('Вы не ввели почту')
                    else:
                        if re.match('/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[-1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/', self.input_mail.text):
                            ErrorDialog('Неккоректный ввод почты')
                        else:
                            if self.input_phone.text == '':
                                ErrorDialog('Вы не ввели телефон')
                            else:
                                if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                                    ErrorDialog('Неккоректный ввод телефона')
                                else:
                                    #self.parent.current = 'RegistrationDop'
                                    ErrorDialog('Данная функция находится в разработке')

class RegistrationDop(Screen):
    button_continue = ObjectProperty()	

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
        if self.input_phone.text == '':
            ErrorDialog('Вы не ввели телефон')
        else:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                ErrorDialog('Неккоректный ввод телефона')
            else:
                phone = self.input_phone.text
                code = random.randint(100000, 999999)
                Data.phone = phone
                Data.code = code
                ErrorDialog('Функция отправки кода подтверждения в разработке, ваш код: '+str(Data.code))
                self.parent.get_screen('EnterCheckPhone').ids.label_phone.text = str(Data.phone)
                self.parent.current = 'EnterCheckPhone'

class EnterCheckPhone(Screen):
    label_phone = ObjectProperty()
    input_code = ObjectProperty()

    def click_on_button_confirm(self):
        if self.input_code.text == '':
            ErrorDialog('Вы не ввели код')
        else:
            if self.input_code.text != str(Data.code):
                ErrorDialog('Неверный код')
            else:
                self.parent.current = 'GPSHelper'

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
    theme_cls = ThemeManager()
    title = 'Умная рыбалка'

    def build(self):
        self.theme_cls.theme_style = "Light"
        from kivy.resources import resource_find
        filename = resource_find(KIVY_FILENAME) or KIVY_FILENAME
        if filename in Builder.files:
            Builder.unload_file(filename)
        return Builder.load_file(filename)

if __name__ == '__main__':
    MyApp().run()

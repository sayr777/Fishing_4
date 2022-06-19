from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine
from dialog import Dialog
import re
import random
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivy.uix.image import Image
from kivymd.uix.menu import MDDropdownMenu

#for debug... REMOVE THIS, IF THIS IS PRODUCTION
from kivy.core.window import Window
Window.size = (375, 812) 

#subimport
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import RelativeLayout

KIVY_FILENAME = 'main.kv'

class Data():
    phone = 0
    code = 0

    input_surname = ''
    input_name = ''
    input_lastname = ''
    input_mail = ''
    input_phone = 0

    def save_info(self, surname, name, lastname, mail, phone):
        self.input_surname = surname
        self.input_name = name
        self.input_lastname = lastname
        self.input_mail = mail
        self.input_phone = phone

class News(Screen):
    pass

class Calendar(Screen):
    pass

class User(Screen):
    pass

class Menu(Screen):
    def click_on_button_catalogFish(self):
        ErrorDialog('Функция отображения каталога рыб в разработке')

    def click_on_button_recipes(self):
        ErrorDialog('Функция отображения рецептов приготовления в разработке')

    def click_on_button_rules(self):
        ErrorDialog('Функция отображения Правил рыбалки в разработке')

    def click_on_button_penalties(self):
        ErrorDialog('Функция отображения Штрафов в разработке')

class Rules(Screen):
    pass

class Penalties(Screen):
    pass

class CatalogFish(Screen):
    pass

class Recipes(Screen):
    pass

#define different screens
class GPSHelper(Screen):
    input_search = ObjectProperty()

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

    def click_on_button_gps(self):
        Dialog('Вы уже на данной странице', 'Уведомление')
    
    def click_on_button_note(self):
        self.parent.current = 'Menu'

    def click_on_button_plus(self):
        self.parent.current = 'News'

    def click_on_button_user(self):
        self.parent.current = 'User'

    def click_on_button_calendar(self):
        self.parent.current = 'Calendar'

    def click_on_button_fish(self):
        Dialog('Функция рыбки в разработке', 'Ошибка')

    def click_on_button_userGps(self):
        Dialog('Функция гео-локации в разработке', 'Ошибка')

    def click_on_button_layers(self):
        Dialog('Функция отображения слоев в разработке', 'Ошибка')

class Onboard(Screen):
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
        Data.save_info(self.input_surname.text, self.input_name.text, self.input_lastname.text, self.input_mail.text, int(self.input_phone.text))
        self.parent.current = 'RegistrationDop'

    def click_on_button_enter(self):
        self.parent.current = 'Enter'
        
    def click_on_button_register(self):
        if self.input_surname.text == '':
            Dialog('Вы не ввели фамилию', 'Ошибка')
        else:
            if self.input_name.text == '':
                Dialog('Вы не ввели имя', 'Ошибка')
            else:
                if self.input_lastname.text == '':
                    Dialog('Вы не ввели отчество', 'Ошибка')
                else:
                    if self.input_mail.text == '':
                        Dialog('Вы не ввели почту', 'Ошибка')
                    else:
                        if re.match('/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[-1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/', self.input_mail.text):
                            Dialog('Неккоректный ввод почты', 'Ошибка')
                        else:
                            if self.input_phone.text == '':
                                Dialog('Вы не ввели телефон', 'Ошибка')
                            else:
                                if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                                    Dialog('Неккоректный ввод телефона', 'Ошибка')
                                else:
                                    #self.parent.current = 'RegistrationDop'
                                    Dialog('Данная функция находится в разработке', 'Ошибка')

class RegistrationDop(Screen):
    button_continue = ObjectProperty()	

    def click_on_checkbox_agree(self, instance, value):
        if value:
            self.button_continue.disabled = False
        else:
            self.button_continue.disabled = True

    def click_on_back(self):
        self.parent.current = 'Onboard'

    def click_on_button_continue(self):
        self.parent.get_screen('RegistrationMain').ids.input_surname.text = Data.input_surname
        self.parent.get_screen('RegistrationMain').ids.input_name.text = Data.input_name
        self.parent.get_screen('RegistrationMain').ids.input_lastname.text = Data.input_lastname
        self.parent.get_screen('RegistrationMain').ids.input_mail.text = Data.input_mail
        self.parent.get_screen('RegistrationMain').ids.input_phone.text = str(Data.input_phone)
        self.parent.current = 'RegistrationMain'

class Enter(Screen, MDBoxLayout):
    input_phone = ObjectProperty()

    def click_on_button_enter(self):
        if self.input_phone.text == '':
            Dialog('Вы не ввели телефон', 'Ошибка')
        else:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                Dialog('Неккоректный ввод телефона', 'Ошибка')
            else:
                phone = self.input_phone.text
                code = random.randint(100000, 999999)
                Data.phone = phone
                Data.code = code
                Dialog('Функция отправки кода подтверждения в разработке, ваш код: '+str(Data.code), 'Ошибка')
                self.parent.get_screen('EnterCheckPhone').ids.label_phone.text = str(Data.phone)
                self.parent.current = 'EnterCheckPhone'

    def click_on_button_register(self):
        self.parent.current = 'RegistrationMain'

class EnterCheckPhone(Screen):
    label_phone = ObjectProperty()
    input_code = ObjectProperty()

    def click_on_button_confirm(self):
        if self.input_code.text == '':
            Dialog('Вы не ввели код', 'Ошибка')
        else:
            if self.input_code.text != str(Data.code):
                Dialog('Неверный код', 'Ошибка')
            else:
                self.parent.current = 'GPSHelper'

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
    theme_cls = ThemeManager()
    title = 'Умная рыбалка'

    def build(self):
        self.theme_cls.theme_style = "Light"
        LabelBase.register(name='Proxima Nova', fn_regular='resources/fonts/proximanova_regular.ttf')
        theme_font_styles.append('Proxima Nova')
        self.theme_cls.font_styles['Proxima Nova'] = ["Proxima Nova", 16, False, 0.15]
        from kivy.resources import resource_find
        filename = resource_find(KIVY_FILENAME) or KIVY_FILENAME
        if filename in Builder.files:
            Builder.unload_file(filename)
        return Builder.load_file(filename)

if __name__ == '__main__':
    MyApp().run()

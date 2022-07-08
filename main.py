from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView, MapSource
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine
from dialog import Dialog
import re
import random
import io
import datetime
from kivy.core.text import LabelBase
from kivymd.font_definitions import theme_font_styles
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import mainthread
import sqlite3 as SQLCommander
from sms_base import rec_otp

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

MONTH_LIST = {
    '1' : 31,
    '2' : 28,
    '3' : 31,
    '4' : 30,
    '5' : 31,
    '6' : 30,
    '7' : 31,
    '8' : 31,
    '9' : 30,
    '10' : 31,
    '11' : 30,
    '12' : 31
}

CALENDAR_CODE = [
    [222222333321110001111111133333222222],
    [000000001222220002223333211000000000],
    [000000001222220002233333332211000000],
    [222222111111330002222222222222222222],
    [222222111133330001111111111122222222],
    [111111222221110002222222333333333111],
    [000000000000030003333221111122221000],
    [111111222222220002222222222222222333],
    [222222111123330002222222222222222333],
    [111111222222330003333333333222211111],
    [111111222222330003333333333222211111],
    [000000000001220002233222222220000000],
]

class Data():
    phone = 0
    code = 0

    input_surname = ''
    input_name = ''
    input_lastname = ''
    input_mail = ''
    input_phone = 0

    db = []

    def save_info(self, surname, name, lastname, mail, phone):
        self.input_surname = surname
        self.input_name = name
        self.input_lastname = lastname
        self.input_mail = mail
        self.input_phone = phone

class News(Screen):
    pass

class Calendar(Screen):
    listFish = ObjectProperty()

    one_label = ObjectProperty()
    two_label = ObjectProperty()
    three_label = ObjectProperty()
    four_label = ObjectProperty()
    fife_label = ObjectProperty()
    six_label = ObjectProperty()
    seven_label = ObjectProperty()
    eight_label = ObjectProperty()
    nine_label = ObjectProperty()
    ten_label = ObjectProperty()
    eleven_label = ObjectProperty()
    twelve_label = ObjectProperty()
    thirteen_label = ObjectProperty()
    fourteen_label = ObjectProperty()
    fifteen_label = ObjectProperty()
    sixteen_label = ObjectProperty()
    seventeen_label = ObjectProperty()
    eightteen_label = ObjectProperty()
    nineteen_label = ObjectProperty()
    twenty_label = ObjectProperty()
    twenty_one_label = ObjectProperty()
    twenty_two_label = ObjectProperty()
    twenty_three_label = ObjectProperty()
    twenty_four_label = ObjectProperty()
    twenty_five_label = ObjectProperty()
    twenty_six_label = ObjectProperty()
    twenty_seven_label = ObjectProperty()
    twenty_eight_label = ObjectProperty()
    twenty_nine_label = ObjectProperty()
    thirty_label = ObjectProperty()
    thirty_one_label = ObjectProperty()

    def __init__(self, **kwargs):
        super(Calendar, self).__init__(**kwargs)
        mn_now = datetime.date.today().month
        days_in_mon = MONTH_LIST[str(mn_now)]
        if days_in_mon == 28:


class User(Screen):
    pass

class Menu(Screen):
    def click_on_button_catalogFish(self):
        self.parent.current = 'CatalogFish'

    def click_on_button_recipes(self):
        self.parent.current = 'Recipes'

    def click_on_button_rules(self):
        self.parent.current = 'Rules'

    def click_on_button_penalties(self):
        self.parent.current = 'Penalties'

class Rules(Screen):
    pass

class Penalties(Screen):
    pass

class CatalogFish(Screen):
    listFish = ObjectProperty()

    def __init__(self, **kwargs):
        super(CatalogFish, self).__init__(**kwargs)
        i = 0
        while i < len(Data.db):
            newGrid = MDGridLayout(rows=2)
            lab1 = MDLabel(font_style='Proxima Nova', text_size='16sp', bold=True, text=Data.db[i][1])
            lab2 = MDLabel(font_style='Proxima Nova', text_size='16sp', text=Data.db[i][5])
            listFish.add_widget(newGrid)
            newGrid.add_widget(lab1)
            newGrid.add_widget(lab2)
            buf = io.BytesIO(Data.db[i][4])
            cim = CoreImage(buf, ext='jpg')
            img = Image(texture=cim.texture)
            listFish.add_widget(img)
            i += 1

    def click_on_button_esox(self):
        Dialog('Страница подробного описания обыкновенной щуки в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_silurus(self):
        Dialog('Страница подробного описания обыкновенного сома в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_cyprinus(self):
        Dialog('Страница подробного описания сазана в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_abramis(self):
        Dialog('Страница подробного описания леща в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_rutilus(self):
        Dialog('Страница подробного описания воблы в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_sander(self):
        Dialog('Страница подробного описания обыкновенного судака в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_aspius(self):
        Dialog('Страница подробного описания обыкновенного жереха в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_perka(self):
        Dialog('Страница подробного описания речного окуня в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_blicca(self):
        Dialog('Страница подробного описания густеры в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_scardinius(self):
        Dialog('Страница подробного описания краснопёрки в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_carassius(self):
        Dialog('Страница подробного описания карася в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

    def click_on_button_tinca(self):
        Dialog('Страница подробного описания линя в разработке', 'Уведомление о разработке')
        #self.parent.current = ''

class Recipes(Screen):
    pass

#define different screens
class GPSHelper(Screen):
    input_search = ObjectProperty()

    def __init__(self, **kwargs):
        super(GPSHelper, self).__init__(**kwargs)

        # source =MapSource("https://api.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}@2x.jpg90?access_token=pk.eyJ1IjoiYW50b24wNjEyIiwiYSI6ImNpbzl5dWQxYjAwN3h2eWx5Zmw1Y2lkdGkifQ.h1Rr222Sb_Ibl7OgrmwulQ","osm",0,19,256,"","","abc")
        # mapview = MapView(zoom=12, lat=46, lon=48)
        # mapview.map_source = source

        # self.add_widget(mapview)
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

    def __init__(self, **kwargs):
        super(RegistrationMain, self).__init__(**kwargs)

    def click_on_button_privacy_policy(self):
        Data.save_info(self.input_surname.text, self.input_name.text, self.input_lastname.text, self.input_mail.text, int(self.input_phone.text))
        self.parent.current = 'RegistrationDop'

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

class Enter(Screen):
    input_phone = ObjectProperty()

    def click_on_button_enter(self):
        if self.input_phone.text == '':
            Dialog('Вы не ввели телефон', 'Ошибка')
        else:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                Dialog('Неккоректный ввод телефона', 'Ошибка')
            else:
                phone = self.input_phone.text
                #code = rec_otp(self.input_phone.text)
                Data.phone = phone
                #Data.code = code
                self.parent.get_screen('EnterCheckPhone').ids.label_phone.text = str(Data.phone)
                #self.parent.current = 'EnterCheckPhone'
                self.parent.current = 'GPSHelper'

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        @mainthread
        def delayed():
            self.load_database()
        delayed()

    def load_database(self):
        conn = SQLCommander.connect("resources/DB/db.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM catalog ORDER BY name")

        allItems = cur.fetchall()
        allItems = list(allItems)

        Data.db = allItems
        #db[n][0] - id, db[n][1] - name, db[n][2] - none, db[n][3] - description, db[n][4] - pic, db[n][5] - latin, db[n][6] - gif

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

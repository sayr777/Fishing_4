from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView, MapSource, MarkerMapLayer
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
from kivymd.uix.dialog import MDDialog
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
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy import platform
from kivy.factory import Factory

if platform == 'android':
    from android.permissions import Permission, request_permissions
    request_permissions([Permission.INTERNET])

KIVY_FILENAME = 'main.kv'

MONTH_LIST = {
    '1' : 'Январь',
    '2' : 'Февраль',
    '3' : 'Март',
    '4' : 'Апрель',
    '5' : 'Май',
    '6' : 'Июнь',
    '7' : 'Июль',
    '8' : 'Август',
    '9' : 'Сентябрь',
    '10' : 'Октябрь',
    '11' : 'Ноябрь',
    '12' : 'Декабрь'
}

CALENDAR_CODE = [
    [2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 3, 3, 3, 3, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0]
]

class Data():
    phone = 0
    code = 0

    input_surname = ''
    input_name = ''
    input_lastname = ''
    input_mail = ''
    input_phone = 0

    stateMap = 'Street'

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

    def costFish(self, index):
        if index == 0:
            return '0%. Клёва нет'
        elif index == 1:
            return '<50%. Слабый клёв'
        elif index == 2:
            return '>50%. Средний клёв'
        elif index == 3:
            return '>80%. Высокий клёв'

    def click_on_cell(self, widget):
        #18-20
        day = int(widget.text)
        if widget.text_color == [1.0, 0.0, 0.0, 1.0]:
            Dialog('Вылов рыбы в этот день запрещен!', 'Внимание!!!')
        else:
            index = 0
            if day < 11:
                index = 18
            elif day < 21 and day > 10:
                index = 19
            else:
                index = 20
            esox = self.costFish(CALENDAR_CODE[0][index])
            silurus = self.costFish(CALENDAR_CODE[1][index])
            cyprinus = self.costFish(CALENDAR_CODE[2][index])
            self.parent.get_screen('Itog').ids.label_chance_esox.text = 'Шанс поймать: '+esox
            self.parent.get_screen('Itog').ids.label_chance_silurus.text = 'Шанс поймать: '+silurus
            self.parent.get_screen('Itog').ids.label_chance_cyprinus.text = 'Шанс поймать: '+cyprinus
            self.parent.current = 'Itog'

class Itog(Screen):
    label_chance_esox = ObjectProperty()
    label_chance_silurus = ObjectProperty()
    label_chance_cyprinus = ObjectProperty()

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

class Esox(Screen):
    pass

class Silurus(Screen):
    pass

class Cyprinus(Screen):
    pass

class Weapon(Screen):
    pass

class CatalogFish(Screen):
    def __init__(self, **kwargs):
        super(CatalogFish, self).__init__(**kwargs)

    def click_on_button_esox(self):
        self.parent.current = 'Esox'

    def click_on_button_silurus(self):
        self.parent.current = 'Silurus'

    def click_on_button_cyprinus(self):
        self.parent.current = 'Cyprinus'

class Recipes(Screen):
    pass

class CustomBottomSheet(Screen, MDBoxLayout):
    image_allowed = ObjectProperty()
    image_disallowed = ObjectProperty()
    image_shops = ObjectProperty()

#define different screens
class GPSHelper(Screen):
    input_search = ObjectProperty()
    main_map = ObjectProperty()
    
    fishing_allowed = False
    fishing_disallowed = False
    fishing_shops = False

    def __init__(self, **kwargs):
        super(GPSHelper, self).__init__(**kwargs)

        self.source_street = MapSource(url='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}')
        self.source_satellite = MapSource(url='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}')
        self.source_hybrid = MapSource(url='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}')

        source_fishing_allowed = 'resources/layers/fishing_allowed.geojson'
        source_fishing_disallowed = 'resources/layers/fishing_disallowed.geojson'
        source_fishing_shops = 'resources/layers/fishing_shops.geojson'
        source_polygon_allowed = 'resources/layers/allowed_polygon.geojson'
        source_polygon_disallowed = 'resources/layers/disallowed_polygon.geojson'
        
        self.layer_polygon_allowed = GeoJsonMapLayer(source=source_polygon_allowed)
        self.layer_polygon_disallowed = GeoJsonMapLayer(source=source_polygon_disallowed)
        self.layer_fishing_allowed = MarkerMapLayer()
        self.layer_fishing_disallowed = MarkerMapLayer()
        self.layer_fishing_shops = MarkerMapLayer()

        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.948970794677734, lat=46.56228323662375, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.008880615234375, lat=46.53253190986272, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.03926467895508, lat=46.52745366594394, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.99600601196288, lat=46.55874226707572, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.013343811035156, lat=46.481373492133784, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.02999496459961, lat=46.50193716468582, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.97025680541992, lat=46.46257575132626, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.9611587524414, lat=46.49141993572272, source='resources/map_sign/fishing_allowed_on.png'))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.005104064941406, lat=46.409931207495845, source='resources/map_sign/fishing_allowed_on.png'))

        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.95463562011719, lat=46.528162286622035, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01574707031249, lat=46.527689873863785, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01300048828125, lat=46.50264611816897, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.99171447753906, lat=46.49177448218621, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.97557830810547, lat=46.500519229985045, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.96424865722656, lat=46.50099187899411, source='resources/map_sign/fishing_disallowed_on.png'))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.976951599121094, lat=46.53359473803679, source='resources/map_sign/fishing_disallowed_on.png'))

        self.layer_fishing_shops.add_widget(MapMarker(lon=47.99520134925842, lat=46.46676590440685, source='resources/map_sign/fishing_shop_on.png'))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03745687007904, lat=46.4956595690788, source='resources/map_sign/fishing_shop_on.png'))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.069820404052734, lat=46.36908189730966, source='resources/map_sign/fishing_shop_on.png'))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03526818752289, lat=46.32747782427445, source='resources/map_sign/fishing_shop_on.png'))

    def centering(self, layer):
        lon, lat = layer.center
        min_lon, max_lon, min_lat, max_lat = layer.bounds
        radius = haversine(min_lon, min_lat, max_lon, max_lat)
        self.main_map.zoom = get_zoom_for_radius(radius, lat)

    def click_fishing_allowed(self, widget):
        if self.fishing_allowed:
            self.fishing_allowed = False
            self.main_map.remove_layer(self.layer_polygon_allowed)
            self.main_map.remove_layer(self.layer_fishing_allowed)
            widget.parent.children[5].source = 'resources/map_sign/fishing_allowed_off.png'
        else:
            self.fishing_allowed = True
            self.centering(self.layer_polygon_allowed)
            self.main_map.add_layer(self.layer_polygon_allowed)
            self.main_map.add_layer(self.layer_fishing_allowed)
            self.layer_fishing_allowed.reposition()
            widget.parent.children[5].source = 'resources/map_sign/fishing_allowed_on.png'

    def click_fishing_disallowed(self, widget):
        if self.fishing_disallowed:
            self.fishing_disallowed = False
            self.main_map.remove_layer(self.layer_polygon_disallowed)
            self.main_map.remove_layer(self.layer_fishing_disallowed)
            widget.parent.children[3].source = 'resources/map_sign/fishing_disallowed_off.png'
        else:
            self.fishing_disallowed = True
            self.centering(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_fishing_disallowed)
            self.layer_fishing_disallowed.reposition()
            widget.parent.children[3].source = 'resources/map_sign/fishing_disallowed_on.png'

    def click_fishing_shops(self, widget):
        if self.fishing_shops:
            self.fishing_shops = False
            self.main_map.remove_layer(self.layer_fishing_shops)
            widget.parent.children[1].source = 'resources/map_sign/fishing_shop_off.png'
        else:
            self.fishing_shops = True
            self.main_map.add_layer(self.layer_fishing_shops)
            self.layer_fishing_shops.reposition()
            widget.parent.children[1].source = 'resources/map_sign/fishing_shop_on.png'

    def click_on_button_gps(self):
        Dialog('Вы уже на данной странице', 'Внимание!')

    def click_on_button_note(self):
        self.parent.current = 'Menu'

    def click_on_button_plus(self):
        self.parent.current = 'News'

    def click_on_button_user(self):
        self.parent.current = 'User'

    def click_on_button_calendar(self):
        mn_now = datetime.date.today().month
        days_in_mon = MONTH_LIST[str(mn_now)]
        if days_in_mon == 28:
            twenty_nine_label.disabled = True
            thirty_label.disabled = True
            thirty_one_label.disabled = True
        elif days_in_mon == 30:
            thirty_one_label.disabled = True

        # sequence = [0, 0, 0, 0]
        # for i in range(len(CALENDAR_CODE)):
        #     if mn_now == 1:
        #         if CALENDAR_CODE[i][mn_now*3-3] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-3] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-3] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-3] == 3:
        #             sequence[3] += 1
        #     else:
        #         if CALENDAR_CODE[i][mn_now*3-2] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 3:
        #             sequence[3] += 1
        # max_ten = 0
        # k = 0
        # for i in range(len(sequence)):
        #     if sequence[i] > max_ten:
        #         max_ten = sequence[i]
        #         k = i
        # if k == 1:
        #     self.parent.get_screen('Calendar').ids.one_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.two_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.three_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.four_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fife_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.six_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seven_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eight_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nine_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.ten_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        # elif k == 2:
        #     self.parent.get_screen('Calendar').ids.one_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.two_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.three_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.four_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fife_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.six_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seven_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eight_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nine_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.ten_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        # elif k == 3:
        #     self.parent.get_screen('Calendar').ids.one_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.two_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.three_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.four_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fife_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.six_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seven_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eight_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nine_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.ten_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]

        # sequence = [0, 0, 0, 0]
        # for i in range(len(CALENDAR_CODE)):
        #     if mn_now == 1:
        #         if CALENDAR_CODE[i][mn_now*3-2] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-2] == 3:
        #             sequence[3] += 1
        #     else:
        #         if CALENDAR_CODE[i][mn_now*3-1] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 3:
        #             sequence[3] += 1
        # max_ten = 0
        # k = 0
        # for i in range(len(sequence)):
        #     if sequence[i] > max_ten:
        #         max_ten = sequence[i]
        #         k = i

        # if k == 1:
        #     self.parent.get_screen('Calendar').ids.eleven_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twelve_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fourteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fifteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.sixteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seventeen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eightteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nineteen_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        # elif k == 2:
        #     self.parent.get_screen('Calendar').ids.eleven_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twelve_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fourteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fifteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.sixteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seventeen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eightteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nineteen_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        # elif k == 3:
        #     self.parent.get_screen('Calendar').ids.eleven_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twelve_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fourteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.fifteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.sixteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.seventeen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.eightteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.nineteen_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]

        # sequence = [0, 0, 0, 0]
        # for i in range(len(CALENDAR_CODE)):
        #     if mn_now == 1:
        #         if CALENDAR_CODE[i][mn_now*3-1] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3-1] == 3:
        #             sequence[3] += 1
        #     else:
        #         if CALENDAR_CODE[i][mn_now*3] == 0:
        #             sequence[0] += 1
        #         elif CALENDAR_CODE[i][mn_now*3] == 1:
        #             sequence[1] += 1
        #         elif CALENDAR_CODE[i][mn_now*3] == 2:
        #             sequence[2] += 1
        #         elif CALENDAR_CODE[i][mn_now*3] == 3:
        #             sequence[3] += 1
        # max_ten = 0
        # k = 0
        # for i in range(len(sequence)):
        #     if sequence[i] > max_ten:
        #         max_ten = sequence[i]
        #         k = i
        # if k == 1:
        #     self.parent.get_screen('Calendar').ids.twenty_one_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_two_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_three_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_four_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_five_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_six_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_seven_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_eight_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_nine_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_one_label.md_bg_color = [53/255, 158/255, 24/255, 1.0]
        # elif k == 2:
        #     self.parent.get_screen('Calendar').ids.twenty_one_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_two_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_three_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_four_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_five_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_six_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_seven_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_eight_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_nine_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_one_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        # elif k == 3:
        #     self.parent.get_screen('Calendar').ids.twenty_one_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_two_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_three_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_four_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_five_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_six_label.md_bg_color = [194/255, 191/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_seven_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_eight_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.twenty_nine_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        #     self.parent.get_screen('Calendar').ids.thirty_one_label.md_bg_color = [194/255, 43/255, 43/255, 1.0]
        self.parent.current = 'Calendar'

    def click_on_button_fish(self):
        Dialog('Функция отображения зон лова рыбы в разработке', 'Внимание')

    def click_on_button_userGps(self):
        Dialog('Функция гео-локации в разработке', 'Внимание')

    def click_on_button_layers(self):
        self.obj = MDCustomBottomSheet(screen = Factory.CustomBottomSheet())
        if self.fishing_allowed:
            self.obj.children[0].children[0].children[0].ids.image_allowed.source = 'resources/map_sign/fishing_allowed_on.png'
        if self.fishing_disallowed:
            self.obj.children[0].children[0].children[0].ids.image_disallowed.source = 'resources/map_sign/fishing_disallowed_on.png'
        if self.fishing_shops:
            self.obj.children[0].children[0].children[0].ids.image_shops.source = 'resources/map_sign/fishing_shop_on.png'
        self.obj.open()

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
            Dialog('Вы не ввели фамилию', 'Внимание!')
        else:
            if self.input_name.text == '':
                Dialog('Вы не ввели имя', 'Внимание')
            else:
                if self.input_lastname.text == '':
                    Dialog('Вы не ввели отчество', 'Внимание')
                else:
                    if self.input_mail.text == '':
                        Dialog('Вы не ввели почту', 'Внимание')
                    else:
                        if re.match('/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[-1-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/', self.input_mail.text):
                            Dialog('Неккоректный ввод почты', 'Внимание')
                        else:
                            if self.input_phone.text == '':
                                Dialog('Вы не ввели телефон', 'Внимание')
                            else:
                                if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                                    Dialog('Неккоректный ввод телефона', 'Внимание')
                                else:
                                    #self.parent.current = 'RegistrationDop'
                                    Dialog('Данная функция находится в разработке', 'Внимание')

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
        #for debug
        self.parent.current = 'GPSHelper'
        if self.input_phone.text == '':
            Dialog('Вы не ввели телефон', 'Внимание!')
        else:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                Dialog('Неккоректный ввод телефона', 'Внимание!')
            else:
                phone = '+7' + self.input_phone.text
                code = rec_otp('7' + self.input_phone.text)
                Data.phone = phone
                Data.code = code
                self.parent.get_screen('EnterCheckPhone').ids.label_phone.text = str(Data.phone)
                self.parent.current = 'EnterCheckPhone'
                #self.parent.current = 'GPSHelper'

    def click_on_button_register(self):
        self.parent.current = 'RegistrationMain'

class EnterCheckPhone(Screen):
    label_phone = ObjectProperty()
    input_code = ObjectProperty()

    def click_on_button_confirm(self):
        if self.input_code.text == '':
            Dialog('Вы не ввели код', 'Внимание!')
        else:
            if self.input_code.text != str(Data.code):
                Dialog('Неверный код', 'Внимание')
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

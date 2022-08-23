from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy_garden.mapview import MapMarker, MapView, MapSource, MarkerMapLayer
from kivy_garden.mapview.clustered_marker_layer import ClusteredMarkerLayer
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from kivy_garden.mapview.utils import get_zoom_for_radius, haversine
from dialog import Dialog
from data import Data
import user_info
from news import News
from gps import Gps
from user import User
from profiledetails import ProfileDetails
from notes import Notes
from addnote import AddNote
import owm_request as owm
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
from kivy.uix.popup import Popup
import json
from shapely.geometry import Point
from shapely.geometry import Polygon

#for debug... REMOVE THIS, IF THIS IS PRODUCTION
from kivy.core.window import Window
#Window.size = (375, 812)

#subimport
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.toolbar import *
from kivymd.uix.button import MDIconButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.relativelayout import RelativeLayout
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivy import platform
from kivy.factory import Factory
from kivymd.uix.card import MDCard
#import screens
#from menu import MenuWidget

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

class FishResort(Screen):
    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showFishResort()

class HeFromEsox(Screen):
    pass

class SilurusHotted(Screen):
    pass

class DumplingFromCyprinus(Screen):
    pass

class PlaceChill(Screen):
    def click_on_fish_resort(self):
        self.parent.current = 'FishResort'

class FishPortal(Screen):
    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showFishPortal()

class Equipment(Screen):
    def click_on_fish_portal(self):
        self.parent.current = 'FishPortal'

class Fishka(Screen):
    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showFishka()

class Bait(Screen):
    def click_on_fishka(self):
        self.parent.current = 'Fishka'

class CaspiyUnic(Screen):
    def click_on_show_map(self):
        self.parent.current = 'GPSHelper'
        self.parent.get_screen('GPSHelper').showCaspiyUnic()

class BuyFish(Screen):
    def click_on_caspiy_unic(self):
        self.parent.current = 'CaspiyUnic'

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

    def entering(self):
        city_id = owm.get_city_id('Astrakhan, RU')
        appid = '7f13700bf40afc4cad42d3f35bcf37fa'
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print(data)

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
            Data.screen_history.append('Calendar')
            self.parent.current = 'Itog'

class Itog(Screen):
    label_chance_esox = ObjectProperty()
    label_chance_silurus = ObjectProperty()
    label_chance_cyprinus = ObjectProperty()

class Rules(Screen):
    def click_on_rule_fishing(self):
        Data.number_rule = 0
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_deadlines_spawning_off(self):
        Data.number_rule = 1
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_spawning_areas(self):
        Data.number_rule = 2
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_weapons_fishing(self):
        Data.number_rule = 3
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_daily_rate_of_fish_catch(self):
        Data.number_rule = 4
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_what_fish_off_fishing(self):
        Data.number_rule = 5
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_size_penalti_fishing(self):
        Data.number_rule = 6
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

    def click_on_what_can_pay_penalti_and_where(self):
        Data.number_rule = 7
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        Data.screen_history.append('Rules')
        self.parent.current = 'RuleFishing'

class RuleFishing(Screen):
    zag = ObjectProperty()
    main_text = ObjectProperty()

    data = [
        ['Правила рыболовства', '    Граждане вправе осуществлять любительское и спортивное рыболовство на водных объектах общего пользования свободно и бесплатно.\n\n    Однако, рыболов должен помнить, что во время лова он находится в границах водоохранных зон рек, озер, ручьев, каналов (50-200 м. от береговой линии в зависимости от протяженности водотока), где действует специальный режим осуществления хозяйственной и иной деятельности в целях предотвращения загрязнения, засорения, заиления указанных водных объектов и истощения их вод, а также сохранения среды обитания водных биологических ресурсов и других объектов животного и растительного мира.\n\n    В границах водоохранных зон запрещаются движение и стоянка транспортных средств (кроме специальных транспортных средств), за исключением их движения по дорогам и стоянки на дорогах и в специально оборудованных местах, имеющих твердое покрытие.\n\n    Нарушение данного запрета влечет за собой административную ответственность в виде штрафа для граждан в размере от трех тысяч до четырех тысяч пятисот рублей (статья 8.42 КоАП РФ).\n\n    В определенные месяцы, в области запрещено ловить рыбу. Ограничения вводятся в связи с периодом активного нереста. Ловить разрешается только на удочку. Количество крючков, используемых 1 человеком, должно быть не более 5.\n\n    Объем пойманной рыбы на одного человека не должен превышать 10 кг.'],
        ['Сроки нерестового запрета', '    Нерестовый период в Астраханской области в 2022 году устанавливается с 16 мая по 20 июня.\n\n    Запрещается любая рыбалка с 20 апреля по 20 июня — повсеместно, за исключением водных объектов рыбохозяйственного значения в пределах административных границ населенных пунктов, а также на рыбопромысловых участках, предоставленных для организации любительского и спортивного рыболовства в этот период. В эти месяцы запрещен отлов любого вида рыбы. Рыбалка разрешена, но только в специализированных водоемах и хранилищах.\n\n    В сроки, С 1 апреля по 30 июня запрещен вылов раков в любом количестве.\n\n    Запрещается:\n\n       •   любительская и спортивная охота на каспийского тюленя.\n\n       •   в запретных районах: волжское запретное предустьевое пространство, за исключением рыбопромысловых участков, предоставленных для организации любительского и спортивного рыболовства, нерестилища, зимовальные ямы.\n\n       •   применение колющих орудий лова, сетей всех типов, ловушек всех типов и конструкций (кроме раколовок), огнестрельного и пневматического оружия, арбалетов и луков, сомовников, капканов, крючковых самоловных снастей, сетных отцеживающих и объячеивающих орудий добычи (вылова) и приспособлений (бредней, неводов, волокуш, наметок, подъемников, кругов, «телевизоров», «экранов» и т.п.);\n\n       •   рыбалка кружками с общим количеством крючков более 10 штук на орудиях добычи (вылова) у одного гражданина;\n\n       •   рыбалка при помощи устройства заездок, загородок, заколок, запруд и других видов заграждений, частично или полностью перекрывающих русло водоемов и водотоков и препятствующих свободному перемещению рыбы;\n\n       •   рыбалка способом багрения, глушения, гона (в том числе с помощью бряцал и ботания), переметами с общим количеством крючков более 10 штук на орудиях добычи (вылова) у одного гражданина, «на подсветку»;\n\n       •   рыбалка жаберным способом (при использовании «жмыхоловок», «комбайнов») с количеством крючков более 2-х штук;\n\n       •   рыбалка раков руками вброд или путем ныряния.'],
        ['Нерестовые участки', '    Река Волга славится огромными территориями нерестилищ осетровой рыбы. Отправляясь на ловлю, стоит прочитать список (или лучше иметь его под рукой), чтобы выбрать правильное и не запрещенное место. Верхняя, средняя и нижняя зоны, следующие\n\n   •   Остров Спорный, Тракторный, Зеленый, Ельшанская, Рудневская. Протяженность нереста 1 км.\n\n   •   Остров Баррикадский, Татьянский – 2 км.\n\n   •   Гряд у Центрального стадиона. Протяженность нерестилища – 5 км.\n\n   •   Райгородская, Солодниковская гряда. Протяженность составляет 1 км.\n\n   •   Светлоярская и Дубовская зона. Территория занимает 2,5 км.\n\n   •   Каменноярская гряда – 6 км.\n\n   •   Соленозаймищенская, Пришибинская, Косикинская, Восточная. Протяженность гряды составляет 1 км.\n\n   •   Ветлянская, Верхнекопановская зона распространяется на 1,5 км.\n\n   •   Копановская, Сероглазовская имеет протяженность 2 км.\n\n   •   Цаган-Аманская – крупная гряда, которая протянулась на 8 км.\n\n    В период, когда начинается нерест, разрешена рыбалка, но только в специализированных местах с применением не более 2 крючков на одного человека.'],
        ['Орудия рыболовства', '    Для рыбалки в Астраханской области разрешается использовать следующие орудия и способы добычи (вылова):\n\n   •   поплавочная удочка, состоящая из удилища (в том числе с пропускными кольцами и со съемной катушкой с леской), лески, поплавка, грузил, поводков и крючков;\n\n   •   донная удочка (донка), состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской или шнуром) или хлыстика, лески или шнура, грузила, поводков и крючков;\n\n   •   донная удочка, состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской и шнуром) или хлыстика, лески, грузила, кормушки или жмыхоловки с количеством крючков не более 2-х штук;\n\n   •   донная удочка с амортизаторов (применяются только одинарные крючки);\n\n   •   блесны, воблеры, мушки и другие приманки, разные по форме и цвету с крючками (одинарными, двойниками или тройниками);\n\n   •   раколовки, в количестве не более трех штук у одного гражданина, каждый из параметров разрешаемых раколовок (длина, ширина, высота -для многоугольных, высота, диаметр - для конических и цилиндрических) не должны превышать 80 см:\n\n   •   добыча (вылов) на дорожку с применением гребного судна или плавучего средства с использованием не более двух приманок на одно судно или плавучее средство;\n\n   •   добыча (вылов) на троллинг - с применением паруса и/или мотора с использованием не более двух приманок на одно судно или плавучее средство;\n\n   •   добыча (вылов) рыбы «на квок»;\n\n   •   кораблики;\n\n   •   жерлицы;\n\n   •   специальные ружья и пистолеты для подводной охоты;\n\n   •   спиннинговая снасть (спиннинг), состоящую из удилища с пропускными кольцами и рукояткой, на которой крепится съемная катушка с леской или шнуром и оснащается одной приманкой с крючками (одинарными, двойниками или тройниками). Дополнительно перед приманкой может ставиться грузило без крючков.\n\n    Крючки - двойники или крючки - тройники применяются только при добыче (вылове) на спиннинг и жерлицу.'],
        ['Суточная норма вылова рыбы', '    Не только местные любят рыбачить на «своей» территории. Активность проявляют и любители попытать удачу в улове крупной рыбы с других регионов. Многие удильщики как можно раньше начинают готовиться к поездке. Необходимо закупить крючки, удочки и узнать период, когда стоит посещать водоем. Но после вступления закона в силу, рыбакам ограничили масштабы отлова. Введена суточная норма, чтобы не нарушать баланс и предотвратить исчезновение некоторых видов:\n\n   •   Суточная норма выловленной добычи не должна превышать 10 кг.\n\n   •   Кроме сома, можно ловить не более 1 экземпляра в одни руки.\n\n   •   Раков нельзя вылавливать больше 50 шт. При этом запрещено брать всех подряд. Особей меньше 10 см следует отпускать обратно.\n\n    Таким образом, рыбак может поймать каждого экземпляра рыбы не более 10 кг. В эту категорию, не попадает сом, так как его размеры могут быть весьма внушительные и не войти в обозначенные килограммы.'],
        ['Какую рыбу запрещено ловить', '    Под запретом в Астраханской области находятся следующие виды рыб:\n\n       •   осетровые;\n\n       •   Сельдь;\n\n       •   Рыбец;\n\n       •   Налим;\n\n       •   Усач.\n\n    Если рыбака поймают с таким уловом, то неприятностей ему не избежать.\n\n    Также действует запрет на перевозку и вывоз из региона рыбы определенных размеров:\n\n       •   Вобла, плотва. Рыба в длину не должна превышать 17 см.\n\n       •   Линь, чехонь – отлов рыбы производится при размере от 22 см.\n\n       •   Сом должен достигнуть в длину 60 см, иначе отлов запрещен.\n\n       •   Лещ. Рыба должна достигать 24 см.\n\n       •   Щука. Эту благородную рыбу можно ловить размером не более 32 см.\n\n       •   Сазан. Отлов рыбы можно производить, когда особь достигнет длины, как минимум, 40 см.\n\n       •   Рак. Нельзя ловить особей меньше 10 см.\n\n    За нарушение предусмотрена и административная, и уголовная ответственность. Нарушителям придется не только оплатить крупный штраф за запрещенные экземпляры, но и можно получить наказание, которое придется отбывать в местах лишения свободы.'],
        ['Размер штрафа за ловлю рыбы', '    При выборе дислокации для рыбалки, в каком бы районе она не находилась, необходимо предварительно уточнять информацию, где и когда возможно закинуть удочку. Незнание закона не поможет избежать наказания. А за некоторые нарушения можно получить довольно внушительный штраф. Не забывают и об уголовной ответственности. За нарушение правил вылова рыбы, размеры и суммы зависят от вида и редкости улова:\n\n       •   При нарушении запрета на вылов, штраф до 5 тыс. руб. При этом конфискуют удочки и другие средства лова.\n\n       •   При обнаружении в улове рыбака редкого или исчезающего вида рыб, ему грозит штраф до 1500 руб. и изъятие всех снастей.\n\n       •   При осуществлении лова рыбы в период нереста, это будет стоить рыболову от 100 до 300 тыс. руб.\n\n    Применение запрещенного вида орудия во время рыбалки в нерест и причинение крупного вреда заставит браконьера заплатить штраф в размере 300 тыс. руб.\n\n    Уголовная ответственность идет за браконьерские действия в крупных водоемах в период нереста с применением моторной лодки или яхты. Также, подобное поведение грозит рыбакам штрафом в размере 500 тыс. руб. или сроком до 2 лет лишения свободы. Отлов рыбы, занесенной в Красную книгу, запрещен. Это грозит браконьеру штрафом в районе 1 млн руб. или 3 годами тюрьмы.'],
        ['Когда можно оплатить штраф и где', '    В случае нарушения закона заполняют протокол и обозначают сумму штрафа, в зависимости от нарушения нарушителю предоставляют 10 суток для оплаты или, в случае несогласия, можно обратиться в суд, обжаловать решение. Но необходимо иметь существенные доказательства невиновности. Если в течение 5 месяцев не производится оплата штрафа, дело передается судебным приставам. В этом случае с гражданина взимается назначенная сумма в принудительном порядке.']
    ]

    def click_on_pre(self):
        Data.number_rule = Data.number_rule - 1
        if Data.number_rule < 0:
            Data.number_rule = 7
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        self.parent.current = 'RuleFishing'

    def click_on_menu(self):
        Data.screen_history.append('RuleFishing')
        self.parent.current = 'Rules'

    def click_on_next(self):
        Data.number_rule = Data.number_rule + 1
        if Data.number_rule > 7:
            Data.number_rule = 0
        self.parent.get_screen('RuleFishing').ids.zag.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][0]
        self.parent.get_screen('RuleFishing').ids.main_text.text = self.parent.get_screen('RuleFishing').data[Data.number_rule][1]
        self.parent.current = 'RuleFishing'

class Penalties(Screen):
    def click_on_state256(self):
        Data.number_penalties = 0
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state258(self):
        Data.number_penalties = 1
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state258_1(self):
        Data.number_penalties = 2
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_7(self):
        Data.number_penalties = 3
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_8(self):
        Data.number_penalties = 4
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_8_1(self):
        Data.number_penalties = 5
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state11_10(self):
        Data.number_penalties = 6
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_33(self):
        Data.number_penalties = 7
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_35(self):
        Data.number_penalties = 8
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state8_37(self):
        Data.number_penalties = 9
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state20_25(self):
        Data.number_penalties = 10
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_2(self):
        Data.number_penalties = 11
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_3(self):
        Data.number_penalties = 12
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

    def click_on_state18_7(self):
        Data.number_penalties = 13
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        Data.screen_history.append('Penalties')
        self.parent.current = 'PenaltieList'

class PenaltieList(Screen):
    zag = ObjectProperty()
    main_text = ObjectProperty()

    data = [
    ['Статья 256 УК РФ. Незаконная добыча (вылов) водных биологических ресурсов', '    1. Незаконная добыча (вылов) водных биологических ресурсов (за исключением водных биологических ресурсов континентального шельфа Российской Федерации и исключительной экономической зоны Российской Федерации), если это деяние совершено:\n\n       а) с причинением крупного ущерба;\n\n       б) с применением самоходного транспортного плавающего средства или взрывчатых и химических веществ, электротока или других запрещенных орудий и способов массового истребления водных биологических ресурсов;\n\n       в) в местах нереста или на миграционных путях к ним;\n\n       г) на особо охраняемых природных территориях либо в зоне экологического бедствия или в зоне чрезвычайной экологической ситуации, -\n\n    наказывается штрафом в размере от трехсот тысяч до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от двух до трех лет, либо обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо лишением свободы на тот же срок.\n\n    2. Незаконная добыча котиков, морских бобров или других морских млекопитающих в открытом море или в запретных зонах -\n\n    наказывается штрафом в размере от трехсот тысяч до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от двух до трех лет, либо обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо лишением свободы на тот же срок.\n\n    3. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные лицом с использованием своего служебного положения либо группой лиц по предварительному сговору или организованной группой либо причинившие особо крупный ущерб, -\n\n    наказываются штрафом в размере от пятисот тысяч до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет либо лишением свободы на срок от двух до пяти лет с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    Примечание. Крупным ущербом в настоящей статье признается ущерб, причиненный водным биологическим ресурсам, исчисленный по утвержденным Правительством Российской Федерации таксам, превышающий сто тысяч рублей, особо крупным - двести пятьдесят тысяч рублей.'],
    ['Статья 258 УК РФ. Незаконная охота', '    1. Незаконная охота, если это деяние совершено:\n\n       а) с причинением крупного ущерба;\n\n       б) с применением механического транспортного средства или воздушного судна, взрывчатых веществ, газов или иных способов массового уничтожения птиц и зверей;\n\n       в) в отношении птиц и зверей, охота на которых полностью запрещена;\n\n       г) на особо охраняемой природной территории либо в зоне экологического бедствия или в зоне чрезвычайной экологической ситуации, -\n\n    наказывается штрафом в размере до пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период до двух лет, либо исправительными работами на срок до двух лет, либо лишением свободы на срок до двух лет.\n\n    2. То же деяние, совершенное лицом с использованием своего служебного положения либо группой лиц по предварительному сговору или организованной группой, либо причинившее особо крупный ущерб, -\n\n    наказывается штрафом в размере от пятисот тысяч до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет либо лишением свободы на срок от трех до пяти лет с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    Примечание. Крупным ущербом в настоящей статье признается ущерб, исчисленный по утвержденным Правительством Российской Федерации таксам и методике, превышающий сорок тысяч рублей, особо крупным - сто двадцать тысяч рублей. '],
    ['Статья 258.1 УК РФ. Незаконные добыча и оборот особо ценных диких животных и водных биологических ресурсов', '\n\n    1. Незаконные добыча, содержание, приобретение, хранение, перевозка, пересылка и продажа особо ценных диких животных и водных биологических ресурсов, принадлежащих к видам, занесенным в Красную книгу Российской Федерации и (или) охраняемым международными договорами Российской Федерации, их частей и дериватов (производных) -\n\n    наказываются обязательными работами на срок до четырехсот восьмидесяти часов, либо исправительными работами на срок до двух лет, либо принудительными работами на срок до четырех лет со штрафом в размере до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период до двух лет или без такового и с ограничением свободы на срок до одного года или без такового, либо лишением свободы на срок до четырех лет со штрафом в размере до одного миллиона рублей или в размере заработной платы или иного дохода осужденного за период до двух лет или без такового и с ограничением свободы на срок до одного года или без такового.\n\n    1.1. Незаконные приобретение или продажа особо ценных диких животных и водных биологических ресурсов, принадлежащих к видам, занесенным в Красную книгу Российской Федерации и (или) охраняемым международными договорами Российской Федерации, их частей и дериватов (производных) с использованием средств массовой информации либо электронных или информационно-телекоммуникационных сетей, в том числе сети "Интернет", -\n\n    наказываются принудительными работами на срок до пяти лет со штрафом в размере от пятисот тысяч до одного миллиона пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от одного года до трех лет или без такового и с ограничением свободы на срок до двух лет или без такового либо лишением свободы на срок до пяти лет со штрафом в размере от пятисот тысяч до одного миллиона пятисот тысяч рублей или в размере заработной платы или иного дохода осужденного за период от одного года до трех лет или без такового и с ограничением свободы на срок до двух лет или без такового.\n\n    2. Деяния, предусмотренные частью первой настоящей статьи, совершенные:\n\n       а) лицом с использованием своего служебного положения;\n\n       б) с публичной демонстрацией, в том числе в средствах массовой информации или информационно-телекоммуникационных сетях (включая сеть "Интернет"), -\n\n    наказываются лишением свободы на срок до шести лет со штрафом в размере до двух миллионов рублей или в размере заработной платы или иного дохода осужденного за период до пяти лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до трех лет или без такового.\n\n    2.1. Деяния, предусмотренные частью первой настоящей статьи, совершенные лицом с использованием своего служебного положения, -\n\n    наказываются лишением свободы на срок от трех до семи лет со штрафом в размере от одного миллиона до трех миллионов рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до пяти лет или без такового.\n\n    3. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные группой лиц по предварительному сговору или организованной группой, -\n\n    наказываются лишением свободы на срок от пяти до восьми лет со штрафом в размере до двух миллионов рублей или в размере заработной платы или иного дохода осужденного за период до пяти лет или без такового, с ограничением свободы на срок до двух лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до пяти лет или без такового.\n\n    3.1. Деяния, предусмотренные частями первой или второй настоящей статьи, совершенные группой лиц по предварительному сговору или организованной группой, -\n\n    наказываются лишением свободы на срок от шести до девяти лет со штрафом в размере от одного миллиона пятисот тысяч до трех миллионов рублей или в размере заработной платы или иного дохода осужденного за период от трех до пяти лет или без такового, с ограничением свободы на срок до двух лет или без такового и с лишением права занимать определенные должности или заниматься определенной деятельностью на срок до семи лет или без такового.'],
    ['Статья 11.7. Нарушение правил плавания', '    1. Нарушение судоводителем или иным лицом, управляющим судном (за исключением маломерного) на морском, внутреннем водном транспорте, правил плавания и стоянки судов, входа судов в порт и выхода их из порта, за исключением случаев, предусмотренных частью 3 настоящей статьи, буксировки составов и плотов, подачи звуковых и световых сигналов, несения судовых огней и знаков -\n\n    влечет наложение административного штрафа в размере от пяти тысяч до десяти тысяч рублей или лишение права управления судном на срок от шести месяцев до одного года.\n\n       1.1. Повторное в течение года совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, -\n\n    влечет наложение административного штрафа в размере от десяти тысяч до двадцати тысяч рублей или лишение права управления судном на срок от одного года до двух лет.\n\n    2. Превышение судоводителем или иным лицом, управляющим маломерным судном, установленной скорости, несоблюдение требований навигационных знаков, преднамеренная остановка или стоянка судна в запрещенных местах либо нарушение правил маневрирования, подачи звуковых сигналов, несения бортовых огней и знаков -\n\n    влечет предупреждение, или наложение административного штрафа в размере от пятисот до одной тысячи рублей, или лишение права управления маломерным судном на срок до шести месяцев.\n\n    3. Осуществление капитаном судна плавания без лоцмана в районах обязательной лоцманской проводки судов, за исключением случаев, если судно относится к категории судов, освобождаемых от обязательной лоцманской проводки, или капитану судна предоставлено право осуществлять плавание без лоцмана капитаном морского порта в установленном порядке, -\n\n    влечет наложение административного штрафа в размере от двадцати тысяч до двадцати пяти тысяч рублей или лишение права управления судном на срок до трех месяцев.\n\n    4. Необъявление или неправильное объявление капитаном судна лоцману данных об осадке, о длине, ширине и вместимости судна и иных данных о судне, которые необходимы лоцману для осуществления лоцманской проводки судна, -\n\n    влечет наложение административного штрафа в размере от одной тысячи до трех тысяч рублей или лишение права управления судном на срок до трех месяцев.\n\n    Примечание. Под маломерным судном в настоящем Кодексе следует понимать судно, длина которого не должна превышать двадцать метров и общее количество людей, на котором не должно превышать двенадцать.'],
    ['Статья 11.8. Нарушение правил эксплуатации судов, а также управление судном лицом, не имеющим права управления', '    1. Управление судном (в том числе маломерным, подлежащим государственной регистрации), не прошедшим технического осмотра (освидетельствования), либо не несущим бортовых номеров или обозначений, либо переоборудованным без соответствующего разрешения или с нарушением норм пассажировместимости, ограничений по району и условиям плавания, за исключением случаев, предусмотренных частью 3 настоящей статьи, -\n\n    влечет наложение административного штрафа в размере от пяти тысяч до десяти тысяч рублей.\n\n    2. Управление судном лицом, не имеющим права управления этим судном, или передача управления судном лицу, не имеющему права управления, -\n\n    влечет наложение административного штрафа в размере от десяти тысяч до пятнадцати тысяч рублей.\n\n    3. Управление судном (в том числе маломерным, подлежащим государственной регистрации), не зарегистрированным в установленном порядке либо имеющим неисправности, с которыми запрещена его эксплуатация, -\n\n    влечет наложение административного штрафа в размере от пятнадцати тысяч до двадцати тысяч рублей. '],
    ['Статья 11.8.1. Управление маломерным судном судоводителем, не имеющим при себе документов, необходимых для допуска к управлению маломерным судном', '    1. Управление маломерным судном судоводителем, не имеющим при себе удостоверения на право управления маломерным судном, судового билета маломерного судна или его копии, заверенной в установленном порядке, а равно документов, подтверждающих право владения, пользования или распоряжения управляемым им судном в отсутствие владельца, -\n\n    влечет предупреждение или наложение административного штрафа в размере ста рублей.\n\n    За совершение данного правонарушения в соответствии со статьей 27.13 настоящего Кодекса применяется задержание транспортного средства, помещение на специализированную стоянку\n\n    2. Передача управления маломерным судном лицу, не имеющему при себе удостоверения на право управления маломерным судном, -\n\n    влечет предупреждение или наложение административного штрафа в размере ста рублей.'],
    ['Статья 11.10. Нарушение правил обеспечения безопасности пассажиров на судах водного транспорта, а также на маломерных судах', '    Нарушение правил обеспечения безопасности пассажиров при посадке на суда, в пути следования и при их высадке с судов водного транспорта либо с маломерных судов -\n\n    влечет наложение административного штрафа на граждан в размере от трехсот до пятисот рублей; на должностных лиц - от пятисот до одной тысячи рублей.'],
    ['Статья 8.33. Нарушение правил охраны среды обитания или путей миграции объектов животного мира и водных биологических ресурсов', '    Нарушение правил охраны среды обитания или путей миграции объектов животного мира и водных биологических ресурсов -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от двух тысяч до пяти тысяч рублей; на должностных лиц - от пяти тысяч до десяти тысяч рублей; на юридических лиц - от десяти тысяч до пятнадцати тысяч рублей. '],
    ['Статья 8.35. Уничтожение редких и находящихся под угрозой исчезновения видов животных или растений', '    Уничтожение редких и находящихся под угрозой исчезновения видов животных или растений, занесенных в Красную книгу Российской Федерации либо охраняемых международными договорами, а равно действия (бездействие), которые могут привести к гибели, сокращению численности либо нарушению среды обитания этих животных или к гибели таких растений, либо добыча, хранение, перевозка, сбор, содержание, приобретение, продажа либо пересылка указанных животных или растений, их продуктов, частей либо дериватов без надлежащего на то разрешения или с нарушением условий, предусмотренных разрешением, либо с нарушением иного установленного порядка, если эти действия не содержат уголовно наказуемого деяния, -\n\n    влечет наложение административного штрафа на граждан в размере от двух тысяч пятисот до пяти тысяч рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой; на должностных лиц - от пятнадцати тысяч до двадцати тысяч рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой; на юридических лиц - от пятисот тысяч до одного миллиона рублей с конфискацией орудий добычи животных или растений, а также самих животных или растений, их продуктов, частей либо дериватов или без таковой.'],
    ['Статья 8.37. Нарушение правил охоты, правил, регламентирующих рыболовство и другие виды пользования объектами животного мира', '    1. Нарушение правил охоты, за исключением случаев, предусмотренных частями 1.2, 1.3 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от пятисот до четырех тысяч рублей с конфискацией орудий охоты или без таковой или лишение права осуществлять охоту на срок до двух лет; на должностных лиц - от двадцати тысяч до тридцати пяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n       1.1. Повторное в течение года совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от 4 000 до 5 000 рублей с конфискацией орудий охоты или без таковой или лишение права осуществлять охоту на срок от одного года до трех лет; на должностных лиц - от тридцати пяти тысяч до пятидесяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n    1.2. Осуществление охоты с нарушением установленных правилами охоты сроков охоты, за исключением случаев, если допускается осуществление охоты вне установленных сроков, либо осуществление охоты недопустимыми для использования орудиями охоты или способами охоты -\n\n    влечет для граждан лишение права осуществлять охоту на срок от одного года до двух лет; наложение административного штрафа на должностных лиц в размере от тридцати пяти тысяч до пятидесяти тысяч рублей с конфискацией орудий охоты или без таковой.\n\n       1.3. Непредъявление по требованию должностных лиц органов, уполномоченных в области охраны, контроля и регулирования использования объектов животного мира (в том числе отнесенных к охотничьим ресурсам) и среды их обитания, органов, осуществляющих функции по контролю в области организации и функционирования особо охраняемых природных территорий федерального значения, государственных учреждений, находящихся в ведении органов исполнительной власти субъектов Российской Федерации, осуществляющих государственный охотничий надзор, функции по охране, контролю и регулированию использования объектов животного мира и среды их обитания, других уполномоченных в соответствии с законодательством Российской Федерации должностных лиц, производственных охотничьих инспекторов охотничьего билета, разрешения на добычу охотничьих ресурсов, путевки либо разрешения на хранение и ношение охотничьего оружия в случае осуществления охоты с охотничьим огнестрельным и (или) пневматическим оружием -\n\n    влечет для граждан лишение права осуществлять охоту на срок от одного года до двух лет; наложение административного штрафа на должностных лиц в размере от двадцати пяти тысяч до сорока тысяч рублей с конфискацией орудий охоты или без таковой.\n\n    2. Нарушение правил, регламентирующих рыболовство, за исключением случаев, предусмотренных частью 2 статьи 8.17 настоящего Кодекса, -\n\n    влечет наложение административного штрафа на граждан в размере от двух тысяч до пяти тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой; на должностных лиц - от двадцати тысяч до тридцати тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой; на юридических лиц - от ста тысяч до двухсот тысяч рублей с конфискацией судна и других орудий добычи (вылова) водных биологических ресурсов или без таковой.\n\n    3. Нарушение правил пользования объектами животного мира, за исключением случаев, предусмотренных частями 1 - 2 настоящей статьи, -\n\n    влечет наложение административного штрафа на граждан в размере от пятисот до одной тысячи рублей с конфискацией орудий добывания животных или без таковой; на должностных лиц - от двух тысяч пятисот до пяти тысяч рублей с конфискацией орудий добывания животных или без таковой; на юридических лиц - от пятидесяти тысяч до ста тысяч рублей с конфискацией орудий добывания животных или без таковой. '],
    ['Статья 20.25. Уклонение от исполнения административного наказания', '    1. Неуплата административного штрафа в срок, предусмотренный настоящим Кодексом, -\n\n    влечет наложение административного штрафа в двукратном размере суммы неуплаченного административного штрафа, но не менее одной тысячи рублей, либо административный арест на срок до пятнадцати суток, либо обязательные работы на срок до пятидесяти часов.\n\n    2. Самовольное оставление места отбывания административного ареста или уклонение от отбывания административного ареста-влечет административный арест на срок до пятнадцати суток либо обязательные работы на срок до пятидесяти часов.\n\n    3. Уклонение иностранного гражданина или лица без гражданства от исполнения административного наказания в виде административного выдворения за пределы Российской Федерации в форме контролируемого самостоятельного выезда из Российской Федерации -\n\n    влечет наложение административного штрафа в размере от трех тысяч до пяти тысяч рублей и административное выдворение за пределы Российской Федерации.\n\n    4. Уклонение от отбывания обязательных работ -\n\n    влечет наложение административного штрафа в размере от ста пятидесяти тысяч до трехсот тысяч рублей или административный арест на срок до пятнадцати суток.\n\n    5. Нарушение административного запрета на посещение мест проведения официальных спортивных соревнований в дни их проведения -\n\n    влечет наложение административного штрафа в размере от сорока тысяч до пятидесяти тысяч рублей или административный арест на срок от десяти до пятнадцати суток.\n\n    Примечания:\n\n       1. К административной ответственности за совершение административного правонарушения, предусмотренного частью 1 настоящей статьи, не привлекаются иностранные граждане и лица без гражданства в случае, если они своевременно не уплатили административный штраф, который был назначен им одновременно с административным выдворением за пределы Российской Федерации.\n\n       2. Административное выдворение за пределы Российской Федерации иностранного гражданина или лица без гражданства в форме контролируемого самостоятельного выезда из Российской Федерации не применяется к иностранным гражданам и лицам без гражданства, привлекаемым к административной ответственности за административное правонарушение, предусмотренное частью 3 настоящей статьи.\n\n       3. Административный арест, предусмотренный частью 1 настоящей статьи, не может применяться к лицу, которое не уплатило административный штраф за совершение административного правонарушения, предусмотренного главой 12 настоящего Кодекса и зафиксированного с применением работающих в автоматическом режиме специальных технических средств, имеющих функции фото- и киносъемки, видеозаписи, или средств фото- и киносъемки, видеозаписи. '],
    ['Статья 18.2. Нарушение пограничного режима в пограничной зоне', '\n\n    1. Нарушение правил въезда (прохода) в пограничную зону, временного пребывания, передвижения лиц и (или) транспортных средств в пограничной зоне -\n\n    влечет предупреждение или наложение административного штрафа в размере от пятисот до одной тысячи рублей.\n\n       1.1. Те же действия, совершенные иностранным гражданином или лицом без гражданства, -\n\n    влекут предупреждение или наложение административного штрафа в размере от пятисот до одной тысячи рублей с административным выдворением за пределы Российской Федерации или без такового.\n\n    2. Ведение хозяйственной, промысловой или иной деятельности либо проведение массовых общественно-политических, культурных или иных мероприятий в пограничной зоне, а равно содержание или выпас скота в карантинной полосе в пределах пограничной зоны без разрешения пограничных органов либо с разрешения таких органов, но с нарушением установленного порядка ведения хозяйственной, промысловой или иной деятельности либо нарушение порядка проведения массовых общественно-политических, культурных или иных мероприятий в пограничной зоне -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от трехсот до одной тысячи рублей; на должностных лиц - от двух тысяч до пяти тысяч рублей; на юридических лиц - от пяти тысяч до десяти тысяч рублей. '],
    ['Статья 18.3. Нарушение пограничного режима в территориальном море и во внутренних морских водах Российской Федерации', '    1. Нарушение установленных в территориальном море и во внутренних морских водах Российской Федерации, в российской части вод пограничных рек, озер и иных водных объектов правил учета, хранения, выхода из пунктов базирования и возвращения в пункты базирования, пребывания на водных объектах российских маломерных самоходных и несамоходных (надводных и подводных) судов (средств) или средств передвижения по льду -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от пятисот до одной тысячи рублей; на должностных лиц - от двух тысяч до пяти тысяч рублей; на юридических лиц - от пяти тысяч до десяти тысяч рублей.\n\n    2. Ведение в территориальном море и во внутренних морских водах Российской Федерации, в российской части вод пограничных рек, озер и иных водных объектов промысловой, исследовательской, изыскательской и иной деятельности без разрешения (уведомления) пограничных органов либо с разрешения (с уведомлением) таких органов, но с нарушением условий такого разрешения (уведомления) -\n\n    влечет предупреждение или наложение административного штрафа на граждан в размере от трехсот до одной тысячи рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой; на должностных лиц - от двух тысяч до пяти тысяч рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой; на юридических лиц - от восьми тысяч до двенадцати тысяч рублей с конфискацией орудий совершения или предмета административного правонарушения или без таковой. '],
    ['Статья 18.7. Неповиновение законному распоряжению или требованию военнослужащего в связи с исполнением им обязанностей по охране Государственной границы Российской Федерации', '    Неповиновение законному распоряжению или требованию военнослужащего в связи с исполнением им обязанностей по охране Государственной границы Российской Федерации -\n\n    влечет наложение административного штрафа в размере от одной тысячи до одной тысячи пятисот рублей или административный арест на срок до пятнадцати суток.']
    ]

    def click_on_pre(self):
        Data.number_penalties = Data.number_penalties - 1
        if Data.number_penalties < 0:
            Data.number_penalties = 13
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        self.parent.current = 'PenaltieList'

    def click_on_menu(self):
        Data.screen_history.append('PenaltieList')
        self.parent.current = 'Penalties'

    def click_on_next(self):
        Data.number_penalties = Data.number_penalties + 1
        if Data.number_penalties > 13:
            Data.number_penalties = 0
        self.parent.get_screen('PenaltieList').ids.zag.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][0]
        self.parent.get_screen('PenaltieList').ids.main_text.text = self.parent.get_screen('PenaltieList').data[Data.number_penalties][1]
        self.parent.current = 'PenaltieList'

class Esox(Screen):
    def click_weapon(self, fish):
        self.parent.get_screen('Weapon').ids.main_text.text = self.parent.get_screen('Weapon').data[1]
        self.parent.current = 'Weapon'

class Silurus(Screen):
    def click_weapon(self, fish):
        self.parent.get_screen('Weapon').ids.main_text.text = self.parent.get_screen('Weapon').data[1]
        self.parent.current = 'Weapon'

class Cyprinus(Screen):
    def click_weapon(self, fish):
        self.parent.get_screen('Weapon').ids.main_text.text = self.parent.get_screen('Weapon').data[1]
        self.parent.current = 'Weapon'

class Weapon(Screen):
    data = [
        "    Ссылка на описание любительских орудий лова, применяемые для ловли сазана в Правилах рыболовства:\n    - донная удочка (донка), состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской или шнуром) или хлыстика, лески или шнура, грузила, поводков и крючков;\n    - донная удочка, состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской и шнуром) или хлыстика, лески, грузила, кормушки или жмыхоловки с количеством крючков не более 2-х штук. \n    Описание любительских орудий лова для пользователей, применяемые для ловли сазана: \n    - донная удочка для ловли сазана («жмыхоловка»). Сазаньи «донки» в зависимости от применяемой оснастки подразделяются на бойловые и жмыховые. Сазанья оснастка для бойлового ужения отличается от жмыховой как правилом наличием одного карпового крючка, а также волоска (тонкой лески), соединяющий крючок и бойл. Конструктивной особенностью донной удочки жмыхового типа, отличающей её от донок остальных модификаций, является применение в конструкции грузила со сквозным отверстием, что позволяет размещать жмых или макуху под грузом, а также наличие обычно двух коротких поводков с карповыми крючками на концах,которые, как правило, насаживаются на жмых. ",
        "    Ссылка на описание любительских орудий лова, применяемые для ловли щуки в Правилах рыболовства:\n    - спиннинговая снасть (спиннинг), состоит из удилища с пропускными кольцами и рукояткой, на которой крепится съемная катушка с леской или шнуром и оснащается одной приманкой с крючками (одинарными, двойниками или тройниками). Дополнительно перед приманкой может ставиться грузило без крючков.\n    - блесны, воблеры, мушки и другие приманки, разные по форме и цвету с крючками (одинарными, двойниками или тройниками);\n    - жерлицы;\n    - крючки-двойники или крючки-тройники применяются только при добыче (вылове) спиннингом и жерлицей. \n    Описание любительских орудий лова для пользователей, применяемые для ловли щуки:\n    - ужение спиннингом искусственными насадками. В качестве оснасток в основном применяются разные типы искусственных насадок: блесны (легкие – щучьи, вращающиеся, колеблющиеся и т.д.), воблеры, попперы, джиголовки и т. д.\n    - донная «живцовая» удочка применяется  для ловли хищных рыб, в том числе и щуки, используя в качестве приманки малька рыб мелких частиковых пород, лягушек, личинок жуков, саранчу. Конструктивной особенностью «живцовой» донки является наличие одного 1-1,5 м поводка с одинарным крючком на конце. Существует два способа лова донки «на живца»: стационарный и сплавом. Способ стационарного лова заключается в ужении рыбы с берега или с лодки, стоящей на якорях. Обычно выставляется несколько орудий лова (от 2 до 5 шт.). Самая популярная насадка – малёк.\n    - жерлицы (кружки). Несмотря на популярность спиннинга и разнообразие искусственных приманок на него, все же определенная часть рыбаков предпочитает вылавливать щуку на живца с использованием жерлиц. Жерлицы для рыбалки подразделяют на летние и зимние.\n    Летние жерлицы или кружки. Суть этого способа ловли заключается в поиске детали конструкции, на которые получится накрутить необходимую длину лески. Этим предметом может стать пластиковая бутылка, деревянный элемент или пластмассовый круг, способный плавать на поверхности воды. \n    Принцип действия жерлиц для зимней рыбалки состоит в том, что на крючок, двойник или тройник насаживается живая приманка, которая опускается в лунку в воду. Голодный хищник захватывает наживку и отходит немного в сторону, для того, чтобы ее проглотить. В этот момент с катушки начинает активно разматываться леска, и срабатывает пружинка или другой световой сигнал. В Астраханской области распространена жерлица, состоящая из лески, палки (куска ветки) и крючка. Палка (кусок ветки) служит и катушкой, и сигнализатором поклевки одновременно. Нахождение палки в лунке говорит о поклевке и возможной поимке хищника.",
        "    Ссылка на описание любительских орудий лова, применяемые для ловли сома в Правилах рыболовства:\n    - донная удочка (донка), состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской или шнуром) или хлыстика, лески или шнура, грузила, поводков и крючков;\n    - донная удочка, состоящая из удилища (в том числе с пропускными кольцами и съемной катушкой с леской и шнуром) или хлыстика, лески, грузила, кормушки или жмыхоловки с количеством крючков не более 2-х штук;\n    - добыча (вылов) рыбы 'на квок';\n    Описание любительских орудий лова для пользователей, применяемые для ловли сома:\n    - донная «живцовая» удочка применяется  для хищных рыб, в том числе и сома, используя в качестве приманки малька рыб мелких частиковых пород, лягушек, личинок жуков, саранчу. Конструктивной особенностью «живцовой» донки является наличие одного 1-1,5 м поводка с одинарным крючком на конце. Существует два способа лова донки «на живца»: стационарный и сплавом. Способ стационарного лова заключается в ужении рыбы с берега или с лодки, стоящей на якорях. Обычно выставляется несколько орудий лова (от 2 до 5 шт.). Самая популярная насадка – малёк. \n    - метод сплава – так называемый лов на «квок», широко распространённый способ лова у рыболовов-любителей в Астраханской области. Основные наживки – лягушки, саранча и т.д."
    ]
    main_text = ObjectProperty()

    def entering(self):
        self.main_text.text = self.data[Data.fish_number]

class CatalogFish(Screen):
    def __init__(self, **kwargs):
        super(CatalogFish, self).__init__(**kwargs)

    def click_on_button_esox(self):
        Data.screen_history.append('CatalogFish')
        self.parent.current = 'Esox'

    def click_on_button_silurus(self):
        Data.screen_history.append('CatalogFish')
        self.parent.current = 'Silurus'

    def click_on_button_cyprinus(self):
        Data.screen_history.append('CatalogFish')
        self.parent.current = 'Cyprinus'

class Recipes(Screen):
    pass

class CustomMenuBlock(Screen, MDFloatLayout):
    pass

class CustomBottomSheet(Screen, MDBoxLayout):
    image_allowed = ObjectProperty()
    image_disallowed = ObjectProperty()
    image_shops = ObjectProperty()

class ContentMarkerAllowed(Screen):
    pass

class ContentMarkerDisAllowed(Screen):
    subInfo = StringProperty()

    def __init__(self, **kwargs):
        super(ContentMarkerDisAllowed, self).__init__(**kwargs)

        if Data.is_polygon:
            self.subInfo = Data.polygon_text
            Data.is_polygon = False

class ContentMarkerShops(Screen):
    pass

class CustomFishLayers(Screen):
    but_silurus = ObjectProperty()
    but_cyprinus = ObjectProperty()

class ContentMarkerSilurus(Screen):
    pass

class ContentMarkerCyprinus(Screen):
    pass

#define different screens
class GPSHelper(Screen):
    input_search = ObjectProperty()
    main_map = ObjectProperty()
    
    fishing_allowed = False
    fishing_disallowed = False
    fishing_shops = False

    silurus = False
    cyprinus = False

    def __init__(self, **kwargs):
        super(GPSHelper, self).__init__(**kwargs)

        @mainthread
        def delayed():
            self.main_map.bind(on_touch_down=self.click_on_map)
        delayed()

        self.source_street = MapSource(url='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}')
        self.source_satellite = MapSource(url='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}')
        self.source_hybrid = MapSource(url='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}')

        source_fishing_allowed = 'resources/layers/fishing_allowed.geojson'
        source_fishing_disallowed = 'resources/layers/fishing_disallowed.geojson'
        source_fishing_shops = 'resources/layers/fishing_shops.geojson'
        source_silurus = 'resources/layers/silurus.geojson'
        source_cyprinus = 'resources/layers/cyprinus.geojson'
        
        self.layer_polygon_disallowed = GeoJsonMapLayer(source=source_fishing_disallowed)
        self.layer_fishing_allowed = MarkerMapLayer()
        self.layer_fishing_disallowed = MarkerMapLayer()
        self.layer_fishing_shops = MarkerMapLayer()
        self.layer_silurus = MarkerMapLayer()
        self.layer_cyprinus = MarkerMapLayer()
        self.layer_fish_resort = MarkerMapLayer()
        self.layer_fishka = MarkerMapLayer()
        self.layer_caspiy_unic = MarkerMapLayer()
        self.layer_fish_portal = MarkerMapLayer()

        self.layer_fish_portal.add_widget(MapMarker(lon=48.03526818752289, lat=46.32747782427445, source='resources/pictures/marker.png'))

        self.layer_caspiy_unic.add_widget(MapMarker(lon=48.03745687007904, lat=46.4956595690788, source='resources/pictures/marker.png'))

        self.layer_fishka.add_widget(MapMarker(lon=47.99520134925842, lat=46.46676590440685, source='resources/pictures/marker.png'))

        self.layer_fish_resort.add_widget(MapMarker(lon=46.748611, lat=47.815556, source='resources/pictures/marker.png'))

        self.layer_silurus.add_widget(MapMarker(lon=47.948970794677734, lat=46.56228323662375, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=48.008880615234375, lat = 46.53253190986272, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=48.03926467895508, lat = 46.52745366594394, source='resources/map_sign/fish.png', on_release=self.markerSilurus))
        self.layer_silurus.add_widget(MapMarker(lon=47.99600601196288, lat = 46.55874226707572, source='resources/map_sign/fish.png', on_release=self.markerSilurus))

        self.layer_cyprinus.add_widget(MapMarker(lon=48.013343811035156, lat = 46.481373492133784, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=48.02999496459961, lat=46.50193716468582, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=47.97025680541992, lat=46.46257575132626, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=47.9611587524414, lat=46.49141993572272, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))
        self.layer_cyprinus.add_widget(MapMarker(lon=48.005104064941406, lat=46.409931207495845, source='resources/map_sign/fish.png', on_release=self.markerCyprinus))

        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.948970794677734, lat=46.56228323662375, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.008880615234375, lat=46.53253190986272, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.03926467895508, lat=46.52745366594394, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.99600601196288, lat=46.55874226707572, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.013343811035156, lat=46.481373492133784, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.02999496459961, lat=46.50193716468582, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.97025680541992, lat=46.46257575132626, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=47.9611587524414, lat=46.49141993572272, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))
        self.layer_fishing_allowed.add_widget(MapMarker(lon=48.005104064941406, lat=46.409931207495845, source='resources/map_sign/fishing_allowed_mark.png', on_release=self.markerAllowedPressed))

        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.95463562011719, lat=46.528162286622035, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01574707031249, lat=46.527689873863785, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=48.01300048828125, lat=46.50264611816897, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.99171447753906, lat=46.49177448218621, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.97557830810547, lat=46.500519229985045, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.96424865722656, lat=46.50099187899411, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))
        self.layer_fishing_disallowed.add_widget(MapMarker(lon=47.976951599121094, lat=46.53359473803679, source='resources/map_sign/fishing_disallowed_mark.png', on_release=self.markerDisAllowedPressed))

        self.layer_fishing_shops.add_widget(MapMarker(lon=47.99520134925842, lat=46.46676590440685, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03745687007904, lat=46.4956595690788, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.069820404052734, lat=46.36908189730966, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))
        self.layer_fishing_shops.add_widget(MapMarker(lon=48.03526818752289, lat=46.32747782427445, source='resources/map_sign/fishing_shops_mark.png', on_release=self.markerShopsPressed))

    def click_on_button_go_to_penalti(self):
        if not Data.urlToPenalti == None:
            Data.number_rule = 1
            self.parent.get_screen(Data.urlToPenalti).ids.zag.text = self.parent.get_screen(Data.urlToPenalti).data[Data.number_rule][0]
            self.parent.get_screen(Data.urlToPenalti).ids.main_text.text = self.parent.get_screen(Data.urlToPenalti).data[Data.number_rule][1]
            Data.screen_history.append('GPSHelper')
            self.parent.current = Data.urlToPenalti
            Data.urlToPenalti = None
            self.menu_marker_disallowed.dismiss()

    def click_on_map(self, widget, touch):
        if self.fishing_disallowed:
            if touch.is_double_tap:
                coord_click = self.main_map.get_latlon_at(touch.x, touch.y, self.main_map.zoom)
        
                point = Point(coord_click.lon, coord_click.lat)
                with open('resources/layers/fishing_disallowed.geojson') as f:
                    data = json.load(f)
        
                featureChoosen = None
                for feature in data['features']:
                    alpha_shape = Polygon((feature['geometry']['coordinates'][0]))
                    if alpha_shape.contains(point):
                        featureChoosen = feature
                        break
                Data.polygon_text = featureChoosen['properties']['name']
                Data.urlToPenalti = featureChoosen['properties']['penalti_url']
                Data.is_polygon = True
                self.menu_marker_disallowed = MDCustomBottomSheet(screen=Factory.ContentMarkerDisAllowed())
                self.menu_marker_disallowed.open()

    def markerSilurus(self,widget):
        self.menu_marker_silurus = MDCustomBottomSheet(screen = Factory.ContentMarkerSilurus())
        self.menu_marker_silurus.open()

    def markerCyprinus(self, widget):
        self.menu_marker_cyprinus = MDCustomBottomSheet(screen = Factory.ContentMarkerCyprinus())
        self.menu_marker_cyprinus.open()

    def markerAllowedPressed(self, widget):
        self.menu_marker_allowed = MDCustomBottomSheet(screen = Factory.ContentMarkerAllowed())
        self.menu_marker_allowed.open()

    def markerDisAllowedPressed(self, widget):
        self.menu_marker_disallowed = MDCustomBottomSheet(screen = Factory.ContentMarkerDisAllowed())
        self.menu_marker_disallowed.open()

    def markerShopsPressed(self, widget):
        self.menu_marker_shops = MDCustomBottomSheet(screen = Factory.ContentMarkerShops())
        self.menu_marker_shops.open()

    def center_from_marker(self, lon, lat): 
        min_lon, max_lon, min_lat, max_lat = lon-1, lon+1, lat-1, lat+1
        radius = haversine(min_lon, min_lat, max_lon, max_lat)
        self.main_map.zoom = get_zoom_for_radius(radius, lat)

    def centering(self, layer):
        lon, lat = layer.center
        min_lon, max_lon, min_lat, max_lat = layer.bounds
        radius = haversine(min_lon, min_lat, max_lon, max_lat)
        self.main_map.zoom = get_zoom_for_radius(radius, lat)

    def click_silurus(self, widget):
        if self.silurus:
            self.silurus = False
            self.main_map.remove_layer(self.layer_silurus)
            widget.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        else:
            self.silurus = True
            self.main_map.add_layer(self.layer_silurus)
            self.layer_silurus.reposition()
            widget.md_bg_color = MDApp.get_running_app().theme_cls.primary_color
        
    def click_cyprinus(self, widget):
        if self.cyprinus:
            self.cyprinus = False
            self.main_map.remove_layer(self.layer_cyprinus)
            widget.md_bg_color = (241/255, 244/255, 250/255, 1.0)
        else:
            self.cyprinus = True
            self.main_map.add_layer(self.layer_cyprinus)
            self.layer_cyprinus.reposition()
            widget.md_bg_color = MDApp.get_running_app().theme_cls.primary_color

    def click_fishing_allowed(self, widget):
        if self.fishing_allowed:
            self.fishing_allowed = False
            self.main_map.remove_layer(self.layer_fishing_allowed)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_allowed_off.png'
        else:
            self.fishing_allowed = True
            self.main_map.add_layer(self.layer_fishing_allowed)
            self.layer_fishing_allowed.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_allowed_on.png'

    def showFishPortal(self):
        self.main_map.add_layer(self.layer_fish_portal)
        self.main_map.center_on(self.layer_fish_portal.children[0].lat, self.layer_fish_portal.children[0].lon)
        self.layer_fish_portal.reposition()

    def showCaspiyUnic(self):
        self.main_map.add_layer(self.layer_caspiy_unic)
        self.main_map.center_on(self.layer_caspiy_unic.children[0].lat, self.layer_caspiy_unic.children[0].lon)
        self.layer_caspiy_unic.reposition()

    def showFishka(self):
        self.main_map.add_layer(self.layer_fishka)
        self.main_map.center_on(self.layer_fishka.children[0].lat, self.layer_fishka.children[0].lon)
        self.layer_fishka.reposition()

    def showFishResort(self):
        self.main_map.add_layer(self.layer_fish_resort)
        self.main_map.center_on(self.layer_fish_resort.children[0].lat, self.layer_fish_resort.children[0].lon)
        self.layer_fish_resort.reposition()

    def click_fishing_disallowed(self, widget):
        if self.fishing_disallowed:
            self.fishing_disallowed = False
            self.main_map.remove_layer(self.layer_polygon_disallowed)
            self.main_map.remove_layer(self.layer_fishing_disallowed)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_disallowed_off.png'
        else:
            self.fishing_disallowed = True
            self.centering(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_polygon_disallowed)
            self.main_map.add_layer(self.layer_fishing_disallowed)
            self.layer_fishing_disallowed.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_disallowed_on.png'

    def click_fishing_shops(self, widget):
        if self.fishing_shops:
            self.fishing_shops = False
            self.main_map.remove_layer(self.layer_fishing_shops)
            widget.children[0].children[0].source = 'resources/map_sign/fishing_shop_off.png'
        else:
            self.fishing_shops = True
            self.main_map.add_layer(self.layer_fishing_shops)
            self.layer_fishing_shops.reposition()
            widget.children[0].children[0].source = 'resources/map_sign/fishing_shop_on.png'

    def click_on_button_gps(self):
        Dialog('Вы уже на данной странице', 'Внимание!')

    def click_on_button_note(self):
        try:
            self.main_map.remove_layer(self.layer_fish_resort)
            self.main_map.remove_layer(self.layer_fishka)
            self.main_map.remove_layer(self.leyer_caspiy_unic)
            self.main_map.remove_layer(self.layer_fish_portal)
        except:
            pass
        self.menu_block = MDCustomBottomSheet(screen = Factory.CustomMenuBlock())
        self.menu_block.open()

    def close_menu(self):
        self.menu_block.dismiss()

    def click_on_button_plus(self):
        self.parent.current = 'News'
        Data.screen_history.append('GPSHelper')

    def click_on_button_user(self):
        Data.screen_history.append('GPSHelper')
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
        Data.screen_history.append('GPSHelper')

        self.parent.current = 'Calendar'

    def click_on_button_fish(self):
        self.fish_layers = MDCustomBottomSheet(screen = Factory.CustomFishLayers())
        if self.silurus:
            self.fish_layers.children[0].children[0].children[0].ids.but_silurus.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
        if self.cyprinus:
            self.fish_layers.children[0].children[0].children[0].ids.but_silurus.md_bg_color = MDApp().get_running_app().theme_cls.primary_color
        self.fish_layers.open()

    def click_on_button_userGps(self):
        Dialog('Функция гео-локации в разработке', 'Внимание')

    def click_on_button_layers(self):
        self.layers = MDCustomBottomSheet(screen = Factory.CustomBottomSheet())
        if self.fishing_allowed:
            self.layers.children[0].children[0].children[0].ids.image_allowed.source = 'resources/map_sign/fishing_allowed_on.png'
        if self.fishing_disallowed:
            self.layers.children[0].children[0].children[0].ids.image_disallowed.source = 'resources/map_sign/fishing_disallowed_on.png'
        if self.fishing_shops:
            self.layers.children[0].children[0].children[0].ids.image_shops.source = 'resources/map_sign/fishing_shop_on.png'
        self.layers.open()

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
        #Data.save_info(surname=self.input_surname.text, name=self.input_name.text, lastname=self.input_lastname.text, mail=self.input_mail.text, phone=self.input_phone.text)
        self.parent.current = 'RegistrationDop'

    def click_on_button_terms_and_agreements(self):
        #Data.save_info(surname=self.input_surname.text, name=self.input_name.text, lastname=self.input_lastname.text, mail=self.input_mail.text, phone=self.input_phone.text)
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
                                    conn = SQLCommander.connect('resources/DB/user_db.db')
                                    curr = conn.cursor()
                                    curr.execute("SELECT * from Users WHERE phone="+self.input_phone.text)

                                    allItems = list(curr.fetchall())

                                    flag = True
                                    for i in range(len(allItems)):
                                        if allItems[i][5] == self.input_phone.text:
                                            flag = False
                                    if flag:
                                        conn = None
                                        flag = True
                                        try:
                                            conn = SQLCommander.connect('resources/DB/user_db.db')
                                            curr = conn.cursor()
                                            curr.execute("INSERT INTO Users VALUES (NULL, '"+self.input_surname.text+"', '"+self.input_name.text+"', '"+self.input_lastname.text+"', '"+self.input_mail.text+"', '"+self.input_phone.text+"')")
                                            conn.commit()
                                        except SQLCommander.Error as e:
                                            if conn: conn.rollback()
                                            flag = False
                                        finally:
                                            if conn:
                                                conn.close()
                                        if flag:
                                            Dialog('Регистрация успешно завершена!', 'Поздравляем!')
                                            self.parent.current = 'RegistrationDop'
                                        else:
                                            Dialog('Введены неверные данные', 'Отказ в регистрации')
                                    else:
                                        Dialog('Такой пользователь уже зарегестрирован', 'Внимание!')

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

    def click_on_button_res(self):
        Data.screen_history.append('Enter')
        user_info.name = 'Иван'
        user_info.surname = 'Иванов'
        user_info.lastname = 'Иванович'
        user_info.phone = '+7 777 777 77 77'
        user_info.mail = 'ivan@ivan.ivan'
        self.parent.current = 'GPSHelper'

    def click_on_button_enter(self):
        if self.input_phone.text == '':
            Dialog('Вы не ввели телефон', 'Внимание!')
        else:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', self.input_phone.text) == None:
                Dialog('Неккоректный ввод телефона', 'Внимание!')
            else:
                conn = SQLCommander.connect('resources/DB/user_db.db')
                curr = conn.cursor()
                curr.execute("SELECT * from Users WHERE phone="+self.input_phone.text)

                allItems = list(curr.fetchall())

                flag = False
                for i in range(len(allItems)):
                    if allItems[i][5] == self.input_phone.text:
                        flag = True
                if flag:
                    phone = '+7' + self.input_phone.text
                    code = rec_otp('7' + self.input_phone.text)
                    Data.phone = phone
                    Data.code = code
                    self.parent.get_screen('EnterCheckPhone').ids.label_phone.text = str(Data.phone)
                    self.parent.current = 'EnterCheckPhone'
                else:
                    Dialog('Профиль с таким номером телефона не найден', 'Внимание')

    def click_on_button_register(self):
        Data.screen_history.append('Enter')
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
    window_manager = ObjectProperty()
    theme_cls = ThemeManager()
    title = 'Умная рыбалка'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_keyboard=self.android_button_click)

        @mainthread
        def delayed():
            self.load_database()
        delayed()

    def android_button_click(self,window, key, *largs):
        if key == 27:
            if not len(Data.screen_history) == 0:
                MDApp.get_running_app().root.current = Data.screen_history[-1]
                Data.screen_history.pop()
            else:
                self.window_manager.current = 'Onboard'
            return True

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

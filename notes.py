from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
import json
from dialog import Dialog

class Notes(Screen):
    note1 = ObjectProperty()
    note2 = ObjectProperty()
    note3 = ObjectProperty()
    zag1 = StringProperty()
    text1 = StringProperty()
    zag2 = StringProperty()
    text2 = StringProperty()
    zag3 = StringProperty()
    text3 = StringProperty()
    data = None

    def __init__(self, **kwargs):
        super(Notes, self).__init__(**kwargs)

    def entering(self):
        with open('notes.json') as file:
            data = json.load(file)

        if data[0]["zag"] == None and data[0]["text"] == None:
            self.note1.opacity = 0
            if data[1]["zag"] == None and data[1]["text"] == None:
                self.note2.opacity = 0
                if data[2]["zag"] == None and data[2]["text"] == None:
                    self.note3.opacity = 0
                else:
                    self.note1.opacity = 1
                    self.zag1.text = data[2]["zag"]
                    self.text1.text = data[2]["text"]
                    data[0]["zag"] = data[2]["zag"]
                    data[0]["text"] = data[2]["text"]
            else:
                self.note1.opacity = 1
                self.zag1.text = data[1]["zag"]
                self.text1.text = data[1]["text"]
                data[0]["zag"] = data[1]["zag"]
                data[0]["text"] = data[1]["text"]
                if data[2]["zag"] == None and data[2]["text"] == None:
                    self.note3.opacity = 0
                else:
                    self.note2.opacity = 1
                    self.zag2.text = data[2]["zag"]
                    self.text2.text = data[2]["text"]
                    data[1]["zag"] = data[2]["zag"]
                    data[1]["text"] = data[2]["text"]
        else:
            self.note1.opacity = 1
            self.zag1.text = data[0]["zag"]
            self.text1.text = data[0]["text"]
            if data[1]["zag"] == None and data[1]["text"] == None:
                self.note2.opacity = 0
                if data[2]["zag"] == None and data[2]["text"] == None:
                    self.note3.opacity = 0
                else:
                    self.note2.opacity = 1
                    self.zag2.text = data[2]["zag"]
                    self.text2.text = data[2]["text"]
                    data[1]["zag"] = data[2]["zag"]
                    data[1]["text"] = data[2]["text"]
            else:
                self.note2.opacity = 1
                self.zag2.text = data[1]["zag"]
                self.text2.text = data[1]["text"]
                if data[2]["zag"] == None and data[2]["text"] == None:
                    self.note3.opacity = 0
                else:
                    self.note3.opacity = 1
                    self.zag3.text = data[2]["zag"]
                    self.text3.text = data[2]["text"]
        with open('notes.json', 'w', encoding = 'UTF-8') as file:
            json.dump(data, file, ensure_ascii = False)

    def add_note(self):
        flag = False
        data = None
        with open('notes.json') as file:
            data = json.load(file)
        print((data[0]["zag"] == None) and (data[0]["text"] == None))
        if (data[0]["zag"] == None and data[0]["text"] == None):
            flag = True
        if (data[1]["zag"] == None and data[1]["text"] == None):
            flag = True
        if (data[2]["zag"] == None and data[2]["text"] == None):
            flag = True
        if flag:
            self.parent.current = 'AddNote'
        else:
            Dialog('К сожалению доступно только 3 заметки', 'Внимание!')

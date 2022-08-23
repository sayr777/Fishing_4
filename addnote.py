from kivy.uix.screenmanager import Screen
import json
from kivy.properties import ObjectProperty

class AddNote(Screen):
    zag_input = ObjectProperty()
    text_input = ObjectProperty()

    def save_note(self):
        data = None
        with open('notes.json') as file:
            data = json.load(file)

        i = None
        flag = False
        if not (data[0]["zag"] == None and data[0]["text"] == None):
            i = 0
        if not (data[1]["zag"] == None and data[1]["text"] == None):
            i = 1
        if not (data[2]["zag"] == None and data[2]["text"] == None):
            i = 2

        data[i]["zag"] = self.zag_input.text
        data[i]["text"] = self.text_input.text

        with open('notes.json', 'w', encoding = 'UTF-8') as file:
            json.dump(data, file, ensure_ascii = False)

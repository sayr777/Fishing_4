class Data():
    phone = 0
    code = 0

    input_surname = ''
    input_name = ''
    input_lastname = ''
    input_mail = ''
    input_phone = 0

    number_rule = 0
    number_penalties = 0

    stateMap = 'Street'

    db = []

    def save_info(self, surname, name, lastname, mail, phone):
        try:
            input_phone = int(phone)
        except:
            pass
        finally:
            input_phone = ''
        self.input_surname = surname
        self.input_name = name
        self.input_lastname = lastname
        self.input_mail = mail
        self.input_phone = input_phone

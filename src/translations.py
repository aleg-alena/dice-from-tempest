translations = {
    'en':{
        'Недостаточно денег':'Not enough money',
        'Успешно удалили комнату':'Successfully removed the room',
        'Такой комнаты не существует':'That room doesnt exist'
    }
}

def tra(text, Lang='ru'):
    if Lang == 'ru':
        return text

    else:
        global translations
        try:
            return translations[Lang][text]
        except:
            return text
import csv

def csvWrite(data, file):
    writehead = False
    fieldnames = ['id', 'login', 'password']
    # lineCount not count fieldnames (idk why)
    with open(file, mode='r', encoding='UTF-8') as csvFr:
        for i in csv.DictReader(csvFr):
            print(dict(i))
        """
        idLineCount = len(csvFr.readlines())
        data.update({'id':f'{idLineCount}'})
        if idLineCount <= 1:
            writehead = True"""

csvWrite({'login':'pidor', 'password':'gay'}, 'storage.csv')
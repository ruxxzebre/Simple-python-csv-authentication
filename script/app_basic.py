import csv, sys, time, hashlib

def lineCount(file):
    with open(file, mode='r', encoding='UTF-8') as csvF:
        reader = csv.DictReader(csvF)
        count = sum(1 for i in reader)
        return count

def csvWrite(data, file):
    writehead = False
    fieldnames = ['id', 'login', 'password']

    with open(file, mode='r', encoding='UTF-8') as csvFr:
        data.update({'id':f'{lineCount(file) + 1}'})
        if lineCount(file) < 1:
            writehead = True

    with open (file, mode='a', encoding='UTF-8', newline='') as csvF:
        writer = csv.DictWriter (csvF, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if writehead:
            writer.writeheader()
        writer.writerow(data)

def csvRead(data, file):
    # returns id
    with open(file, "r", encoding="UTF-8") as csvFr:
        cReader = csv.DictReader(csvFr)
        for i in cReader:
            i = dict(i)
            if i['login'] == data['login'] and i['password'] == data['password']:
                return i['id']
        else:
            return 'Wrong credentials'
def main():
    storageChoose = input('Encrypted storage or not? {0 or 1} : ')
    storage = 'storage_encryption.csv' if storageChoose == '0' else 'storage.csv'
    while True:
        pair = {}
        command = input('Log in / Sign Up {0 or 1} : ')
        if command == '1':
            login = input ('Login : ')
            while True:
                password = input('Password : ')
                passwordCheck = input('Password again : ')
                if password == passwordCheck:
                    break
                else:
                    print("Passwords isn't matching, please, try again...")
                    time.sleep(1)
            if storageChoose == '1' :
                pair.update({'login':login, 'password':password})
            else:
                pair.update ({'login': login,
                              'password': hashlib.md5 (bytes (password, encoding='ascii')).hexdigest()})
            csvWrite(pair, storage)
        elif command == '0':
            login = input ('Login : ')
            password = input ('Password : ')
            if storageChoose == '1':
                pair.update ({'login': login, 'password': password})
            else:
                pair.update ({'login': login,
                              'password': hashlib.md5(bytes(password, encoding='ascii')).hexdigest()})
            print(csvRead(pair ,storage))

if __name__ == '__main__':
    main()
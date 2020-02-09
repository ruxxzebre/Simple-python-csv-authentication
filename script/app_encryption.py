"""
    Simple auth system on python.
    Script can :
        Sign out users
        Log in
    Then it will can change encryption algos, passwords, logins etc.
"""

import csv, sys, time, hashlib
#import fire
from getpass import getpass


def lineCount(file):
    """
    Needed for correct id assignment for every pair of log:pass
    :param file: for example 'storage.csv'
    :return: number of lines
    """
    with open(file, mode='r', encoding='UTF-8') as csvF:
        reader = csv.DictReader(csvF)
        count = sum(1 for i in reader)
        return count

def csvWrite(data, file):
    writehead = False
    fieldnames = ['id', 'login', 'password']

    with open(file, mode='r', encoding='UTF-8') as csvFr:
        count = sum(1 for i in csv.DictReader(csvFr))
        """
        here we count lines in csv file so we can assign certain id to new pair value
        The fieldnames row (row that contains names of columns) not don't count
        because DictReader class reads only values, and than assign it to certain field names
        Then i'm adding 1 to count, because id's began on 1 not zero.
        You can consider fieldnames row in csv file as 0 row, that's will be more clear.
        So we change writehead flag to True, if there's no any values in file, except field names.
        It causes problem, because if there in file already is the row with field names, new one will 
        be added.
        Don't really know at this moment what to do with it, because working with csv and dicts in 
        one is a bit strange.
        
        So in this brand, csv file should be clear, or contain at least one value.
        """
        if count == 0:
            writehead = True
        count += 1
        data.update({'id':str(count)})

    with open (file, mode='a', encoding='UTF-8', newline='') as csvF:
        writer = csv.DictWriter (csvF, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if writehead:
            writer.writeheader()
        writer.writerow(data) # writing our new pair of log:pass

def csvRead(data, file):
    # returns id if there is given value
    with open(file, "r", encoding="UTF-8") as csvFr:
        cReader = csv.DictReader(csvFr)
        for i in cReader:
            i = dict(i)
            if i['login'] == data['login'] and i['password'] == data['password']:
                return (True, i['id']) # returns tuple, where first parameter - is boolean value
        else:
            return (False, 'Wrong credentials, maybe try again?\n')

def main():
    storage=sys.argv[1] if len(sys.argv) > 1 else 'storage.csv'
    while True:
        pair = {}
        command = input('Log in (0) \nSign Up (1)\n')

        if command == '1':
            login = input ('Login : ')
            while True:
                #password = stdiomask.getpass(prompt='Password : ', mask='*')
                #passwordCheck = stdiomask.getpass(prompt='Password again : ', mask='*')
                #password, passwordCheck = getpass(), getpass()
                password = input('Password : ')
                if password == input('And one more time : '):
                    break
                else:
                    print("Passwords isn't matching, please, try again...")
                    time.sleep(1)

            pair.update ({'login': login,
                            'password': hashlib.md5 (bytes (password, encoding='ascii')).hexdigest()})
            csvWrite(pair, storage)

        elif command == '0':
            while True:
                login = input ('Login : ')
                #password = getpass(prompt='Password : ')
                password = input('Password : ')
                pair.update ({'login': login,
                                'password': hashlib.md5(bytes(password, encoding='ascii')).hexdigest()})
                reader = csvRead(pair ,storage)
                if reader[0]:
                    print (f"Success! You logged in. It is your account's id - {reader[1]}")
                    time.sleep(1)
                    break
                else:
                    print(reader[1])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt and EOFError:
        # why OR is not working?
        print('\nGoodbye...')
        time.sleep(2)
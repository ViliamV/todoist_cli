#!/usr/bin/env python3
import pickle
import os

DIR = os.path.dirname(os.path.realpath(__file__))
print('Enter your Todoist credentials. They will be stored in unencrypted format therefore do not share the \'login\' file.')
login = input('Login: ')
password = input('Password: ')
try:
    pickle.dump((login, password), open('login','wb'))
    print('Credentials saved.')
except:
    print('Unable to write in the directory.')

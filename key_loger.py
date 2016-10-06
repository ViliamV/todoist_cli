import pickle
import click

key_names = ['up', 'down', 'left', 'right', 'space', 'enter', 'backspace']
keys = {}
for key_name in key_names:
    print('Press {}'.format(key_name))
    key = click.getchar()
    keys[key_name]=key
pickle.dump(keys, open('keys', 'wb'))

#!/usr/bin/env python3
from pytodoist import todoist
import os
from datetime import timedelta
from datetime import date
import argparse
import pickle
import click
import threading
from blessings import Terminal

# Bug - Empty list of tasks
# Feature missing - due date on tasks


DIR = os.path.dirname(os.path.realpath(__file__))
CACHE = DIR + '/cache'

class View:
    def __init__(self, name, header, help_text='', update_args=None, update_func=None):
        self.items = None
        self.name = name
        self.header = header 
        self.help_text= help_text
        self.selected = 0           
        self.update_args = update_args
        self.update_func=update_func
        self.parent = None
        try:
            self.items = pickle.load(open(CACHE+'/'+name, 'rb'))     
        except:
            pass
        self.update_thread = threading.Thread(target=self.update).start()          
    
    def set_parent(self, parent):
        self.parent = parent            
    
    def print(self, items):
        os.system('cls' if os.name == 'nt' else 'clear')
        with term.location(0, 0):
            print(self.header)        
            for i, n in enumerate(items):
                print('> {}'.format(n)) if i==self.selected else print('  {}'.format(n))
        with term.location(0, term.height - 2):
            print(self.help_text)
    
    def update(self):
        if self.update_args is None:
            self.items = self.update_func()
        elif type(self.update_args) is tuple:
            self.items = self.update_func(*self.update_args)
        else:
            self.items = self.update_func(self.update_args)
        pickle.dump(self.items, open(CACHE+'/'+self.name, 'wb'))
    
    def pass_function(self, selected):
        pass
        
    def go_back(self, selected):
        self.parent.read_input() 
        
    def go_to(self, selected):
        self.items[selected].read_input()   
        
    def read_input(self, confirm_function, undo_function, right_function, left_function):
        while True:
            key = click.getchar()
            if key == keys['down']:
                self.selected = min(self.selected+1, len(self.items)-1)
                self.print()
            elif key == keys['up']:
                self.selected = max(self.selected-1, 0)
                self.print()
            elif key == keys['space'] or key == keys['enter']:
                confirm_function(self.selected)
                #if not validate_right:
                #    print('Wait please, loading data')
                #else:
                #    return action_right
            elif key == keys['right']:
                right_function(self.selected)
                #return action_right
            elif key == keys['left']:
                left_function(self.selected)
                #return action_left
            elif key == 'u':
                undo_function(self.selected)
            elif key == 'q':
                exit()
                #return -1, 0
        

class TaskList(View):    
    def print(self):
        while self.items is None:
            pass
        if self.items == [] and self.header.find('\n(empty)')==-1:            
            self.header +='\n(empty)'
        if len(self.items) != 0 and self.header.find('\n(empty)')!=-1:
            self.header.replace('\n(empty)', '')
        super().print(['{}\t{}'.format(t.content, t.due_date) for t in self.items])    
    def update(self):        
        super().update()
        
    def complete_task_t(self):
        self.task.complete()
        self.update()
        
    def complete_task(self, selected):
        self.task = self.items[selected]
        self.items.remove(self.task)
        if self.selected == len(self.items)-1:
            self.selected -= 1
        self.print()
        threading.Thread(target=self.complete_task_t).start()                
        #tasks.remove(task)
        #task.complete()
        #load_view()
        
    def undo_completion_t(self):
        self.task.uncomplete()
        self.task = None
        self.update()  
              
    def undo_completion(self, selected):
        if self.task is not None:
            self.items.append(self.task)
            self.print()            
            threading.Thread(target=self.undo_completion_t).start() 
                
    def read_input(self):
        self.print()
        super().read_input(self.complete_task, self.undo_completion, super().pass_function, super().go_back)
        

        
class Menu(View):
    def print(self):
        super().print(['Today+Overdue', 'Tomorrow', 'Projects'])
    def update(self):
        self.items = [today, tomorrow, projects]    
    def read_input(self):
        self.print()
        super().read_input(super().go_to, super().pass_function, super().go_to, super().pass_function)
        
class Projects(View):
    def print(self):
        while self.items == []:
            pass
        super().print([p.name for p in self.items])
    def update(self):        
        super().update()
        self.projects=self.items
        self.items = [TaskList(p.name, p.name, None, update_func=self.projects[i].get_tasks) for i, p in enumerate(self.projects)]
        for p in self.items:
            p.set_parent(self)
    def read_input(self):
        self.print()
        super().read_input(super().go_to, super().pass_function, super().go_to, super().go_back)
   
def login():
    global user
    
    
    
if __name__ == "__main__":  
    '''Simple command-line interface for completing tasks in Todoist. Work in progress''' 
    term = Terminal()  
    if not os.path.exists(CACHE):
        os.makedirs(CACHE)
    try:
        keys = pickle.load(open('keys', 'rb')) 
        login, password = pickle.load(open(DIR+'/login', 'rb'))             
    except:
        print('Missing \'keys\' or \'login\'')
    user = todoist.login(login, password)
    today = TaskList('today', 'Today', '', update_args=(todoist.Query.TODAY, todoist.Query.OVERDUE), update_func=user.search_tasks)
    tomorrow = TaskList('tomorrow', 'Tomorrow', update_args=todoist.Query.TOMORROW, update_func=user.search_tasks)
    projects = Projects('projects', 'Projects', update_func=user.get_projects)    
    menu = Menu('menu', 'Todoist', 'Move with arrows and select with Space, Enter or Right arrow.')
    today.set_parent(menu)
    tomorrow.set_parent(menu)
    projects.set_parent(menu)    
    #while login_thread.isAlive():
    #    pass
    #print([t.content for t in user.search_tasks(todoist.Query.TOMORROW)])
    menu.read_input()
    
    

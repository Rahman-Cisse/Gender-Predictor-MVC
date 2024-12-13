#model
import json
import os
from tkinter.messagebox import showerror

class Model:
    #initializing
    def __init__(self):
        self.session_history = []#assigning an empty listbox to store results
        self.history_file = "model/history.json"
        
        
    def save_history(self):
        try:
            with open(self.history_file, 'a') as file:
                for name, gender, probability, date_today, time_today in self.session_history:
                    json.dump({'name': name.upper(), 'gender': gender, 'probability': probability, 'date': date_today, 'time':time_today}, file)#to write the info into the json file 'history.json'
                    file.write('\n')#the /n will ensure each prediction info stored will be on a new line
                    self.session_history=[]#to make clear everything in the list so that it does not rewrite the same info into thejson file multiple times
        except Exception as e:#error handling
            showerror(title='Error', message=f'AN ERROR OCCURED WHILE SAVING YOUR HISTORY')
            
            
    #function that appends the info predictions into the list from the json file it was stored
    def load_history(self):
        history = []#assigning a list to store predictions from file


        if os.path.isfile(self.history_file)==False:   #creates a json file inside the folder created if theres none
            file = open(self.history_file, 'a')
        try:
            with open(self.history_file, 'r') as file:
                for line in file:
                    prediction = json.loads(line.strip())
                    history.append(prediction)
        #error handling
        except FileNotFoundError:
            showerror(title='Error', message='NO HISTORY FILE FOUND')
        except Exception as e:
            showerror(title='Error', message=f'SORRY, AN ERROR OCCURED WHILE LOADING HISTORY')
        return history
    
    
    def clear_history_file(self):
        with open(self.history_file, 'w') as file: 
                pass #clearing content
#controller
#importing all modules required
import threading
from model.model import Model                           
from view.main_window import MainWindow
from view.history_window import HistoryWindow
import requests
TEST_MODE = True

#using a class object
class Controller:
    #initializing
    def __init__(self,root):
        self.model = Model()
        self.root=root
        self.is_history_window_open = False  #this will help the history window to be opened
        self.predict_view = MainWindow(self.root, self)
        self.history_view = None #this ensures the history window is not opened immediately the application is opened
        
        
    def mock_api(self): 
        return ({'count': 36136, 'name': 'rahman', 'gender': 'male', 'probability': 0.9777}) 


    def on_predict(self, event=None):
        def fetch_data():
            try:
                
                entered_name = self.predict_view.name_entry.get().strip().lower()#to help get and validate entry
                
                #validate the user's input
                if len(entered_name) < 2 or not entered_name.isalpha():
                    self.predict_view.stop_loading_animation()
                    self.predict_view.showerror(title='Error', message='PLEASE ENTER A VALID NAME')
                    return 
                
                #make clear all previous searches that are currently being displayed
                self.predict_view.clear_labels()

                #to show the loading gif
                self.predict_view.start_loading_animation()
                #prevent user from changing name while program is running
                self.predict_view.disable_entrybox()
                
                #getting the information using requests if 
                if TEST_MODE : 
                    response = self.mock_api()
                else :
                    response = requests.get(f'https://api.genderize.io/?name={entered_name}').json()

                #assigning the results to variables
                name = response['name']
                gender = response['gender']
                probability = ( f"{100 * response['probability']:.1f}%")
                
                #allow usre to enter data
                self.predict_view.enable_entrybox()
                #######to handle names whose  genders are not found
                if gender == None: 
                    self.predict_view.stop_loading_animation()
                    self.predict_view.showerror(title='Gender not found', message='Please make sure you have entered a valid first name')
                    return
                
                #to display the information to the user
                self.predict_view.update_page(name, gender, probability)
                
                #updating the history tree
                self.model.session_history.append((name, gender, probability, self.predict_view.today_date, self.predict_view.today_time))
                #add copy command to drop down menu
                self.predict_view.adding_copy_command()
                #storing the information gotten
                self.model.save_history()
                #displaying the information stored in the tree
                self.update_history_tree()
                
            #error handling
            except requests.exceptions.RequestException:
                self.predict_view.stop_loading_animation()
                self.predict_view.showerror(title='Error', message='NETWORK ERROR: PLEASE MAKE SURE YOU ARE CONNECTED TO THE INTERNET')
            except KeyError:
                self.predict_view.stop_loading_animation()
                self.predict_view.showerror(title='Error', message='AN UNEXPECTED ERROR OCCURED: PLEASE TRY AGAIN LATER')
            except Exception as e:
                self.predict_view.stop_loading_animation()
                self.predict_view.showerror(title='Error', message='AN UNEXPECTED ERROR OCCURED: PLEASE TRY AGAIN LATER')
            finally:
                self.root.after(0, self.predict_view.stop_loading_animation)


        search_processes = threading.Thread(target=fetch_data)#threading
        search_processes.daemon= True
        search_processes.start()
        
    
    #def validate(self,entered_name): # callback function
           
    
    #to allow only one history window to be opened at a time
    def show_history_window(self):
        if not self.is_history_window_open:#this will prevent multiple windows from being opened
            self.history_view = HistoryWindow(self.root, self)
            self.history_view.display_history()
            self.is_history_window_open = True


    #to display stored information in the tree on the main window
    def update_history_tree(self):
        self.predict_view.update_history_tree()


    def copy(self): #copying predictions# into clipboard
        data = self.model.load_history()[-1]
        self.predict_view.predict_frame.clipboard_clear()
        self.predict_view.predict_frame.clipboard_append(f"Name:{data['name']}, Gender:{data['gender']}, Probability:{data['probability']}")
        self.predict_view.copied()
        
        
    def paste(self): #pasting name into the enntrybox from cliboard
        name_to_be_pasted=self.predict_view.predict_frame.clipboard_get()
        self.predict_view.entry_focus_in(event=None)
        self.predict_view.name_entry.insert(0, name_to_be_pasted)


    #to make sure the user wants to close the program by asking a yes or no question to the user
    def on_closing(self):
        if self.predict_view.askyenso(title="Quit", message="Quit?"):
            if self.is_history_window_open == True:
                self.history_view.close_history_window()
            self.root.destroy()#close window


    #function to clear all infoemation in the json file storing the history
    def clear_history(self):
        try:
            self.model.clear_history_file()
            self.update_history_tree()#refresh tree
            self.predict_view.clear_labels()#remove displayed info from screen
            self.predict_view.show_prediction_tab()#redirect user to prediction tab
            self.predict_view.clear_entrybox()    
            self.predict_view.remove_copy_command()
            self.predict_view.entry_focus_out(event=None)#remove anything entered in entrybox and enter placeholder
        except Exception as e:
            self.predict_view.showerror(title='Error', message=f'SORRY, AN ERROR OCCURED WHILE CLEARING HISTORY')


    # function to prepare stored info
    def load_history(self):
        return self.model.load_history()

    
    #main command to run programme
    def run(self):
        self.root.mainloop()
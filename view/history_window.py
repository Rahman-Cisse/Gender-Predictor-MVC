from tkinter import Toplevel, Label, Scrollbar, VERTICAL, BOTH, RIGHT, Y, LEFT, Button, TOP
from tkinter.messagebox import askyesno, showerror
from tkinter import ttk
from idlelib.tooltip import Hovertip 

class HistoryWindow:
    def __init__(self, root, controller):
        #creating the history window and all its features
        self.controller = controller
        self.history_window = Toplevel(root)
        self.history_window.title("Prediction History")
        self.history_window.geometry("480x520")
        self.history_window.resizable(False, False)
        self.history_window.configure(bg='#F7F7F7')
        self.buttons_font= 'Poppins 10 bold'
        
        self.history_window_features()
        
        
    def history_window_features(self):
        Label(self.history_window, text='ALL PREDICTIONS', font='Papyrus 17', bg='#F7F7F7', fg='#CB625F').pack()

        columns = ('name', 'gender', 'probability', 'date')
        self.full_tree = ttk.Treeview(self.history_window, columns=columns, show='headings')


        for col in columns:
            self.full_tree.heading(col, text=col)
            self.full_tree.column(col, width=100, anchor='center')

        self.full_tree.pack(side=TOP, fill=BOTH, expand=True)

        self.scrollbar = Scrollbar(self.full_tree, orient=VERTICAL, command=self.full_tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.full_tree.config(yscrollcommand=self.scrollbar.set)

        self.refresh_button = Button(self.history_window, text=" REFRESH ", bg='#F5F5DC', fg='black', bd='5', font=self.buttons_font, cursor='hand2', command=self.display_history)
        self.refresh_button.pack(pady=5, side=LEFT)
        self.hover_popup(self.refresh_button, 'refresh page')
        
        self.clear_button = Button(self.history_window, text='   CLEAR   ', bg='#F5F5DC', bd='5', fg='black', font=self.buttons_font, cursor='hand2',command=self.clear_full_history)
        self.clear_button.pack(pady=5, side=RIGHT)
        self.hover_popup(self.clear_button, 'clear your history')

        self.history_window.protocol("WM_DELETE_WINDOW", self.close_history_window)
        
        
    #to show popup messages when mouse hovers on widget
    def hover_popup(self, widget, message):
        Hovertip(widget, message)
        
        
    # to help close the history window and allow it to be opened again
    def close_history_window(self):
        self.history_window.destroy()
        self.controller.is_history_window_open = False


    #show history on the tree in history window
    def display_history(self):
        for row in self.full_tree.get_children():
            self.full_tree.delete(row)
        history = self.controller.load_history()
        try:
            for prediction in history:
                self.full_tree.insert('', 0, values=(prediction['name'], prediction['gender'], f"{prediction['probability']}", prediction['date']))
        except FileNotFoundError:
            showerror(title='Error', message='NO HISTORY FILE FOUND')
        except Exception as e:
            showerror(title='Error', message=f'SORRY AN ERROR OCCURED WHILE LOADING YOUR HISTORY')

            
    #function that cleares every info in the json file
    def clear_full_history(self):
        if askyesno(title="Clear History", message="ARE YOU SURE YOU WANT TO CLEAR YOUR HISTORY?"):
            self.controller.clear_history()
            self.display_history()
            self.close_history_window()
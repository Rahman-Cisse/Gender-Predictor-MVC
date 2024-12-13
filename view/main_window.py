from tkinter import Label, Menu, Scrollbar, Button,PhotoImage,Frame,Entry, VERTICAL, END, BOTH,RIGHT, Y,TOP,BOTTOM,CENTER
from tkinter.messagebox import showerror, askyesno
from tkinter import ttk
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
from idlelib.tooltip import Hovertip 

class MainWindow:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        self.showerror = showerror
        self.askyenso = askyesno
        self.end= END

        #window and label propertiies
        self.window_size = '410x524'
        self.my_background = '#0097A7'
        self.prediction_font = ('Poppins 10 bold', 9)
        
        #getting today's date from datetime
        self.today_date = datetime.now().strftime('%Y-%m-%d')
        self.today_time = datetime.now().strftime('%H:%M:%S')
        #a flag to create copy menu when preiction is made
        self.is_copy_command_added = False
                
        
        #setting up my window
        self.initialize_window()
        #calling my functionns to be used
        self.load_images()
        self.frames_and_tabs()
        self.create_predict_tab_widgets()
        #self.show_welcome_page()
        self.create_menu()
        self.bind_popup_menu()
        self.create_history_widgets()
        self.mouse_hover_popups()
        
        
    #setting up window and its propreties
    def initialize_window(self):
        self.root.title("Gender Predictor")
        self.root.geometry(self.window_size)
        self.root.resizable(False, False)
        self.root.configure(bg=self.my_background)
        self.root.protocol("WM_DELETE_WINDOW", self.controller.on_closing)

        #my_icon
        self.icon = PhotoImage(file='images/icon.png')
        self.root.iconphoto(self.root, self.icon)


    #all frames and notebook
    def frames_and_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill=BOTH)

        self.predict_frame = Frame(self.notebook, bg=self.my_background)
        self.history_frame = Frame(self.notebook)

        self.notebook.add(self.predict_frame, image=self.home_icon)
        self.notebook.add(self.history_frame, image=self.history_icon)


    #assigning all images to be used
    def load_images(self):
        self.top_image = PhotoImage(file='images/top_image.png')
        self.bottom_male_frame = PhotoImage(file='images/name_frame.png')
        self.bottom_female_frame = PhotoImage(file='images/female_name_frame.png')
        self.male_image = PhotoImage(file='images/male.png')
        self.female_image = PhotoImage(file='images/female.png')
        self.my_history_image = PhotoImage(file='images/history_image.png')
        self.copy_image = PhotoImage(file='images/copy.png')
        self.search_image = PhotoImage(file='images/search_button.png')
        self.welcome_image = PhotoImage(file='images/welcome_image.png')
        self.home_icon = PhotoImage(file='images/home_icon.png')
        self.history_icon = PhotoImage(file='images/history_icon.png')
        self.copied_icon = PhotoImage(file='images/copied_icon.png')

    
    #creating the physical details
    def create_predict_tab_widgets(self):
        self.top_image_label = Label(self.predict_frame, image=self.top_image)
        self.top_image_label.place(x=-10, y=-10)
        
        Label(self.predict_frame, text='Please insert your name here👇👇', font='Arial 12', bg=None).place(x=81, y=213)

        self.name_entry = Entry(self.predict_frame, width=20, font=('Poppins 15 bold'), justify=CENTER, fg='grey')
        self.name_entry.place(x=88, y=237)
        
        self.name_entry.bind('<Return>', self.controller.on_predict)
        
        self.name_entry.insert(0, 'ENTER NAME HERE..')
        self.name_entry.bind('<FocusIn>', self.entry_focus_in)
        self.name_entry.bind('<FocusOut>', self.entry_focus_out)
        
        self.predict_button = Button(self.predict_frame, image=self.search_image, bg='#032B44', bd='4', cursor='hand2' ,command=self.controller.on_predict)
        self.predict_button.place(x=165, y=269)

        self.bottom_image_frame_label = Label(self.predict_frame, bg=self.my_background)
        self.bottom_image_frame_label.place(x=206, y=308)
        
        self.name_label = Label(self.predict_frame, text='', bg=self.my_background, font= self.prediction_font)
        self.name_label.place(x=239, y=334)

        self.gender_label = Label(self.predict_frame, text='', bg=self.my_background, font=self.prediction_font)
        self.gender_label.place(x=239, y=364)

        self.probability_label = Label(self.predict_frame, text='', bg=self.my_background, font=self.prediction_font)
        self.probability_label.place(x=239, y=394)

        self.loading = Label(self.predict_frame, bg= self.my_background)
                
        self.spinner = SpinnerLabel(self.loading, 'images/loading.gif', size=(75, 75), delay=40) #calling the spinnerclass defined at the bottom of the code
        self.spinner.config(bg='#0097A7')
        self.spinner.pack()    #packing it on the loading label and ttaing two positiona arguments directory and size

        
        self.gender_image_label = Label(self.predict_frame, bg=self.my_background)
        self.gender_image_label.place(x=14, y=315)

        self.copy_button = Button(self.predict_frame, image=self.copy_image, command=self.controller.copy)


    # creating the features of the history tab in the main window
    def create_history_widgets(self):
        self.history_image_label = Label(self.history_frame, image=self.my_history_image)
        self.history_image_label.pack(side=TOP, fill=BOTH)
        
        #creating various columns in tree
        columns = ('name', 'gender', 'probability', 'time')
        self.tree = ttk.Treeview(self.history_frame, columns=columns, show='headings', cursor='hand2')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor='center')
        
        #displaying tree
        self.tree.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        #adding a scrollbar to tree
        self.scrollbar = Scrollbar(self.tree, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=self.scrollbar.set)

        #adding button forhistory window
        self.history_button = Button(self.history_frame, text="FULL HISTORY", bg='#F2EC9B', bd='5', font=('Poppins 10 bold'),cursor='hand2', command=self.controller.show_history_window)
        self.history_button.place(x=295, y=6)
        

        #keep history in tree
        self.update_history_tree()


    #this page is displayed immediatelly the page is opened
    def show_welcome_page(self):
        self.welcome_frame = Frame(self.root, bg='white')
        self.welcome_frame.place(relwidth=1, relheight=1)
        
        self.welcome_image_label = Label(self.welcome_frame,  bg='white', image=self.welcome_image)
        self.welcome_image_label.pack(side='top', fill='x')

        self.welcome_network_reminder = Label(self.welcome_frame, text="Make Sure You Are Connected To The Internet", font=('Arial', 14), bg='white', fg='black')
        self.welcome_network_reminder.pack(side=BOTTOM, fill='x')
        
        self.welcome_gif = Label(self.welcome_frame, bg='white')
        self.welcome_gif.pack(side='top', fill='x')

        self.spinner = SpinnerLabel(self.welcome_gif, 'images/welcome_gif.gif', size=(400, 350), delay=5) #calling the spinnerclass defined at the bottom of the code
        self.spinner.config(bg='white')
        self.spinner.pack(fill=BOTH)

        self.root.after(4000, self.welcome_frame.destroy)

    
    #right mouse button menu
    def create_menu(self):
        self.menu = Menu(self.root,bg="white", tearoff=0) #defining menu to have its parent as the main window and storing menu into self.menu since that is the object
        self.menu.add_command(label="Search", command=self.controller.on_predict)  #and also tearoff by deefault is 1 which means the user can turn this menu into another window
        self.menu.add_separator()
        self.menu.add_command(label="Paste name",command=self.controller.paste)
        
        
    def bind_popup_menu (self):
        def do_popup(event):    #defining a funtion to show the popup menu
            try:
                self.menu.tk_popup(event.x_root, event.y_root) #showing the menu at the x and y positions of where the right button was clicked
            finally:
                self.menu.grab_release()
        
        self.predict_frame.bind("<Button-3>", do_popup) #binding each of these widgets to the popup menu whenever the right mouse buttn is pressed with in them    
        self.top_image_label.bind("<Button-3>", do_popup)
        self.name_entry.bind("<Button-3>", do_popup)
        self.bottom_image_frame_label.bind("<Button-3>", do_popup)
        self.gender_image_label.bind("<Button-3>", do_popup)
        
    
    def adding_copy_command(self):
        if self.is_copy_command_added == False:
            self.is_copy_command_added= True
            self.menu.add_separator()
            self.menu.add_command(label="Copy Prediction",command=self.controller.copy)
        else:
            pass


    def remove_copy_command(self):
        self.menu.delete(0, END)
        self.create_menu()
    
    
    def copied(self):
        self.copy_button.config(image=self.copied_icon)
    
    
    #show temporal message when mouse hovers over widget
    def hover_popup(self, widget, message):
        Hovertip(widget, message)


    #messages to display below widget
    def mouse_hover_popups(self):
        self.hover_popup(self.name_entry, 'Enter Name Here')
        self.hover_popup(self.predict_button, 'Predict Gender')
        self.hover_popup(self.copy_button, 'Copy Your Last Prediction')
        self.hover_popup(self.history_button, 'View All History')


    #this will help remove all info that will clear previously displayed info from the screen
    def clear_labels(self):
        self.name_label.config(text='', bg=self.my_background)
        self.gender_label.config(text='', bg=self.my_background)
        self.probability_label.config(text='', bg=self.my_background)
        self.gender_image_label.config(image='', bg=self.my_background)
        self.bottom_image_frame_label.config(image='', bg=self.my_background)
        self.predict_frame.config(bg=self.my_background)
        self.predict_button.config(bg='#032B44')
        self.copy_button.place_forget()

        
    #responsible for displaying the info retreived from internet
    def update_page(self, name, gender, probability):
        #using color according to gender
        if gender == 'male':
            self.color = '#0080ff'
        elif gender == 'female':
            self.color = '#ffaec8'
        #configuring all labels according to gender
        self.predict_frame.config(bg=self.color)
        self.name_label.config(text='Name: ' + name.upper(), bg = self.color)
        self.gender_label.config(text='Gender: ' + (gender.upper() if gender else 'N/A'), bg = self.color)
        self.probability_label.config(text='Accuracy: ' + str(probability) , bg = self.color)
        self.bottom_image_frame_label.config(image=self.bottom_male_frame if gender == 'male' else self.bottom_female_frame, bg=self.color)
        self.gender_image_label.config(image=self.male_image if gender == 'male' else self.female_image , bg= self.color)
        
        self.copy_button.config(image=self.copy_image ,bg=self.color)
        self.copy_button.place(x=324, y=428)
        self.predict_button.config(bg='#ADD8E6' if gender=='male' else '#FFC0CB')
        
        
    #function to show the gif which appears when the application is searching for info
    def start_loading_animation(self):
        self.loading.place(x=160, y=400)
    

    #to stop the spinner immediately this command is passed
    def stop_loading_animation(self):
        self.loading.place_forget()
        
        
    def disable_entrybox(self):
        self.name_entry.config(state='readonly')
        
        
    def enable_entrybox(self):
        self.name_entry.config(state='normal')
            
    
    #to clear text when the history is cleared
    def clear_entrybox(self):
        self.name_entry.delete(0, END)


    #function responsible for inserting the info retreived into the tree
    def update_history_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        history = self.controller.load_history()
        for prediction in history:
            if prediction['date'] == self.today_date:
                self.tree.insert('', 0, values=(prediction['name'], prediction['gender'], prediction['probability'], prediction['time']))


    def show_prediction_tab(self):
        self.notebook.select(self.predict_frame)  # Redirect to the predict view


    def entry_focus_in(self, event):
        """function that gets called whenever entry is clicked"""
        if self.name_entry.get() == 'ENTER NAME HERE..':
            self.name_entry.delete(0, END) # delete all the text in the entry
            self.name_entry.configure(fg = 'black')


    def entry_focus_out(self,event):
        if self.name_entry.get() == '':
            self.name_entry.insert(0, 'ENTER NAME HERE..')
            self.name_entry.configure(fg = 'grey')


    #this will ensure the gif actually spins
class SpinnerLabel(Label):
    def __init__(self, master, gif_path, size, delay):
        Label.__init__(self, master)
        self.size = size
        self.frames = [ImageTk.PhotoImage(img.resize(self.size, Image.Resampling.LANCZOS)) 
                       for img in ImageSequence.Iterator(Image.open(gif_path))]
        self.index = 0
        self.update_label(delay)

    def update_label(self, delay):
        self.config(image=self.frames[self.index])
        self.index = (self.index + 1) % len(self.frames)
        self.after(delay, lambda: self.update_label(delay))  # Adjust the delay as necessary

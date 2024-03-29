from geopy.geocoders import Nominatim 
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage

names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Missing Person Detector")
        self.resizable(True, True)
        self.geometry("500x400")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        self.geolocator = Nominatim(user_agent="missing_person_app")  # Initialize Nominatim geocoder
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.frames["Login"] = Login(parent=container, controller=self)

        for F in (Login, StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # self.show_frame("StartPage")
        self.show_frame("Login")


    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()
    
    def login(self, username, password):
    
        if username == "Sidd" and password == "Sidd":
            self.show_frame("StartPage")  # Allow access to the main application
            self.logged_in = True
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        
    def on_closing(self):

        if messagebox.askokcancel("Exit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()

class Login(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.username_label = tk.Label(self, text="Username", font='Helvetica 12 bold')
        self.username_entry = tk.Entry(self, font='Helvetica 11')
        self.password_label = tk.Label(self, text="Password", font='Helvetica 12 bold')
        self.password_entry = tk.Entry(self, show="*", font='Helvetica 11')

        self.username_label.grid(row=0, column=0, pady=10, padx=5)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        self.password_label.grid(row=1, column=0, pady=10, padx=5)
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)

        self.login_button = tk.Button(self, text="Login", fg="#ffffff", bg="#000000", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, ipadx=5, ipady=4, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.controller.login(username, password)
        


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller 
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.grid(row=0, column=1, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font,fg="#000000")
            label.grid(row=0, sticky="nsew")
            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#000000",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Find a User  ", fg="#ffffff", bg="#000000",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Exit", fg="#ffffff", bg="#000000", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)


        def on_closing(self):
            if messagebox.askokcancel("Exit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Enter the Name", fg="#000000", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(self, text="Enter Email", fg="#000000", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_email = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_email.grid(row=1, column=1, pady=10, padx=10)

        tk.Label(self, text="Enter Phone Number", fg="#000000", font='Helvetica 12 bold').grid(row=2, column=0, pady=10, padx=5)
        self.user_phone = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_phone.grid(row=2, column=1, pady=10, padx=10)

        tk.Label(self, text="Enter Last Location", fg="#000000", font='Helvetica 12 bold').grid(row=3, column=0, pady=10, padx=5)
        self.user_location = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_location.grid(row=3, column=1, pady=10, padx=10)

        tk.Label(self, text="Enter Height (cm)", fg="#000000", font='Helvetica 12 bold').grid(row=4, column=0, pady=10, padx=5)
        self.user_height = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_height.grid(row=4, column=1, pady=10, padx=10)

        tk.Label(self, text="Enter Weight (kg)", fg="#000000", font='Helvetica 12 bold').grid(row=5, column=0, pady=10, padx=5)
        self.user_weight = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_weight.grid(row=5, column=1, pady=10, padx=10)

        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#000000", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#000000", command=self.start_training)

        self.buttoncanc.grid(row=6, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=6, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return

        # You can retrieve the user information from the fields like this:
        name = self.user_name.get()
        to_email = self.user_email.get()
        to_email_str = str(to_email)
        phone = self.user_phone.get()
        location = self.user_location.get()
        height = self.user_height.get()
        weight = self.user_weight.get()

        # Now, you can save this user information or use it as needed.
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        self.controller.frames("PageFour").to_email= to_email_str

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#000000", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#000000")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#000000")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#000000")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#000000", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#000000",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "This will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


# class PageFour(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller

#         label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
#         label.grid(row=0,column=0, sticky="ew")
#         button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#000000")
#         #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
#         #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
#         button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#000000")
#         button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

#     def openwebcam(self):
#         main_app(self.controller.active_name)

class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0, column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#000000")
        button2 = tk.Button(self, text="Geocoding", command=self.geocode_address, fg="#ffffff", bg="#000000")
        button3 = tk.Button(self, text="Reverse Geocoding", command=self.reverse_geocode, fg="#ffffff", bg="#000000")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#000000")
        button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button2.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button3.grid(row=2, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=2, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self,to_email=None):
        latitude = 19.0760  
        longitude = 72.8777 
        self.to_email = to_email
        main_app(self.controller.active_name, latitude, longitude, to_email)
        

    def geocode_address(self):
        # Example of geocoding an address
        address = "Mumbai"
        location = self.controller.geolocator.geocode(address)
        if location:
            messagebox.showinfo("Geocoding Result", f"Location: {location.latitude}, {location.longitude}")
        else:
            messagebox.showerror("Geocoding Error", "Address not found.")

    def reverse_geocode(self):
        # Example of reverse geocoding coordinates
        latitude = 19.0760
        longitude = 72.8777
        location = self.controller.geolocator.reverse((latitude, longitude))
        if location:
            messagebox.showinfo("Reverse Geocoding Result", f"Address: {location.address}")
        else:
            messagebox.showerror("Reverse Geocoding Error", "Coordinates not found.")




app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.png'))
app.mainloop()


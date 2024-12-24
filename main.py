# Import the modules from the modules.py file
from modules import *
from app_functions import *


# Functions
def checker():
    if var.get() == 1:
        main_label.config(text="Fuck Refael")
    else:
        main_label.config(text="Fuck Hard Refael")

def system_check_health_all_system():
    main_label.config(text='System Health (All System)')   # Change the main label
    main_label.place(x=170,y=80)
    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(LIGHT, OUTLINE), command=lambda:back(cb1,cb2,cb3,b7,b8))
    b7.place(x=10,y=540)

    b8 = ttk.Button(root, text="Start", bootstyle=(LIGHT, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    b8.place(x=310,y=500)

    # Create Checkbutton
    ping_var = IntVar()
    cb1 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Ping Test", variable=ping_var, onvalue=1, offvalue=0, command=checker)
    cb1.place(x=300,y=300)

    softwares_var = IntVar()
    cb2 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Softwares Test", variable=softwares_var, onvalue=1, offvalue=0, command=checker, state=DISABLED)
    cb2.place(x=300,y=320)

    older_spyder_var = IntVar()
    cb3 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Older Spyder Software Test", variable=older_spyder_var, onvalue=1, offvalue=0, command=checker)
    cb3.place(x=300,y=340)


def system_check_health_self():
    main_label.config(text='System Health (Self)')   # Change the main label
    main_label.place(x=170,y=80)
    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(LIGHT, OUTLINE), command=lambda:back(cb1,cb2,cb3,b7,b8))
    b7.place(x=10,y=540)

    b8 = ttk.Button(root, text="Start", bootstyle=(LIGHT, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    b8.place(x=310,y=500)

    # Create Checkbutton
    ping_var = IntVar()
    cb1 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Ping Test", variable=ping_var, onvalue=1, offvalue=0, command=checker)
    cb1.place(x=300,y=300)

    softwares_var = IntVar()
    cb2 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Softwares Test", variable=softwares_var, onvalue=1, offvalue=0, command=checker)
    cb2.place(x=300,y=320)

    older_spyder_var = IntVar()
    cb3 = ttkb.Checkbutton(bootstyle="LIGHT, round-toggle", text="Older Spyder Software Test", variable=older_spyder_var, onvalue=1, offvalue=0, command=checker)
    cb3.place(x=300,y=340)

def back(cb1,cb2,cb3,b7,b8):
    main_label.config(text='Spyder SU')
    main_label.place(x=200,y=80)

    section_label.config(text='Main')
    section_label.place(x=310,y=10)

    cb1.place_forget()
    cb2.place_forget()
    cb3.place_forget()
    

    b1.place(x=200,y=300)
    b2.place(x=200,y=340)
    b3.place(x=200,y=380)
    b4.place(x=200,y=420)
    b5.place(x=200,y=460)
    b6.place(x=10,y=540)
    
    b7.place_forget()
    b8.place_forget()



def ping_test():
    b1.config(text='START')
    b1.place(x=145,y=350)

# Create the main windows of the app
root = ttkb.Window(themename="vapor")                          #Set the root var value to the class tk
root.geometry('700x600')                #Set the size of the window
root.resizable(False,False)             #Set the option to resize the window to inactive
root.title('Spyder Software Update')    #Set the tile of the app
root.iconbitmap("C:\Work\Spyder-SU\images\mprest.ico")


# Set a background image for the app
background_image = PhotoImage()


# Set Menu bars
app_menu = tk.Menu(root)
root.config(menu=app_menu)

# Create a open menu item
open_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Open', menu=open_menu)
open_menu.add_command(label='1. Softwares Installation Guid', command=checker)
open_menu.add_command(label='2. Softwares List', command=checker)

# Create a help menu item
help_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='1. mPrest instegrators members', command=checker)
help_menu.add_command(label='2. About', command=checker)


# Create Labels
main_label = ttkb.Label(text='Spyder SU', font=("Helvetica", 28), bootstyle='LIGHT')
main_label.place(x=200,y=80)

section_label = ttkb.Label(text='Main', bootstyle="light")
section_label.place(x=310,y=10)



# Create Buttons
b1 = ttk.Button(root, text="System Health Check (All System)", bootstyle=(LIGHT, OUTLINE), command=system_check_health_all_system)
b1.place(x=200,y=300)

b2 = ttk.Button(root, text="System Health Check (Self)", bootstyle=(LIGHT, OUTLINE), command=system_check_health_self)
b2.place(x=200,y=340)

b3 = ttk.Button(root, text="Spyder Software Installation (All System)", bootstyle=(LIGHT, OUTLINE), state=DISABLED)
b3.place(x=200,y=380)

b4 = ttk.Button(root, text="Spyder Software Installation (Self)", bootstyle=(LIGHT, OUTLINE), state=DISABLED)
b4.place(x=200,y=420)

b5 = ttk.Button(root, text="ThirdParty Softwares Installation", bootstyle=(LIGHT, OUTLINE))
b5.place(x=200,y=460)

b6 = ttk.Button(root, text="Exit", bootstyle=(LIGHT, OUTLINE), command=exit)
b6.place(x=10,y=540)

# Create Checkbutton
# var = IntVar()
# cb1 = ttkb.Checkbutton(bootstyle="danger, round-toggle", text="Ready!", variable=var, onvalue=1, offvalue=0, command=checker)
# cb1.place(x=300,y=300)



root.mainloop()                        #Allow the app to run without ending by itself

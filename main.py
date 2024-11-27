# Import the modules from the modules.py file
from modules import *
from app_functions import *


# Functions
def checker():
    if var.get() == 1:
        main_label.config(text="Fuck Refael")
    else:
        main_label.config(text="Fuck Hard Refael")

def system_check_health():
    main_label.config(text='System Health')   # Change the main label
    main_label.place(x=170,y=80)
    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.config(text='Ping Test', command=ping_test)
    b1.place(x=145,y=350)
    # b1.place_forget()                             # Make Button gone
    b2.config(text='Softwares Checker', command=ping_test)
    b2.place(x=145,y=400)
    # b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    
def ping_test():
    b1.config(text='START')
    b1.place(x=145,y=350)

# Create the main windows of the app
root = ttkb.Window(themename="vapor")                          #Set the root var value to the class tk
root.geometry('700x600')                #Set the size of the window
root.resizable(False,False)             #Set the option to resize the window to inactive
root.title('Spyder Software Update')    #Set the tile of the app
root.iconbitmap("C:\Python Projects\Spyder SU\images\mprest.ico")


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
main_label = ttkb.Label(text='Spyder SU', font=("Helvetica", 28), bootstyle='SUCCESS')
main_label.place(x=200,y=80)

section_label = ttkb.Label(text='Main', bootstyle="light")
section_label.place(x=310,y=10)



# Create Buttons
b1 = ttk.Button(root, text="System Health Check", bootstyle=(SUCCESS, OUTLINE), command=system_check_health)
b1.place(x=245,y=350)

b2 = ttk.Button(root, text="Spyder Software Installation", bootstyle=(LIGHT, OUTLINE), state=DISABLED)
b2.place(x=220,y=405)

b3 = ttk.Button(root, text="ThirdParty Softwares Installation", bootstyle=(LIGHT, OUTLINE))
b3.place(x=205,y=460)

b4 = ttk.Button(root, text="Exit", bootstyle=(LIGHT, OUTLINE))
b4.place(x=310,y=515)

# Create Checkbutton
# var = IntVar()
# cb1 = ttkb.Checkbutton(bootstyle="danger, round-toggle", text="Ready!", variable=var, onvalue=1, offvalue=0, command=checker)
# cb1.place(x=300,y=300)



root.mainloop()                        #Allow the app to run without ending by itself

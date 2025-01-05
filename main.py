# Import the modules from the modules.py file
from modules import *
from app_functions import *
from ping import *

# Functions
def checker():
    if var.get() == 1:
        main_label.config(text="Fuck Refael")
    else:
        main_label.config(text="Fuck Hard Refael")

def system_check_health_all_system():
    main_label.config(text='System Health')   # Change the main label
    main_label.place(x=170,y=80)
    secondary_label = ttkb.Label(text='All System', font=("Helvetica", 10), bootstyle='DARK')
    secondary_label.place(x=300,y=140)
    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(DARK, OUTLINE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,racks_label,battey_label,projects_label,cb3,secondary_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(DARK, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number:', font=("Helvetica", 11), bootstyle='DARK')
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='dark', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    racks_label = ttkb.Label(text='Select Number of racks:', font=("Helvetica", 11), bootstyle='DARK')
    racks_label.place(x=240,y=270)

    racks = ['1R','2R']

    cb2 = ttkb.Combobox(root, bootstyle='dark', values=racks)
    cb2.place(x=240, y=300)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='DARK')
    projects_label.place(x=240,y=350)

    cb3 = ttkb.Combobox(root, bootstyle='dark', values=projects)
    cb3.place(x=240, y=380)
    cb3.current(0)


    # Create Checkbutton
    b9 = ttk.Button(root, text="Networking", bootstyle=(DARK, OUTLINE), command=lambda:ping(cb1.get()))
    b9.place(x=240,y=450)

    b10 = ttk.Button(root, text="Softwares", bootstyle=(DARK, OUTLINE), command=checker)
    b10.place(x=370,y=450)

    b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=checker)
    b11.place(x=240,y=495)

    b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=checker)
    b12.place(x=370,y=495)
    
def system_check_health_self():
    main_label.config(text='System Health')   # Change the main label
    main_label.place(x=170,y=80)

    secondary_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='DARK')
    secondary_label.place(x=330,y=140)

    section_label.config(text='system_check_health') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(DARK, OUTLINE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,racks_label,battey_label,projects_label,cb3,secondary_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(DARK, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number', font=("Helvetica", 11), bootstyle='DARK')
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='dark', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    racks_label = ttkb.Label(text='Select Component', font=("Helvetica", 11), bootstyle='DARK')
    racks_label.place(x=240,y=270)

    racks = ['CCU1','CCU2',"ICS1","ICS2","DRS1","DRS2","OC1","OC2","COP"]

    cb2 = ttkb.Combobox(root, bootstyle='dark', values=racks)
    cb2.place(x=240, y=300)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='DARK')
    projects_label.place(x=240,y=350)

    cb3 = ttkb.Combobox(root, bootstyle='dark', values=projects)
    cb3.place(x=240, y=380)
    cb3.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Networking", bootstyle=(DARK, OUTLINE), command=lambda:ping(cb1.get()))
    b9.place(x=240,y=450)

    b10 = ttk.Button(root, text="Softwares", bootstyle=(DARK, OUTLINE), command=checker)
    b10.place(x=370,y=450)

    b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=checker)
    b11.place(x=240,y=495)

    b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=checker)
    b12.place(x=370,y=495)

def system_installation_Self():
    main_label.config(text='System Installation')   # Change the main label
    main_label.place(x=170,y=80)

    secondary_label = ttkb.Label(text='Self', font=("Helvetica", 10), bootstyle='DARK')
    secondary_label.place(x=330,y=140)

    section_label.config(text='system_Installation') # Change the section label
    section_label.place(x=270,y=10)
    b1.place_forget()                             # Make Button gone
    b2.place_forget()                             # Make Button gone
    b3.place_forget()                             # Make Button gone
    b4.place_forget()                             # Make Button gone
    #b5.place_forget()                             # Make Button gone
    b6.place_forget()                             # Make Button gone

    b7 = ttk.Button(root, text="Back", bootstyle=(DARK, OUTLINE), command=lambda:back2(b9,b10,b7,cb2,cb1,racks_label,battey_label,projects_label,cb3,secondary_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(DARK, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number', font=("Helvetica", 11), bootstyle='DARK')
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='dark', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    racks_label = ttkb.Label(text='Select Component', font=("Helvetica", 11), bootstyle='DARK')
    racks_label.place(x=240,y=270)

    racks = ['CCU1','CCU2',"ICS1","ICS2","DRS1","DRS2","OC1","OC2","COP"]

    cb2 = ttkb.Combobox(root, bootstyle='dark', values=racks)
    cb2.place(x=240, y=300)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='DARK')
    projects_label.place(x=240,y=350)

    cb3 = ttkb.Combobox(root, bootstyle='dark', values=projects)
    cb3.place(x=240, y=380)
    cb3.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Spyder Software", bootstyle=(DARK, OUTLINE), command=checker)
    b9.place(x=200,y=450)

    b10 = ttk.Button(root, text="Third Party Softwares", bootstyle=(DARK, OUTLINE), command=checker)
    b10.place(x=370,y=450)

    # b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=checker)
    # b11.place(x=240,y=495)

    # b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=checker)
    # b12.place(x=370,y=495)

def back2(b9,b10,b7,cb2,cb1,battey_label,racks_label,projects_label,cb3,secondary_label):
    main_label.config(text='Spyder SU')
    main_label.place(x=200,y=80)
    
    section_label.config(text='Main')
    section_label.place(x=310,y=10)

    secondary_label.place_forget()

    b9.place_forget()
    b10.place_forget()

    b1.place(x=200,y=300)
    b2.place(x=200,y=340)
    b3.place(x=200,y=380)
    b4.place(x=200,y=420)
    #b5.place(x=200,y=460)
    b6.place(x=10,y=540)
    
    b7.place_forget()
    #b8.place_forget()

    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    racks_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()

def back(b9,b10,b11,b12,b7,cb2,cb1,battey_label,racks_label,projects_label,cb3,secondary_label):
    main_label.config(text='Spyder SU')
    main_label.place(x=200,y=80)
    
    section_label.config(text='Main')
    section_label.place(x=310,y=10)

    secondary_label.place_forget()

    b9.place_forget()
    b10.place_forget()
    b11.place_forget()
    b12.place_forget()

    b1.place(x=200,y=300)
    b2.place(x=200,y=340)
    b3.place(x=200,y=380)
    b4.place(x=200,y=420)
    #b5.place(x=200,y=460)
    b6.place(x=10,y=540)
    
    b7.place_forget()
    #b8.place_forget()

    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    racks_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()


# Create the main windows of the app
root = ttkb.Window(themename="cosmo")                          #Set the root var value to the class tk
root.geometry('710x630')                #Set the size of the window
root.resizable(False,False)             #Set the option to resize the window to inactive
root.title('Spyder Software Update')    #Set the tile of the app
root.iconbitmap("C:\Python Projects\Spyder-SU\Spyder-SU\images\mprest.ico")


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
main_label = ttkb.Label(text='Spyder SU', font=("Helvetica", 28), bootstyle='DARK')
main_label.place(x=200,y=80)

section_label = ttkb.Label(text='Main', bootstyle="DARK")
section_label.place(x=310,y=10)



# Create Buttons
b1 = ttk.Button(root, text="System Health Check (All System)", bootstyle=(DARK, OUTLINE), command=system_check_health_all_system)
b1.place(x=200,y=300)

b2 = ttk.Button(root, text="System Health Check (Self)", bootstyle=(DARK, OUTLINE), command=system_check_health_self)
b2.place(x=200,y=340)

b3 = ttk.Button(root, text="System Installation (All System)", bootstyle=(DARK, OUTLINE))
b3.place(x=200,y=380)

b4 = ttk.Button(root, text="System Software Installation (Self)", bootstyle=(DARK, OUTLINE), command=system_installation_Self)
b4.place(x=200,y=420)

#b5 = ttk.Button(root, text="ThirdParty Softwares Installation", bootstyle=(DARK, OUTLINE))
#b5.place(x=200,y=460)

b6 = ttk.Button(root, text="Exit", bootstyle=(DARK, OUTLINE), command=exit)
b6.place(x=10,y=540)

# Create Checkbutton
# var = IntVar()
# cb1 = ttkb.Checkbutton(bootstyle="danger, round-toggle", text="Ready!", variable=var, onvalue=1, offvalue=0, command=checker)
# cb1.place(x=300,y=300)



root.mainloop()                        #Allow the app to run without ending by itself

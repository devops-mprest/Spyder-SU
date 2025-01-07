# Import the modules from the modules.py file
from modules import *
from app_functions import *
from ping import *
import threading
from tkinter import messagebox
import socket
from softwares import *

# Functions
# Functions for networking check and threading
def update_progressbar(pb, progress_value):
    pb['value'] = progress_value


def networking(battnumber, project, set, b9):
    global pb_label
    global pb
    # Create a progress bar and label
    if set == 'Main+Backup':
        b9.configure(bootstyle='info')
        pb = ttk.Progressbar(root, bootstyle='info', maximum=200, mode="determinate", length=200, value=0)
        pb.place(x=255, y=550)
        pb_label = ttk.Label(root, text="Networking Check In Progress")
        pb_label.place(x=230, y=570)
        pb_label.configure(text="Networking Check In Progress")
    else:
        b9.configure(bootstyle='info')
        pb = ttk.Progressbar(root, bootstyle='info', maximum=100, mode="inte", length=200, value=0)
        pb.place(x=255, y=550)
        pb_label = ttk.Label(root, text="Networking Check In Progress")
        pb_label.place(x=230, y=570)
        pb_label.configure(text="Networking Check In Progress")

    # Create a thread to run the ping function
    def ping_thread():
        # Run the ping function and get the result
        result = ping(battnumber, project, set, update_progressbar, pb)

        # Update the progress bar and label
        if result == 0:
            update_progressbar(pb, 100)  # Assuming ping success should update to 100%
            messagebox.showinfo("Ping Success", "All pings were successful.")
            b9.configure(bootstyle='SUCCESS')
            pb_label.place_forget()
            pb.place_forget()            
        else:
            b9.configure(bootstyle='DANGER')
            pb_label.place_forget()
            pb.place_forget()
            messagebox.showerror("Ping Failed", "There failures in the ping test.")

    # Start the thread to run the ping function
    threading.Thread(target=ping_thread, daemon=True).start()

def software_check(battnumber,project,set,b10):
    if set == 'Main+Backup':
        b10.configure(bootstyle='info')
        pb = ttk.Progressbar(root, bootstyle='info', maximum=200, mode="determinate", length=200, value=0)
        pb.place(x=255, y=550)
        pb_label = ttk.Label(root, text="Softwares Check In Progress")
        pb_label.place(x=230, y=570)
        pb_label.configure(text="Softwares Check In Progress")
    else:
        b10.configure(bootstyle='info')
        pb = ttk.Progressbar(root, bootstyle='info', maximum=100, mode="inte", length=200, value=0)
        pb.place(x=255, y=550)
        pb_label = ttk.Label(root, text="Softwares Check In Progress")
        pb_label.place(x=230, y=570)
        pb_label.configure(text="Softwares Check In Progress")

    def software_thread():
        # Run the ping function and get the result
        result = run_wmi_query()

    threading.Thread(target=software_thread, daemon=True).start()

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

    b7 = ttk.Button(root, text="Back", bootstyle=(DARK, OUTLINE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,sets_label,battey_label,projects_label,cb3,secondary_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(DARK, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number:', font=("Helvetica", 11), bootstyle='DARK')
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='dark', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='DARK')
    projects_label.place(x=240,y=270)

    cb3 = ttkb.Combobox(root, bootstyle='dark', values=projects)
    cb3.place(x=240, y=300)
    cb3.current(0)
    
    sets_label = ttkb.Label(text='Select Number of racks:', font=("Helvetica", 11), bootstyle='DARK')
    sets_label.place(x=240,y=350)
    if cb3.get() == 'All-in-One':
        sets = ['Main']
    else: 
        sets = ['Main','Backup','Main+Backup']

    cb2 = ttkb.Combobox(root, bootstyle='dark', values=sets)
    cb2.place(x=240, y=380)
    cb2.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Networking", bootstyle=(DARK, OUTLINE), command=lambda:networking(cb1.get(),cb3.get(),cb2.get(),b9))
    b9.place(x=240,y=450)

    b10 = ttk.Button(root, text="Softwares", bootstyle=(DARK, OUTLINE), command=lambda:software_check(cb3.get(),cb2.get(),b10))
    b10.place(x=370,y=450)

    b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=networking)
    b11.place(x=240,y=495)

    b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=networking)
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

    b7 = ttk.Button(root, text="Back", bootstyle=(DARK, OUTLINE), command=lambda:back(b9,b10,b11,b12,b7,cb2,cb1,sets_label,battey_label,projects_label,cb3,secondary_label))
    b7.place(x=10,y=540)

    #b8 = ttk.Button(root, text="Start", bootstyle=(DARK, OUTLINE), command=lambda:back(cb1,cb2,cb3))
    #b8.place(x=310,y=500)

    battey_label = ttkb.Label(text='Select Battery Number', font=("Helvetica", 11), bootstyle='DARK')
    battey_label.place(x=240,y=190)

    battnumber = [1,2,3,4,5,6,7,8,9,10]

    cb1 = ttkb.Combobox(root, bootstyle='dark', values=battnumber)
    cb1.place(x=240, y=220)
    cb1.current(0)
    
    sets_label = ttkb.Label(text='Select Component', font=("Helvetica", 11), bootstyle='DARK')
    sets_label.place(x=240,y=350)

    sets = ['CCU1','CCU2',"ICS1","ICS2","DRS1","DRS2","OC1","OC2","COP"]

    cb2 = ttkb.Combobox(root, bootstyle='dark', values=sets)
    cb2.place(x=240, y=380)
    cb2.current(0)

    projects = ['Spyder','All-in-One',]

    projects_label = ttkb.Label(text='Select Project:', font=("Helvetica", 11), bootstyle='DARK')
    projects_label.place(x=240,y=270)

    cb3 = ttkb.Combobox(root, bootstyle='dark', values=projects)
    cb3.place(x=240, y=300)
    cb3.current(0)

    # Create Checkbutton
    b9 = ttk.Button(root, text="Networking", bootstyle=(DARK, OUTLINE), command=lambda:ping(cb1.get()))
    b9.place(x=240,y=450)

    b10 = ttk.Button(root, text="Softwares", bootstyle=(DARK, OUTLINE), command=networking)
    b10.place(x=370,y=450)

    b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=networking)
    b11.place(x=240,y=495)

    b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=networking)
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
    b9 = ttk.Button(root, text="Spyder Software", bootstyle=(DARK, OUTLINE), command=networking)
    b9.place(x=200,y=450)

    b10 = ttk.Button(root, text="Third Party Softwares", bootstyle=(DARK, OUTLINE), command=networking)
    b10.place(x=370,y=450)

    # b11 = ttk.Button(root, text="Permissions", bootstyle=(DARK, OUTLINE), command=checker)
    # b11.place(x=240,y=495)

    # b12 = ttk.Button(root, text="Disk Space", bootstyle=(DARK, OUTLINE), command=checker)
    # b12.place(x=370,y=495)

def back2(b9,b10,b7,cb2,cb1,battey_label,sets_label,projects_label,cb3,secondary_label):
    main_label.config(text='Spyder SU')
    main_label.place(x=200,y=80)
    
    section_label.config(text='Main')
    section_label.place(x=310,y=10)

    secondary_label.place_forget()

    b9.place_forget()
    b10.place_forget()

    b1.place(x=190,y=300)
    b2.place(x=190,y=360)
    b3.place(x=190,y=420)
    b4.place(x=190,y=480)
    #b5.place(x=200,y=460)
    b6.place(x=10,y=540)
    
    b7.place_forget()
    #b8.place_forget()

    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    sets_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()

def back(b9,b10,b11,b12,b7,cb2,cb1,battey_label,sets_label,projects_label,cb3,secondary_label):
    main_label.config(text='Spyder SU')
    main_label.place(x=200,y=80)
    
    section_label.config(text='Main')
    section_label.place(x=310,y=10)

    secondary_label.place_forget()

    b9.place_forget()
    b10.place_forget()
    b11.place_forget()
    b12.place_forget()

    b1.place(x=190,y=300)
    b2.place(x=190,y=360)
    b3.place(x=190,y=420)
    b4.place(x=190,y=480)
    #b5.place(x=200,y=460)
    b6.place(x=10,y=540)
    
    b7.place_forget()
    #b8.place_forget()

    cb1.place_forget()
    battey_label.place_forget()
    cb2.place_forget()
    sets_label.place_forget()
    projects_label.place_forget()
    cb3.place_forget()
    # remove_pb()


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
open_menu.add_command(label='1. Softwares Installation Guid', command=networking)
open_menu.add_command(label='2. Softwares List', command=networking)

# Create a help menu item
help_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='1. mPrest instegrators members', command=networking)
help_menu.add_command(label='2. About', command=networking)

# Create Labels
main_label = ttkb.Label(text='Spyder SU', font=("Helvetica", 28), bootstyle='DARK')
main_label.place(x=200,y=80)

section_label = ttkb.Label(text='Main', bootstyle="DARK")
section_label.place(x=310,y=10)

local_ip = socket.gethostbyname(socket.gethostname())
hostname = socket.gethostname()
runner_info_label = ttkb.Label(text=f'''
                                {hostname}
                               {local_ip}''')
runner_info_label.place(relx=-0.2, rely=-0.050)
# runner_info_label.place(x=400,y=50)


# Create Buttons
b1 = ttk.Button(root, text="System Health Check (All System)", bootstyle=(DARK, OUTLINE),width=30, command=system_check_health_all_system)
b1.place(x=190,y=300)

b2 = ttk.Button(root, text="System Health Check (Self)", bootstyle=(DARK, OUTLINE),width=30, command=system_check_health_self)
b2.place(x=190,y=360)

b3 = ttk.Button(root, text="System Installation (All System)", bootstyle=(DARK, OUTLINE),width=30)
b3.place(x=190,y=420)

b4 = ttk.Button(root, text="System Software Installation (Self)", bootstyle=(DARK, OUTLINE),width=30, command=system_installation_Self)
b4.place(x=190,y=480)

#b5 = ttk.Button(root, text="ThirdParty Softwares Installation", bootstyle=(DARK, OUTLINE))
#b5.place(x=200,y=460)

b6 = ttk.Button(root, text="Exit", bootstyle=(DARK, OUTLINE), command=exit)
b6.place(x=10,y=540)

# Create Checkbutton
# var = IntVar()
# cb1 = ttkb.Checkbutton(bootstyle="danger, round-toggle", text="Ready!", variable=var, onvalue=1, offvalue=0, command=checker)
# cb1.place(x=300,y=300)



root.mainloop()                        #Allow the app to run without ending by itself

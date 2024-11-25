# Import the modules from the modules.py file
from modules import *
from app_functions import *

# Create the main windows of the app
root = tk.Tk()                          #Set the root var value to the class tk
root.geometry('600x400')                #Set the size of the window
root.resizable(False,False)             #Set the option to resize the window to inactive
root.title('Spyder Software Update')    #Set the tile of the app
root.iconbitmap("C:\Python Projects\Spyder SU\images\mprest.ico")

# Set a background image for the app



# Set Menu bars
app_menu = tk.Menu(root)
root.config(menu=app_menu)

# Create a open menu item
open_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Open', menu=open_menu)
open_menu.add_command(label='1. Softwares Installation Guid', command=software_installation_guid)
open_menu.add_command(label='2. Softwares List', command=software_installation_guid)

# Create a help menu item
help_menu = tk.Menu(app_menu)
app_menu.add_cascade(label='Help', menu=help_menu)
help_menu.add_command(label='1. mPrest instegrators members', command=software_installation_guid)
help_menu.add_command(label='2. About', command=software_installation_guid)





root.mainloop()                        #Allow the app to run without ending by itself

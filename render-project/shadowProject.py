from tkinter import *
from UIsphereProj import UIinterface

def main():
    master = Tk()
    window = UIinterface(master)
    window.setup()
    mainloop()
   
main()
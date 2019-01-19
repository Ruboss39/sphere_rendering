from tkinter import *
from render import SphereRender
from Sphere import Sphere
from tkinterRender import TkinterRender
from tkinter import messagebox

class UIinterface:
    def __init__(self,tkMain,width = 1080,height = 1000):
        #All constants, frames and lists accesible from every function
        self.__width = width
        self.__height = height

        self.__master = tkMain
        self.__mainCanvas = Canvas(self.__master, width=self.__width ,height=self.__height)
        self.__mainCanvas.grid(row = 0,column = 0)

        self.__holdTab = LabelFrame(self.__master,text = "Main", padx = 10, pady = 10)
        self.__holdTab.grid(row = 0,column = 1, sticky = N + W + E + S)
        self.__settingsTab = LabelFrame(self.__holdTab,text = "Settings", padx = 10, pady = 10)
        self.__settingsTab.grid(row = 0,column = 0,sticky = N + W + E)
        self.__objectTab = LabelFrame(self.__holdTab,text = "Objects", padx = 10, pady = 10)
        self.__objectTab.grid(row = 2, column = 0, sticky = N + W + E)
        self.__renderObjects = []
        self.__entryList = []

    def setup(self):
        self.__renderObjects = []
        self.__entryList = []
        self.widgetSetup()
        self.__master.bind("<Motion>",self.mouseMovement)
        self.drawBackground(self.__mainCanvas)

    def getMastertk(self):
        return self.__master

    def widgetSetup(self):
        #Creates widgets for the settings-tab, and also addes the widgets to a global list to make it easier for other funtions to acces them
        labels = ["Radius","X-position","Y-position","Z-position","Denisty","Pixelsize","Range"]
        for i in range(len(labels)):
            Label(self.__settingsTab, text=labels[i]).grid(row=i,column = 0 ,sticky=W)
            txBox = Entry(self.__settingsTab)
            txBox.grid(row = i,column = 1)
            self.__entryList.append(txBox)

            rgb = LabelFrame(self.__settingsTab,text = "Color", padx = 10, pady = 10)
            rgb.grid(row = len(labels),column = 1)
            Label(self.__settingsTab,text="RGB-value").grid(row = len(labels),column = 0, sticky = W)
        for i in range(0,3):
            txBoxRgb = Entry(rgb,width=6)
            txBoxRgb.grid(row = 0,column = i)
            self.__entryList.append(txBoxRgb)
        
        addButton = Button(self.__settingsTab,text = "Add object",command = self.addSphere,width = 8,height = 4)
        addButton.grid(row = len(labels) + 1, column = 0)

        self.objectSetup()

    def objectSetup(self):
        #Sets up the object tab, should run everytime an object changes
        for widget in self.__objectTab.winfo_children():
            widget.destroy()

        for i in range(len(self.__renderObjects)):
            self.addObjectToWidget(i)

    def addSphere(self):
        #Adds a renderobject from proper data, if the data is not proper, the program will not do anything
        d = self.getData()
        if len(d) == 0:
            messagebox.showerror("Error", "A value-error has appeared. Enter proper values")
        else:
            rnge = d[6]
            rgb = [d[7],d[8],d[9]]
            sphere = Sphere(d[0],d[1],d[2],d[3])
            renderObj = TkinterRender(self.__mainCanvas,sphere,d[4],d[5],rgb,rnge)
            self.__renderObjects.append(renderObj)
        self.objectSetup()

    def getData(self):
        #checks the data if it is parseable
        tmp = []
        i = 0
        for entry in self.__entryList:
            try:
                if i ==6:
                    cRange = self.parseRangeData(entry.get())
                    if len(cRange) == 2:
                        tmp.append(cRange)
                    else:
                        return []
                else:
                    tmp.append(float(entry.get()))
            except ValueError:
                return []
            i+=1
        for i in range(0,3):
            tmp[7 + i] = self.limitValue(tmp[7+i],0,255)
        return tmp

    #A special parser only for range-data since it's entry contains 2 values
    def parseRangeData(self,data):
        try:
            if data == "":
                return [0,255]
            else :
                data = data.strip("]")
                data = data.strip("[")
                d = data.split(",")
                d[0] = float(d[0])
                d[1] = float(d[1])
                d[0] = self.limitValue(d[0],0,255)
                d[1] = self.limitValue(d[1],0,255)
                return d
        except ValueError:
            return []
        except IndexError:
            return []

    def limitValue(self,value,low,high):
        if value > high:
            value = high
        elif value < low:
            value = low
        return value

    def addObjectToWidget(self,iteration):
        #Simple function that adds a object to the object-display. 
        #Buttons are not stored in any list, but they are connected to the same callback but with different arguments.
        i = iteration
        Label(self.__objectTab, text="Sphere " + str(i)).grid(row=i,column = 0 ,sticky=W)
        button1 = Button(self.__objectTab,text = "Remove", command = lambda:self.removeSphere(i))
        button2 = Button(self.__objectTab,text = "Change", command = lambda:self.changeSphere(i))
        button1.grid(row = i, column = 1)
        button2.grid(row = i, column = 2)

    def removeSphere(self,sphere):
        #Self-explanatory
        self.__renderObjects.pop(sphere)
        self.objectSetup()

    def changeSphere(self,sphere):
        #Puts the data from the renderobject into the widgets 
        data = self.__renderObjects[sphere].getValues()
        i = 0
        for entry in self.__entryList:
            entry.delete(0,'end')
            entry.insert(0,str(data[i]))
            i+=1
        self.removeSphere(sphere)
            
    def drawBackground(self,graphics):
        graphics.create_rectangle(0,0,2560,1600,fill = "#5669a0")

    def mouseMovement(self,event):
        #function that 
        if event.x < self.__width -20 and event.y < self.__height-20:
            self.clearCanvas()
            self.drawBackground(self.__mainCanvas)
            for obj in self.__renderObjects:
                obj.drawSphere(event.x,event.y)

    def clearCanvas(self):
        self.__mainCanvas.delete("all")
    
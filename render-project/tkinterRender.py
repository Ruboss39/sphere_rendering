from render import SphereRender
#This class's main purpose is to render the data already given from render.py
#This class simply needs a canvas to create multpiple rectangles on to create a sphere
class TkinterRender:
    def __init__(self,canvas,sphere,density,pixelSize,rgb,lumosRange):
        self.__canvas = canvas
        self.__sphere = sphere
        self.__density = abs(density)
        self.__rgb = self.__scaleRGB(rgb)
        self.__pixelSize = pixelSize
        self.__range = lumosRange

    #Scaales the rgb-value to be less than 1
    def __scaleRGB(self,rgb):
        newRgb = []
        for color in rgb:
            newRgb.append(float(color/255.0))
        return newRgb

    #Return all the values
    def getValues(self):
        sphereData = [self.__sphere.getRadius(),self.__sphere.getCenterX(),self.__sphere.getCenterY(),self.__sphere.getCenterZ()]
        renderData = [self.__density,self.__pixelSize,self.__range,self.__rgb[0] * 255,self.__rgb[1]*255,self.__rgb[2]*255]
        return sphereData + renderData

    #A linear function that adjusts a range of values to another intervall
    def __mapper(self,value):
        rangeM = [0,1,self.__range[0],self.__range[1]]
        k = (rangeM[2]-rangeM[3]) / (rangeM[0]-rangeM[1])
        m = rangeM[2] - rangeM[0]*k
        return k*value + m

    #Returns the proper color depending on the value, color value being of hexadecimal
    def __getColor(self,value):
        if (value < 0):
            return self.__valueToHex(0)
        if True:
            return self.__valueToHex(value)

    #converts a lumos-value to a color-value (hexadecimal)
    def __valueToHex(self,value):
        rgb = self.__rgb
        colorValue = self.__mapper(value)
        return '#%02x%02x%02x' % (int(colorValue * rgb[0]),int(colorValue * rgb[1]),int(colorValue*rgb[2]))

    #Draws the shadow twice mirror-symmetric to make it more T H I C C 
    def __drawShadow(self,data,pivotPoints):
        pp = [2*pivotPoints[0],2*pivotPoints[1]]
        pixelSize = self.__pixelSize

        for i in data:
            self.__canvas.create_rectangle(i[0] ,i[1] ,i[0] + pixelSize ,i[1] + pixelSize ,fill = "#000000" , outline = "#000000")

        for i in data:
            self.__canvas.create_rectangle(-i[0] + pp[0],-i[1] + pp[1],-i[0] + pixelSize + pp[0],-i[1] + pixelSize + pp[1] ,fill = "#000000", outline = "#000000")
        
    #This void draws the actual sphere by creating small rectangles next to each other according to the spheres location
    def drawSphere(self,x,y):
        pixelSize = self.__pixelSize
        cooridnates = self.__sphere.getNormalCoordinates(x,y)
        sphereRender = SphereRender(self.__sphere,self.__density,cooridnates,pixelSize)
        data,sdata = sphereRender.getRenderData() #Get the matrix with all the light-values
        xoffset,yoffset = self.__sphere.getXYoffset(pixelSize,self.__density) #get the x and y-offset
        pivotpoints = sphereRender.getPivotPoints() #get the pivotpoints (or center of shadow) 
        self.__drawShadow(sdata,pivotpoints) #draws the shadow before drawing the sphere
        
        a = xoffset
        for i in data:
            b = yoffset
            for j in i:
                if j == 0:
                    b += pixelSize
                    continue
                lumos = self.__getColor(j)
                self.__canvas.create_rectangle(a,b,a + pixelSize, b + pixelSize, fill = lumos, outline ="")
                b += pixelSize
            a += pixelSize
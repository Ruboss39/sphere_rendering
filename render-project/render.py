import math

class SphereRender:
    #densiteten anges i punkter per längdenhet
    #This class is higly mathematical and calculates the cos-angle between two vectors in a given area
    #This area is nothing but a set of points
    def __init__(self,sphere,density,coordinate,pixelSize = 10):
        self.__sphere = sphere
        self.__density = density
        self.__coordinate = coordinate
        self.__backgroundDepth = sphere.getRadius()
        self.__pixelSize = pixelSize
        self.__coordinate.append(self.__getZ0())
    
    #This function returns Z0, which is the z0-coord for where the light vector is orthogonal to the sphere-body.
    #This function is only used by this class
    def __getZ0(self):
        radius = self.__sphere.getRadius()
        x = self.__coordinate[0]
        y = self.__coordinate[1]
        z = math.sqrt(math.pow(radius,2) - math.pow(x,2) - math.pow(y,2))
        return z
    
    def getSphere(self):
        return self.__sphere

    def getDensity(self):
        return self.__density

    #A check-function to see whether or not the examined point lies on the sphere
    def __noLight(self,x,y,r):
        if (math.pow(r,2) - math.pow(x,2) - math.pow(y,2) < 0 ):
            return True 
        else :
            return False
            
    #This function calculates the cos-angle which we will interpret as how much light reflects
    def __calculateLumos(self,x,x0,y,y0,z,z0,r):
        return (x*x0 + y*y0 + z*z0)/ (math.pow(r,2))

    #This function creates the map of points, of whom shall be calculated
    def __createRangeList(self):
        rList = []
        radius = self.__sphere.getRadius()
        points = int(self.__density * 2 * radius + 0.5)
        for i in range(0,points + 1):
            rList.append(-radius + i/(self.__density))
        return rList

    #Center of the shadow
    def getPivotPoints(self):
        return self.__getShadowCoordinate(self.__coordinate[0],self.__coordinate[1],self.__coordinate[2],self.__coordinate[2])

    #Returns the shadow-coordinate, meaning the coordinate where the light that passes through the spehere hits the background
    def __getShadowCoordinate(self,x0,y0,z0,z01):
        #These sets of comments requires the reader to understand linear algebra
        #Please reattend the course if this understanding is not found
        
        p = self.__pixelSize*self.__density #P is a factor that adjusts the location
        x01 = self.__coordinate[0]
        y01 = self.__coordinate[1]
        z = self.__backgroundDepth #Z is the coord of where the background-plane lies
        x = p*x0 + p*x01*((-z-z0)/z01) + self.__sphere.getCenterX() #This math-code computes the corresponding x-coord that lies in the shadow
        y = p*y0 + p*y01*((-z-z0)/z01) + self.__sphere.getCenterY()
        return [x,y]

    #This function goes through every point in our map and calculates the cos-angle of that point. The cos-angle-value is called lumos
    #If there is a lumos-value that is not 0, that means som light is hitting the ball, meaning there will be a shadowcoordinate.
    def getRenderData(self):
        dataMatrix = []
        sDataList = []
        radius = self.__sphere.getRadius()
        x0 = self.__coordinate[0]
        y0 = self.__coordinate[1]
        z0 = math.sqrt(math.pow(radius,2) - math.pow(x0,2) - math.pow(y0,2))
        rangeList = self.__createRangeList()
        for x in rangeList:
            tmpColumn = []
            for y in rangeList:
                lumos = 0
                if (self.__noLight(x,y,radius)): #If lumos is 0 there will be no lighth
                    tmpColumn.append(0)
                    continue
                else:
                    z = math.sqrt(math.pow(radius,2) - math.pow(x,2) - math.pow(y,2))
                    lumos = self.__calculateLumos(x,x0,y,y0,z,z0,radius)
                    tmpColumn.append(lumos)
                    if lumos !=0: # if there is light there will be a shadow
                        sDataList.append(self.__getShadowCoordinate(x,y,z,z0))
            dataMatrix.append(tmpColumn)
        return dataMatrix,sDataList
import math

#A simple class that contatins values that define a sphere and where it lies in the space
#Two special methods who returns the normal coords from x and y coords
class Sphere:
    def __init__(self,radius,centerX,centerY,centerZ):
        self.__radius = abs(radius)
        self.__centerX = centerX
        self.__centerY = centerY
        self.__centerZ = centerZ

    def getRadius(self):
        return self.__radius

    def getCenterX(self):
        return self.__centerX
    
    def getCenterY(self):
        return self.__centerY

    def getCenterZ(self):
        return self.__centerZ

    #This is simply maths
    #This mathematical function will 'scale' every sphere so that the coordinates are lying on the sphere's surface
    #It will den take notes of those coordinates and then return those coordinates, but of the descaled sphere (original size)
    #The sphere will always be facing the pointer
    def getNormalCoordinates(self,x,y):
        x0 = self.__centerX
        y0 = self.__centerY
        z0 = self.__centerZ
        radius = self.__radius
        tmp = math.sqrt(math.pow(x - x0,2) + math.pow(y - y0 ,2)) #tmp is the distance between (x,y) and (x0,y0)
        radiusH = math.sqrt(math.pow(tmp,2) + math.pow(z0,2)) #RadiusH is the distane between tmp and z0, where tmp and z0 can be interpreted as two vectors orthogonal to eachother
        xPoint = (x -x0)/(radiusH) * radius #RadiusH is the distance from the mouse to the sphere's center
        yPoint = (y -y0)/(radiusH) * radius #This math-code returns the point of where the line hits the spheres surface 
        return [xPoint,yPoint]

    #This void is a little bit out of place, but it returns the offset that is needed for tkinterRender to properly draw the sphere in
    #The right location
    def getXYoffset(self,pixelSize,density):
        x0 = self.__centerX
        y0 = self.__centerY
        radius = self.__radius
        xoffset = x0 -radius*pixelSize*density
        yoffset = y0 -radius*pixelSize*density
        return xoffset,yoffset        
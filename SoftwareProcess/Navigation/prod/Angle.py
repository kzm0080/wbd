'''
Created on Sep  02, 2016

@author: KIRAN KUMAR MEDASANI
'''
import math

class Angle():
    def __init__(self):
        self.degrees = 0  # initializing the angle to 0 degrees at the start
        self.minutes = 0.0  # initializing the angle to 0 minutes at the start
        
    def setDegrees(self, degrees=None):  # Set the degrees to none 
        if(degrees == None):
            #raise ValueError("Angle.setDegrees: Degrees should not be empty")
            degrees=0
        
        if(isinstance(degrees, (int, float))):  # Check whether the degrees are number or float          
            try:  # Starting Exception handling using try block               
                if(float(degrees)):                                                      
                    degMod = self.degreesMod(degrees)  # Gets degrees depending on the input 
                    
                    
                    self.degrees =float(degMod)#round(degMod, 1)  # Assigning the result to degrees
                    self.minutes = 0.0
                    #self.getMinutesFromDegrees(self.degrees)
                else:  # if degrees are integer
                    degMod = self.degreesMod(degrees)  # Get degrees as output
                    self.degrees = degMod  # Assigning degrees
                    self.minutes = 0.0  # Assigning Minutes
                return self.degrees
            except:
                raise ValueError("Angle.setDegrees: Invalid data")            
        else:  # If degrees received are Non Integer and Float numbers                       
            raise ValueError("Angle.setDegrees: Invalid data in degrees, should be either integer or float")
    
                
    def setDegreesAndMinutes(self, angleString=None):
        
        # Creating variables for allocating degrees
        angleDeg = 0
        angleMin = 0.0
        angleStr = 0
        if(angleString == None):  # If None
            raise ValueError("Angle.setDegreesAndMinutes: Invalid angle string")
        angleSplit = angleString.split("d")  # Split angle based on 'd' separator      
        if len(angleSplit) < 2:  # If length is less than two
            raise ValueError("Angle.setDegreesAndMinutes: Missing Separator 'd'")
        elif len(angleSplit) > 2:  # If length is greater than two 
            raise ValueError("Angle.setDegreesAndMinutes: More than one 'd' separator is not allowed")
        elif angleString.startswith("d"):  # If angle starts with 'd'
            raise ValueError("Angle.setDegreesAndMinutes: Missing degrees")
        elif angleString.endswith("d"):  # If angle ends with 'd'
            raise ValueError("Angle.setDegreesAndMinutes: Missing Minutes")
        elif "." in angleSplit[0]:  # Check if degrees is float
            raise ValueError("Angle.setDegreesAndMinutes: Degrees must be integer")
        if(angleSplit[0] == "0" or angleSplit[0] == "-0"):  # Check if angle is zero 
            pass                              
        elif(not int(angleSplit[0])):  # Degrees Accepts only integers           
            raise ValueError("Angle.setDegreesAndMinutes: Degrees must be integer")
        elif(angleSplit[1].startswith('-')):  # Minutes needs to be positive 
            raise ValueError("Angle.setDegreesAndMinutes: Minutes must be positive")
        
                 
        angleDeg = int(angleSplit[0])    
        angleStr = angleDeg     
        if float(angleSplit[1]) > 60:  # If minutes are greater than Sixty          
            try:                
                angleMin = float(angleSplit[1]) / 60  # Converting Minutes to degrees
                angleMinMod = float(angleSplit[1]) % 60      
                if angleDeg < 0:  # If degrees are less than zero                                                
                    angleDeg = angleDeg - angleMin  # Sub to get result degrees              
                else:
                    angleDeg = angleDeg + angleMin  # Add to get result degrees             
            except:
                raise ValueError("Angle.setDegreesAndMinutes: Invalid data")
        else:  # If minutes are less than Sixty
            try:                            
                angleMin = float(angleSplit[1]) / 60  # Converting Minutes to degrees
                angleMinMod = float(angleSplit[1]) % 60              
                if angleDeg < 0:  # If degrees are less than zero                                    
                        angleDeg = angleDeg - angleMin  # Sub to get result degrees             
                else:
                        angleDeg = angleDeg + angleMin  # Add to get result degrees
                                                                              
                angleDeg = round(angleDeg, 1)
            except:           
                raise ValueError("Angle.setDegreesAndMinutes: Invalid data") 
            
        angleDeg = self.degreesMod(float(angleDeg))  # Get Degrees
       
      
        self.degrees = angleStr  # Adding Original degrees to variable
        self.minutes = angleMinMod
        return angleDeg
        
          
    def add(self, angle=None):         
        if angle == None:  # If None
            angle="0d0.0"
        else:
            if  isinstance(angle, Angle):
                angle=str(int(angle.degrees))+"d"+ str(angle.minutes)
            else:
                angle=angle
       
        try:    
            angleDegree = angle.split("d")
            if len(angleDegree) < 2:  # If length is less than two
                raise ValueError("Angle.compare: Missing Separator 'd'")
            elif len(angleDegree) > 2:  # If length is greater than two 
                raise ValueError("Angle.compare: More than one 'd' separator is not allowed")
            elif angle.startswith("d"):  # If angle starts with 'd'
                raise ValueError("Angle.compare: Missing degrees")
            elif angle.endswith("d"):  # If angle ends with 'd'
                raise ValueError("Angle.compare: Missing Minutes") 
             
          
            
            self.degrees += self.getDegreesMinutes(angle, "D")  # Get Degrees from angle
           
            self.minutes += self.getDegreesMinutes(angle, "M")  # Get Minutes from angle    
           
            return self.getDegrees()
        except:
            raise ValueError("Angle.add: Invalid Angle")
            
    
    def subtract(self, angle=None):
        if angle == None:  # If None
            angle="0d0.0"
        else:
            if  isinstance(angle, Angle):
                angle=str(int(angle.degrees))+"d"+ str(angle.minutes)
            else:
                angle=angle
        try:
            angleDegree = angle.split("d")
            if len(angleDegree) < 2:  # If length is less than two
                raise ValueError("Angle.compare: Missing Separator 'd'")
            elif len(angleDegree) > 2:  # If length is greater than two 
                raise ValueError("Angle.compare: More than one 'd' separator is not allowed")
            elif angle.startswith("d"):  # If angle starts with 'd'
                raise ValueError("Angle.compare: Missing degrees")
            elif angle.endswith("d"):  # If angle ends with 'd'
                raise ValueError("Angle.compare: Missing Minutes") 
            
            self.degrees -= self.getDegreesMinutes(angle, "D")  # Get Degrees from angle
            self.minutes -= self.getDegreesMinutes(angle, "M")  # Get Minutes from angle

            return self.getDegrees()
        except:
            raise ValueError("Angle.Subtract: Invalid Angle")
    
    def compare(self, angle=None):        
        if angle == None:  # If None
            angle="0d0.0"
        else:
            if  isinstance(angle, Angle):
                angle=str(int(angle.degrees))+"d"+ str(angle.minutes)
            else:
                angle=angle       
        try:                
            angleDegree = angle.split("d")
            if len(angleDegree) < 2:  # If length is less than two
                raise ValueError("Angle.compare: Missing Separator 'd'")
            elif len(angleDegree) > 2:  # If length is greater than two 
                raise ValueError("Angle.compare: More than one 'd' separator is not allowed")
            elif angle.startswith("d"):  # If angle starts with 'd'
                raise ValueError("Angle.compare: Missing degrees")
            elif angle.endswith("d"):  # If angle ends with 'd'
                raise ValueError("Angle.compare: Missing Minutes")            
          
            getMinute = self.minutes / 60  # Get degrees from minutes
            getMinute = float(getMinute)
            getMinute = round(getMinute, 1)  # Round to one decimal
            compDegree = (self.degrees + getMinute) % 360  # Get degrees as modulus of degrees and minutes
            
             
            self.degrees = self.getDegreesMinutes(angle, "D")  # Get Degrees from angle
            self.minutes = self.getDegreesMinutes(angle, "M")  # Get Minutes from angle
    
            comp1Degree = self.getDegrees()       
    
            if compDegree > comp1Degree:
                return 1
            elif compDegree < comp1Degree:
                return -1
            else:
                return 0
       
        except:
            raise ValueError("Angle.add: Invalid Angle")
                
    def getString(self):
        return str(int(self.degrees)) + "d" + str(round(self.minutes, 1/10))  # Get string from degrees and minutes
    
    def getDegrees(self):       
       
        getMinute = self.minutes / 60  # Get degrees from minutes
               
        getMinute = float(getMinute)
        #getMinute=round(getMinute,1)
       
        cDegrees= (self.degrees + getMinute) % 360  # Get degrees as modulus of degrees and minutes    
        
        return cDegrees
    # Method to get degrees
    # Used in setDegrees
    def degreesMod(self, degrees):                   
        self.degrees = degrees % 360
        return self.degrees 
    
    # Method to get minutes from degrees
    # Used in setDegrees to set Minutes
    def getMinutesFromDegrees(self, degrees):
        degSplit = str(degrees).split(".")  # Split degrees for minutes
        minSplit = float("0." + degSplit[1])  # Add the decimal and convert to float      
        self.minutes = minSplit * 60  # Convert to minutes
    
    # Method to get degrees and minutes from angle
    # Used in add,subtract
    def getDegreesMinutes(self, angle, split):
        if split == "D":  # For degrees
           
            return int(angle.split("d")[0])
        else:  # For Minutes
            if(angle.startswith("-")):
                return float("-" + angle.split("d")[1])
            else:                
                return float(angle.split("d")[1])
            
        

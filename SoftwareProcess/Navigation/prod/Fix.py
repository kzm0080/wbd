'''
Created on Oct , 2016

@author: Kirankumar
'''


from datetime import *
from time import timezone
import time
from __builtin__ import str
from string import upper, lower, lowercase
from math import *
import xml.dom.minidom
import xml.etree.ElementTree
import Angle as Angle
import math



class Fix(object):
    '''
    classdocs
    '''
    # Constructor of the class
    def __init__(self, logFile="log.txt"):
        self.logFileOpen=""
        
        if(logFile == None):  #If log file name received is empty 
            raise ValueError("Fix.__init__: log file name should not be empty")  #Check if the file name is empty
        
        elif (isinstance(logFile, str) == False):
            raise ValueError("Fix.__init__: log file name must be string")  #
                   
        elif len(logFile) < 1: # Check the log file length
            raise ValueError("Fix.__init__: Invalid file name") # Raise exception if the file name does not match
        
       
        else:
            try:  # Start to handle exceptions           
            
                logFileOpen=open(logFile,"a") # To open the flat file            
                self.logFileOpen=logFileOpen

                logDate=self.gettimeUTC() # Getting the date time with time zone
                # Creating a log entry
                self.logFileOpen.write("LOG:\t" + logDate + ":\t Start of log\n")
                #self.writeLog(logMsg="Start of log")
                
            except ValueError: # Return this exception if any error
                raise ValueError("Fix.__init__:  Can not create log file")
    
    def writeLog(self,logMsg):
        self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\t " + logMsg + "\n")
    
    # Created a new method for time
    # Method returns the time as per the time zone to write into log file
    def gettimeUTC(self):
        try:            
            gmtTime = time.gmtime()
            logHour = time.localtime().tm_hour
            self.UTCoffset = str((gmtTime.tm_hour - logHour)%12 + 1)+ ":00"            
            getTime = str(gmtTime.tm_hour) + ":" + str(gmtTime.tm_min) + ":" + str(gmtTime.tm_sec) + " "       
            localDate=str(date.today()) + "\t" + getTime + "-" + self.UTCoffset
            return localDate   # returns the time
        
        except ValueError: # Return this exception if any error
            raise ValueError("Fix.gettimeUTC:  Unable to get time zone")
    
   
    # Created a new method for xml
    # Method returns true if it read the xml
    # Writes a log entry as starting the sighting file
    def setSightingFile(self,sightingFile=None):
        if(sightingFile == None):  #If log file name received is empty 
            raise ValueError("Fix.setSightingFile: select sighting file to import")  #Check if the file name is empty
        elif not isinstance(sightingFile, str):        
            raise ValueError("Fix.setSightingFile:  sighting file must be string")  #Check if the file name is string
        elif "." not in sightingFile:
            raise ValueError("Fix.setSightingFile:  Select a valid sighting file")  #Check if the file name is string
             
        sFile = sightingFile.split(".") # Split the xml file to check
        sFileName=sFile[0] # Take the first part of the split
        
        if len(sFileName) < 1: # If the length of file name is zero
            raise ValueError("Fix.setSightingFile:  Invalid file name")
        elif upper(sFile[1])!="XML": # If extension is not xml 
            raise ValueError("Fix.setSightingFile:  Select sighting file")
        
        self.sightingFile = sightingFile # Assigning the name
        
        try:
            # Write the log file
            self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\tStart of sighting file " + self.sightingFile + "\n")
        except ValueError: # Return this exception if any error
            raise ValueError("Fix.setSightingFile:  Can not write to log file")
        try:
            # Write the log file
            chkXMLExists=open(self.sightingFile,"r")
            chkXMLExists.close()            
        except: # Return this exception if any error
            raise ValueError("Fix.setSightingFile: True, Can not find the xml file or a new file")  
        return False # Returns false if exists, true if new
    
    # Method to parse the sighting tag 
    # Implemented the selected conditions as applied
    def getXMLElement(self,tagName,tagID,tagData):
        
        try:
            # tag name is name of the measurement
            # get the data from the measurement
            tagXMLSighting= tagData.getElementsByTagName(tagName)[0]
            tagXMLSightingValue= tagXMLSighting.childNodes[0].data    
               
        except: #if any error in reading the data
            if tagID in (1,2,3,4) : # if tag name is body,date, time,observation
                raise ValueError("Fix.getSightings-getXMLElement: " + tagName +"  tag is missing in sighting : "+ tagData)
            elif tagID==5: # if tag name is height  
                tagXMLSightingValue=0 # sets to default value
            elif tagID==6:# if tag name is temperature
                tagXMLSightingValue=72 # sets to default value
            elif tagID==7: # if tag name is pressure
                tagXMLSightingValue=1010 # sets to default value
            elif tagID==8: # if tag name is horizon
                tagXMLSightingValue="natural" # sets to default value
        
        
        # Checking validations for all the tag names        
        if tagID==1: # for body              
            self.body=tagXMLSightingValue
        elif tagID==2: #check if date is in yyyy-mm-dd format
            if datetime.strptime(tagXMLSightingValue, '%Y-%m-%d'):             
                self.date=tagXMLSightingValue
            else:
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag should be in YYYY-MM-DD format in sighting : "+ tagData)
        elif tagID==3:    # check if time is in hh-mm-ss format
            print tagXMLSightingValue             
            if datetime.strptime(tagXMLSightingValue, '%H:%M:%S'):             
                self.time=tagXMLSightingValue
            else:
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag should be in hh:mm:ss format in sighting : "+ tagData)            
        elif tagID==4:   # Check the observation
            if self.chkObservationValidation: # validate the angle
                chkObservation=Angle.Angle()
                observedAltitude= chkObservation.setDegreesAndMinutes(tagXMLSightingValue)# Using method in angle class
                if chkObservation.degrees < 0 :  
                    raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag degrees should be greater than or equal zero in sighting : "+ tagData)       
                elif chkObservation.degrees > 90 :  
                    raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag degrees should be less than or equal to 90 in sighting : "+ tagData)
                if chkObservation.minutes < 0 :  
                    raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag minutes should be greater than or equal zero in sighting : "+ tagData)       
                elif chkObservation.minutes > 60 :  
                    raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag minutes should be less than or equal to 60 in sighting : "+ tagData)                       
                if chkObservation.degrees == 0 :
                    if chkObservation.minutes == 0.1 :
                        raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag observed altitude is LT 0d0.1  in sighting : "+ tagData) 
                self.degrees=chkObservation.degrees
                self.minutes=chkObservation.minutes
                self.observedAltitude=observedAltitude
                
                self.observation=tagXMLSightingValue
        elif tagID==5: # if height               
            self.height=tagXMLSightingValue
        elif tagID==6: # if temperature               
            self.temperature=int(tagXMLSightingValue)
            if self.temperature < -20 :  
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag temperature should be greater than or equal to zero in sighting : "+ tagData)       
            elif self.temperature > 120 :  
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag temperature should be less than or equal to 120 in sighting : "+ tagData)
        elif tagID==7: # if pressure          
            self.pressure=int(tagXMLSightingValue)
            if self.pressure < 100 :  
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag pressure should be greater than or equal to 100 in sighting : "+ tagData)       
            elif self.pressure > 1100 :  
                raise ValueError("Fix.getSightings-getXMLElement: " +tagName +"  tag pressure should be less than or equal to 1100 in sighting : "+ tagData)
        elif tagID==8: #if horizon
            self.horizon=tagXMLSightingValue
            
    # Method to validate the parameter passed in the observation
    # Returns true if passes
    def chkObservationValidation(self,angleString):
        if(angleString == None):  # If None
            raise ValueError("Fix.chkObservationValidation: Invalid angle string")
        angleSplit = angleString.split("d")  # Split angle based on 'd' separator      
        if len(angleSplit) < 2:  # If length is less than two
            raise ValueError("Fix.chkObservationValidation: Missing Separator 'd'")
        elif len(angleSplit) > 2:  # If length is greater than two 
            raise ValueError("Fix.chkObservationValidation: More than one 'd' separator is not allowed")
        elif angleString.startswith("d"):  # If angle starts with 'd'
            raise ValueError("Fix.chkObservationValidation: Missing degrees")
        elif angleString.endswith("d"):  # If angle ends with 'd'
            raise ValueError("Fix.chkObservationValidation: Missing Minutes")
        elif "." in angleSplit[0]:  # Check if degrees is float
            raise ValueError("Fix.chkObservationValidation: Degrees must be integer")
        if(angleSplit[0] == "0" or angleSplit[0] == "-0"):  # Check if angle is zero 
            pass                              
        elif(not int(angleSplit[0])):  # Degrees Accepts only integers           
            raise ValueError("Fix.chkObservationValidation: Degrees must be integer")
        elif(angleSplit[1].startswith('-')):  # Minutes needs to be positive 
            raise ValueError("Fix.chkObservationValidation: Minutes must be positive")
        elif(angleSplit[1].endswith('.')):  # Minutes needs to be positive 
            raise ValueError("Fix.chkObservationValidation: Minutes must be valid float value , Should not end with .")
        elif(angleSplit[1].startswith('.')):  # Minutes needs to be positive 
            raise ValueError("Fix.chkObservationValidation: Minutes must be valid float value, Should not start with .")
        elif(angleSplit[1] > 60):  # Minutes needs to be positive 
            raise ValueError("Fix.chkObservationValidation: Minutes must be valid float value")
        
        return True
    
    # Method to get and process data of sighting file.
    # Calculate and returns the values. 
    def getSightings(self):
        approximateLatitude = "0d0.0"    # set the approximate latitude to zero        
        approximateLongitude = "0d0.0"   # set the approximate longitude to zero

        try:
            # Check of xml exists
            chkXMLExists=open(self.sightingFile,"r")
            chkXMLExists.close()            
        except: # Return this exception if any error
            raise ValueError("Fix.getSightings: Can not find the xml file or a new file")
        try:
            xnlImport = xml.dom.minidom.parse(self.sightingFile)  # Parse the xml file for reading data
        except Exception:
            raise ValueError("Fix.getSightings:  Can not parse the xml sighting file")
        
        # Code to get the root element
        root=xml.etree.ElementTree.parse(self.sightingFile).getroot()
        
        # Code to check if the root element is fix
        if root.tag=="fix":
            getXML = xnlImport.documentElement
            
            sighting = getXML.getElementsByTagName("sighting") # Get the elements in the sighting tag
                        
            for tagData in sighting: # for each sighting data           
                self.getXMLElement('body', 1, tagData) # if tag name is body
                self.getXMLElement('date', 2, tagData) # if tag name is date
                self.getXMLElement('time', 3, tagData)  # if tag name is time
                self.getXMLElement('observation', 4, tagData)  # if tag name is observation 
                self.getXMLElement('height', 5, tagData)  # if tag name is height
                self.getXMLElement('temperature', 6, tagData)  # if tag name is temperature
                self.getXMLElement('pressure', 7, tagData) # if tag name is pressure
                self.getXMLElement('horizon', 8, tagData) # if tag name is horizon
                print self.body
                print self.date
                print self.time
                print self.observation
                print self.height
                print self.temperature
                print self.pressure
                print self.horizon
                
                dip=0.0 # cal dip, defaults to zero
                try:                    
                    if lower(self.horizon)=="natural": # if horizon is natural
                        dip = (-0.97 * sqrt(float(self.height))) / 60.0
                    else:
                        dip=0.0 # default to zero
                except: # Return this exception if any error
                    raise ValueError("Fix.getSightings:  can not calculate dip")
                    
                pressure= float(self.pressure) # converting pressure to float
                tempareture=float(self.temperature) # converting temperature to float
                
                try:
                    # calculate adjusted altitude
                    refraction = ( -0.00452 * pressure) / ( 273 + ((tempareture-32)*5)/9) / math.atan(self.observedAltitude)             
        
                    adjustedAltitude = self.observedAltitude + dip + refraction
                    #adjustedAltitude=round(adjustedAltitude,1/10)
                    angle=Angle.Angle()
                    angle.setDegrees(adjustedAltitude)
                    
                    aString=angle.getString()
                    # adjustedAltitude=round(adjustedAltitude,1/10) # adjusting to the nearest 0.1
                    
                except: # Return this exception if any error
                    raise ValueError("Fix.getSightings:  can not calculate adjustedAltitude")
                
                try:
                    self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\t" + self.body + "\t" + self.date + "\t" + self.time + "\t" + aString + "\n")
                except: # Return this exception if any error
                    raise ValueError("Fix.getSightings:  can not write measurements to log file")
            try:
                self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\tEnd of sighting file " + self.sightingFile + "\n")
                self.logFileOpen.close()
            except: # Return this exception if any error
                raise ValueError("Fix.getSightings:  can not close the log file")
        else:
            raise ValueError("Fix.getSightings:  No fix tag in xml sighting file")
        
        # adding latitude and longitude to tuple
               
        approximateLocation=[]
              
        approximateLocation.append({                
                approximateLatitude  : approximateLatitude,
                approximateLongitude :approximateLongitude
        })
        
        return approximateLocation
        
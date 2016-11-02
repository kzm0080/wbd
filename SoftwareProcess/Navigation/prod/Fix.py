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
import os
from _ast import Str



class Fix(object):
    '''
    classdocs
    '''
    # Constructor of the class
    def __init__(self, logFile="log.txt"):
        self.logFileOpen=""
        self.sightingError = 0
        
        if(logFile == None):  #If log file name received is empty 
            raise ValueError("Fix.__init__: log file name should not be empty")  #Check if the file name is empty
        
        elif (isinstance(logFile, str) == False):
            raise ValueError("Fix.__init__: log file name must be string")  # Check if it is string
                   
        elif len(logFile) < 1: # Check the log file length
            raise ValueError("Fix.__init__: Invalid file name") # Raise exception if the file name does not match
        
       
        else:
            try:  # Start to handle exceptions           
            
                logFileOpen=open(logFile,"a") # To open the flat file            
                self.logFileOpen=logFileOpen # Assigning to the global
                
                logPath= os.path.abspath(logFile) # Getting the path of the flat file

                logDate=self.gettimeUTC() # Getting the date time with time zone
                
                # Creating a log entry                
                self.logFileOpen.write("LOG:\t" + logDate + "\t " + "Log File:\t "+ logPath +" \n")
                #self.writeLog(logMsg="Start of log")
                
            except ValueError: # Return this exception if any error
                self.sightingError += 1
                raise ValueError("Fix.__init__:  Can not create log file")
            
            
    def setAriesFile(self, ariesFile):
        
        if(ariesFile == None):  #If aries file name received is empty 
            raise ValueError("Fix.setAriesFile: aries file name should not be empty")  #Check if the file name is empty
        
        elif (isinstance(ariesFile, str) == False):
            raise ValueError("Fix.setAriesFile: aries file name must be string")  # Check if it is string
                   
        elif len(ariesFile) < 1: # Check the log file length
            raise ValueError("Fix.setAriesFile: Invalid file name") # Raise exception if the file name does not match
        
        aFile=ariesFile.split(".")
        aFileSplit = aFile[0]
        
        # Check if the split string has the correct length
        if (len(aFile)) <= 1:
            self.sightingError += 1
            raise (ValueError("Fix.setAriesFile:  Invalid file name"))
        elif upper(aFile[1])!="TXT": # If extension is not text 
            raise ValueError("Fix.setAriesFile:  Invalid file name")
        
        self.ariesFile = aFileSplit + ".txt"   # Assign to the global         
       
        ariesPath = os.path.abspath(self.ariesFile)  # get file path of file
        
        logDate=self.gettimeUTC() # Getting the date time with time zone
    
        
        self.logFileOpen.write("LOG:\t" + logDate + "\t " + "Aries File:\t "+ ariesPath +" \n")
       
        # checking ariesfile is exist or not.
        try:
            f = open(self.ariesFile, "r")
            f.close()
        except Exception as e:
            raise (ValueError("Fix.setAriesFile:  Aries file could not be opened"))
        # return full path of aries file.
        return ariesPath
    
    
    def setStarFile(self, starFile):
        
        if(starFile == None):  #If aries file name received is empty 
            raise ValueError("Fix.setStarFile: Star file name should not be empty")  #Check if the file name is empty
        
        elif (isinstance(starFile, str) == False):
            raise ValueError("Fix.setStarFile: Star file name must be string")  # Check if it is string
                   
        elif len(starFile) < 1: # Check the log file length
            raise ValueError("Fix.setStarFile: Invalid file name") # Raise exception if the file name does not match
        
        stFile=starFile.split(".")
        starFileSplit = stFile[0]
        
        # Check if the split string has the correct length
        if (len(stFile)) <= 1:
            self.sightingError += 1
            raise (ValueError("Fix.setStarFile:  Invalid file name"))
        elif upper(stFile[1])!="TXT": # If extension is not text 
            raise ValueError("Fix.setStarFile:  Invalid file name")
               
        
        self.starFile = starFileSplit + ".txt"  # set star file as global.
        
        starFilePath = os.path.abspath(self.starFile) # get full path of star file.
        
        logDate=self.gettimeUTC() # Getting the date time with time zone

        # make a string of filename and file full path with current datetime.
        self.logFileOpen.write("LOG:\t" + logDate + "\t " + "Star File:\t "+ starFilePath +" \n")

        # checking stars file is exist or not.
        try:
            f = open(self.starFile, "r")
            f.close()
        except Exception as e:
            raise (ValueError("Fix.setStarFile:  Stars file could not be opened"))
        # return full path of aries file.
        return starFilePath


    
       
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
            sightingPath = os.path.abspath(self.sightingFile)
            # Write the log file
            self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + "\t Sighting file:\t " + sightingPath + "\n")
        except ValueError: # Return this exception if any error
            self.sightingError += 1
            raise ValueError("Fix.setSightingFile:  Can not write to log file")
        try:
            # Write the log file
            chkXMLExists=open(self.sightingFile,"r")
            chkXMLExists.close()                  
        except: # Return this exception if any error
            self.sightingError += 1
            raise ValueError("Fix.setSightingFile: True, Can not find the xml file or a new file")  
        return sightingPath # Returns false if exists, true if new
    
    # Method to parse the sighting tag 
    # Implemented the selected conditions as applied
    def getXMLElement(self,tagName,tagID,tagData):
        
        try:
            # tag name is name of the measurement
            # get the data from the measurement
            tagXMLSighting= tagData.getElementsByTagName(tagName)[0]
            tagXMLSightingValue= tagXMLSighting.childNodes[0].data    
               
        except: #if any error in reading the data
            self.sightingError += 1
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
        
        # adding latitude and longitude to tuple
               
        approximateLocation=[]
              
       

        try:
            # Check of xml exists
            chkXMLExists=open(self.sightingFile,"r")
            chkXMLExists.close()            
        except: # Return this exception if any error
            raise ValueError("Fix.getSightings: Can not find the xml file or a new file")
        try:
            xnlImport = xml.dom.minidom.parse(self.sightingFile)  # Parse the xml file for reading data
        except Exception:
            self.sightingError += 1
            raise ValueError("Fix.getSightings:  Can not parse the xml sighting file")
        
        # Code to get the root element
        root=xml.etree.ElementTree.parse(self.sightingFile).getroot()
        
        # Code to check if the root element is fix
        if root.tag=="fix":
            getXML = xnlImport.documentElement
            
            sighting = getXML.getElementsByTagName("sighting") # Get the elements in the sighting tag
                        
            for tagData in sighting: # for each sighting data     
                createDictonary= {} # Creating for sorting the data    
                self.getXMLElement('body', 1, tagData) # if tag name is body
                self.getXMLElement('date', 2, tagData) # if tag name is date
                self.getXMLElement('time', 3, tagData)  # if tag name is time
                self.getXMLElement('observation', 4, tagData)  # if tag name is observation 
                self.getXMLElement('height', 5, tagData)  # if tag name is height
                self.getXMLElement('temperature', 6, tagData)  # if tag name is temperature
                self.getXMLElement('pressure', 7, tagData) # if tag name is pressure
                self.getXMLElement('horizon', 8, tagData) # if tag name is horizon
                
                createDictonary["body"]=self.body
                createDictonary["date"]=self.date
                createDictonary["time"]=self.time
                createDictonary["observation"]=self.observation
                createDictonary["height"]=self.height
                createDictonary["temperature"]=self.temperature
                createDictonary["pressure"]=self.pressure
                createDictonary["horizon"]=self.horizon
                
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
                    self.sightingError += 1
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
                    createDictonary["adjustedAltitude"] = aString
                    createDictonary["datetime"] = datetime.strptime(self.date + " " + self.time, "%Y-%m-%d %H:%M:%S")
                    # adjustedAltitude=round(adjustedAltitude,1/10) # adjusting to the nearest 0.1
                    
                except: # Return this exception if any error
                    self.sightingError += 1
                    raise ValueError("Fix.getSightings:  can not calculate adjustedAltitude")
                 
                try:                        
                    # split time where received from sighting file and set hours, minutes and seconds.
                    splitHours = self.time.split(":")  # Get hours
                    tHours=splitHours[0]
                    splitMinutes = self.time.split(":") # Get Minutes
                    tMinutes=splitMinutes[1]
                    splitSeconds = self.time.split(":") # Get Seconds
                    tSeconds=splitSeconds[2]
                    
                    # convert minutes in seconds
                    mSeconds = (int(tMinutes) * 60) 
                    mSeconds = mSeconds+ int(tSeconds)
                    self.mSeconds=mSeconds
                     
                    chkDate = datetime.strptime(self.date, '%Y-%m-%d').strftime('%m/%d/%y') # Format date
                                    
                                                
                except: # Return this exception if any error
                    self.sightingError += 1
                    raise ValueError("Fix.getSightings:  Can not split or format time")
                
                angle1 = Angle.Angle()  # create new Angle instance.
                
                readStar = open(self.starFile, "r") # open stars file in read mode.
        
                findBody = False # Taken a boolean value to find whether the star file contains data or not
                                        
                
                for starData in readStar: # read each line from star file    
                    
                    sBodySplit= starData.split("\t") # split line using tab separator
                    sBody=sBodySplit[0]  # First element of each file is name
                    
                    if (isinstance(sBody, str) == False):        
                        raise ValueError("Fix.getSightings:  Name in the star file must be string")  #Check if the file name is string
                    
                    # split line and take first element as date.
                    sDateSplit = starData.split("\t") # split line using tab separator
                    sDate=sDateSplit[1] # Second element of each file is date
                    
                    # To search star file.
                    if sBody == self.body and sDate == chkDate: # if body and date match
                       
                        print sBody,sDate
                        
                        sAngleSplit=starData.split("\t") # Split the line of the matched star data
                        sAngle=sAngleSplit[2] # Get the angle
                        SHAStar = angle1.setDegreesAndMinutes(sAngle) # Get degrees and minutes from the angle
                        
                        self.SHAStar=SHAStar # Assign to global
                        
                        sLatitudeSplit=starData.split("\t")  # Split the line of the matched star data
                        sLatitude=sLatitudeSplit[3] # Get the Latitude
                        sLatitude=sLatitude.strip()
                        
                        self.starLatitude=sLatitude # Assign to global                     
                       
                        findBody = True # To check if the name and date are present 
                        
                        createDictonary["latitude"] = self.starLatitude
                
                readStar.close() # close stars file.
                
                if(findBody): # if name and date matches                                      
                    print "match"       
                else: # if name and date not found in stars file than return
                    self.sightingError += 1
                    raise ValueError("Fix.getSightings:  can not find name in star file") # returns value error
                    continue
                    
                
                readAries = open(self.ariesFile,"r")  # open aries file in read mode.
                               
                ariesAngle = Angle.Angle() # create an instance of angle.
                ariesAngle1 = Angle.Angle() # create an instance of angle.
                
                for ariesData in readAries:  # read each line form aries file.
                        
                    # To split lines
                    aDateSplit = ariesData.split("\t") # Split using tab space
                    aDate=aDateSplit[0] # Get the date from the split string
                    
                    aHoursSplit = ariesData.split("\t") # Split using tab space                    
                    aHours=aHoursSplit[1] # Get the hours from the split string                    
                   
                    aAngleSplit = ariesData.split("\t") # Split using tab space
                    aAngle=aAngleSplit[2] # Get the angle from the split string
                                                    
                    cmpHours = int(tHours) # Get Hours
                    ariesHours = int(aHours) # Get Aries Hours
                    
                    
                    if aDate == chkDate and ariesHours == cmpHours: # Check for date and hours
                        
                        
                        GHAAriesAngle = ariesAngle.setDegreesAndMinutes(aAngle) # Send to angle class to get degrees and minutes
                       
                        ObservationAngleSplit = next(readAries).split("\t") # Split using tab space
                        ObservationAngle=ObservationAngleSplit[2] # Get the angle from the split string
                        
                        GHAAriesAngle1 = ariesAngle1.setDegreesAndMinutes(ObservationAngle) # Send to angle class to get degrees and minutes
                        
                        self.GHAAriesAngle=GHAAriesAngle # Assign to global 
                        self.GHAAriesAngle1=GHAAriesAngle1 # Assign to global 
                                        
                readAries.close()  # close aries file after completion
                        
                # calculation for aries
                self.GHAAriesAngle = self.GHAAriesAngle + (self.GHAAriesAngle1 - self.GHAAriesAngle) * float(self.mSeconds)/3600
               
                self.GHAobservation = self.GHAAriesAngle + self.SHAStar  # Get observation    
               
                angle.setDegrees(self.GHAobservation)  #Set as degrees to setDegrees method.
                
                self.GHAobservation = angle.getString() # set return value of getString 
                    
                # Assigning to array       
                createDictonary["longitude"] = self.GHAobservation
                
                # add dictionary in list
                approximateLocation.append(createDictonary)
                
                # sort data 
                approximateLocation.sort(key=lambda sort: sort['body'])  # sort by body 
                approximateLocation.sort(key=lambda sort: sort['datetime'])  # sort by datetime 
                
            try:
                for val in approximateLocation: # Read each value and write in log
                                     
                    self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\t" + val["body"] + "\t" + val["date"] + "\t" + val["time"] + "\t" + val["adjustedAltitude"] + "\t" + val["latitude"] + "\t" + val["longitude"] + "\n")
            except: # Return this exception if any error
                self.sightingError += 1
                raise ValueError("Fix.getSightings:  can not write measurements to log file")
            try:
                self.logFileOpen.write("LOG:\t" + self.gettimeUTC() + ":\t" + " Sighting errors:" + "\t" + str(self.sightingError) + "\n")
                self.logFileOpen.close()
            except: # Return this exception if any error
                raise ValueError("Fix.getSightings:  can not close the log file")
        else:
            raise ValueError("Fix.getSightings:  No fix tag in xml sighting file")    
       
        return approximateLocation
        
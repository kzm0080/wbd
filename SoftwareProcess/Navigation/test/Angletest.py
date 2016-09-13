import Navigation.prod.Angle as Angle


# ---------- constructor ----------
# Instantiate angles
angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()

# Passing parameters for "setDegrees"

print "setDegrees"

angle1Degrees = angle1.setDegrees(-19.5)  # angle1Degrees should be "340.5"
print angle1Degrees

# Passing parameters for "setDegreesAndMinutes"

print "setDegreesAndMinutes"
angle1DegreesMinutes = angle1.setDegreesAndMinutes("45d30.0")  # angle1DegreesMinutes should be "45.0"
print angle1DegreesMinutes

# Passing parameters for "Add"
print "Add"

addedDegree1=angle1.add("25d10.0")
print addedDegree1

# Passing parameters for "Subtract"
print "Sub"

subDegree1=angle1.subtract("340d30.0")
print subDegree1 

# Passing parameters for "Compare"
print "Compare"

angle1Comp=angle1.compare("340d30.0")
print angle1Comp



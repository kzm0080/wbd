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

angle2Degrees = angle2.setDegrees(0.0)  # angle2Degrees should be "0.0"
print angle2Degrees

angle3Degrees = angle3.setDegrees(45)  # angle3Degrees should be "45.0"
print angle3Degrees


# Passing parameters for "setDegreesAndMinutes"

print "setDegreesAndMinutes"
angle1DegreesMinutes = angle1.setDegreesAndMinutes("45d0.0")  # angle1DegreesMinutes should be "45.0"
print angle1DegreesMinutes

angle2DegreesMinutes = angle2.setDegreesAndMinutes("0d30.0")  # angle2DegreesMinutes should be "0.5"
print angle2DegreesMinutes

angle3DegreesMinutes = angle3.setDegreesAndMinutes("-19d30.0")  # angle3DegreesMinutes should be "340.5"
print angle3DegreesMinutes

# Passing parameters for "Add"

print "Add"

addedDegree1=angle1.add("25d10.0")
print addedDegree1

angle1Comp=angle1.compare("340d60")
print angle1Comp



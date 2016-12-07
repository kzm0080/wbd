'''
Created on Oct , 2016

@author: Kirankumar
'''

import Navigation.prod.Fix as Fix

# ---------- constructor ----------
# Instantiate 
fix1 = Fix.Fix()


fixs=fix1.setSightingFile("sight.xml")
fixstar=fix1.setStarFile("stars.txt")
fixaries=fix1.setAriesFile("aries.txt")
   
print fixs

fixss=fix1.getSightings("S56d35", "89d38.3")
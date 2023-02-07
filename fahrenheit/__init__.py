# This needs to be before import clr
from pythonnet import load

load("coreclr")

import sys

import clr

# Add path to dlls
assemblydir = r"./fahrenheit"
sys.path.append(assemblydir)

# Import dlls using clr
clr.AddReference("fhcommon")
clr.AddReference("fhcorex")

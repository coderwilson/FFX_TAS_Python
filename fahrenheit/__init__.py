# This needs to be before import clr
from pythonnet import load

import sys
import clr

load("coreclr")

# Add path to dlls
assemblydir = r"./fahrenheit"
sys.path.append(assemblydir)

# Import dlls using clr
clr.AddReference("fhcommon")
clr.AddReference("fhcorex")

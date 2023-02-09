# Fahrenheit integration
This directory contains the integration of the Fahrenheit project (`https://github.com/fkelava/fahrenheit/`), which has an extensive set of enums for various things in FFX and FFX-2.

Fahrenheit is built in C#, so importing it into python is done using the `pythonnet` package (run `pip install -r requirements.txt` to add it).

Replace the dll files in the `fahrenheit` directory to update to a newer version of the library.

Usage:

```
# Parse the dlls (preferably only do this once)
# This adds the Fahrenheit.Core.X.Kernel, Fahrenheit.Core.X.Structs and Fahrenheit.Common.* modules
import fahrenheit

# Import stuff from dlls
from Fahrenheit.Core.X.Kernel import FhXBtlItemId

# Use imported enums
print(FhXBtlItemId.ITEM_POTION.value__)
print(FhXBtlItemId.ITEM_HI_POTION.value__)
print(FhXBtlItemId.ITEM_X_POTION.value__)
print(FhXBtlItemId.ITEM_MEGA_POTION.value__)
```

Note that due to how the `pythonnet` enums work, the `.value__` part is needed to get the actual numeric value of the enum, rather than its name.

To see the contents of the library, either study the source code of Fahrenheit, or use a free C# decompiler tool like `JetBrains dotPeek` to inspect the `.dll` files.

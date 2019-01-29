All-Sky Camera Operations
* Scope
1. This portion of the project is concerned with the operating the camera
2. Create the necessary software interfaces required to satisfy the presentation aspect of this project.
3. There will be no direct interaction with the acquisition portion of the software except for those items
provided via a configuration file or by some other indirect method.

* Purpose
    - Make raw FITS images available to the Presentation software


* Fundamental Requirements
1. Provide a method for automatically starting the camera exposure sequence based on the sun angle.
2. Develop an algorithm to increase/decrease exposure times based on the sun angle and sky brightness to include
the moon's contribution to the sky background.
3. Acquire and store raw FITS images


* Technical Requirements
1. Camera operation requires interaction by TOs? ?????????
2. A user configurable "config" file is to be made available to TOs at DCT. ???????
3. Make use of INDI camera driver to operate the allsky camera.
4. Modularize the camera interface such that it can easily be adapted if the camera changes.

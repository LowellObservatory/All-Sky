All-Sky Camera Operations
* Scope
    1. This portion of the project is concerned with operating the camera and acquiring images.
    2. Create the necessary software interfaces required to satisfy the presentation aspect of this project.
    3. There will be no direct interaction with the acquisition portion of the software except for those items
provided via a configuration file or by some other indirect method.

* Purpose
    - Make raw FITS images available to the Presentation software.


* Fundamental Requirements
    1. Provide a method for automatically starting the camera exposure sequence based on the sun angle.
    2. Develop an algorithm to increase/decrease exposure times based on the sun angle and sky brightness to include
the moon's contribution to the sky background.  
    3. Acquire and store raw FITS images
    4. Retrieve humidity and temperature information for activemq in a strictly consumer/listener capacity.


* Technical Requirements
    1. Camera operation requires interaction by TOs? Yes. Seen #5 below.
    2. A user configurable "config" file is to be made available to TOs at DCT. (Need more specificity for this)
    3. Make use of INDI camera driver to operate the allsky camera.
    4. Modularize the camera interface such that it can easily be adapted if the camera changes.
    5. Provide a "user interface" that allows TOs to start the camera if it has stopped taking images. The same user interface should provide a "staleness" status so that operators know whether the camera has stopped taking images.
    6. Write FITS headers in either a stand alone mode or by using LOFITS to write the headers. (TBD)
    

* Questions
    1. Does the allsky camera make complete use of the INDI protocol or does in only use the camera driver/server portion available with use of INDI?
    2. Will the ASC write its own FITS headers or will it use LOFITS to write the headers?
    3. Shall the image acquisition "pipeline" be strictly synchronous or can it be done asyncronously? How does one keep track of when a file is open for reading/writing by some other portion of the processing pipeline? Is this a question better suited for the Presentation portion of this project?
    
    

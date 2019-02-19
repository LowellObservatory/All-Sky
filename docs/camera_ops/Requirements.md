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
    4. Retrieve humidity and temperature information via activemq in a strictly consumer/listener capacity.
    5. The software must adhere to good object oriented practices and procedures to assure modularity and extensibility.


* Technical Requirements
    1. Camera operation requires interaction by TOs? Yes. Seen #5 below.
    2. A user configurable "config" file is to be made available to TOs at DCT. `(Need more specificity for this)`
    3. Make use of INDI camera driver to operate the allsky camera.
    4. Modularize the camera interface such that it can easily be adapted if the camera changes.
    5. Provide a "user interface" that allows TOs to start the camera if it has stopped taking images. The same user interface should provide a "staleness" status so that operators know whether the camera has stopped taking images.
    
    Possible "mini-ui" for TOs to monitor and control the allsky camera:
    
    ![alt text](https://github.com/LowellObservatory/All-Sky/blob/master/asc_mini_ui.png)
    
    6. Write FITS headers in either a stand alone mode or by using LOFITS to write the headers. (TBD) Which keywords should be in the file header?\
    Suggested keywords:                                                                                                                       
        1. Temperature
        2. Relative humidity
        3. LST time at exposure start
        4. Sun angle
        5. Moon angle
        6. Moon % illum
        7. bzero
        8. datamin
        9. datamax
        10. Observatory location
        11. Obs latitude
        12. Obs longitude
        13. Obs altitude
        14. Instrument name = "DCT ALLSKY"
        15. Sequence number
        16. Firmware version, when applicable
        
 The following shows the FITS head of the existing All-sky camera at DCT:
 ![alt_text](https://github.com/LowellObservatory/All-Sky/blob/master/header.png)
 
* Technical Requirements (continued)                                    
    7. File naming. Suggested file naming 'UTdate'_sequence number.fits\
       Example: 20190205_0001.fits                                             
    8. Provide a configuration file from which several parameters may be edited.  Possible items to include in the
    configuration file are as follows:                                        
       &nbsp; &nbsp; &nbsp; &nbsp; 1. Default cadence    
       &nbsp; &nbsp; &nbsp; &nbsp; 2. Default sun angle for start and end of a nightly sequence.    
       &nbsp; &nbsp; &nbsp; &nbsp; 3. Binning mode.    
       &nbsp; &nbsp; &nbsp; &nbsp; 4. Exposure min and max times.   
       &nbsp; &nbsp; &nbsp; &nbsp; 5. Camera handle, identifier or driver name needed by the software to identify the specific
                                      camera make and model.
      
* Questions
    1. Does the allsky camera make complete use of the INDI protocol or does it only use the camera driver/server portion available with use of INDI?
    2. Will the ASC write its own FITS headers or will it use LOFITS to write the headers?
    
    

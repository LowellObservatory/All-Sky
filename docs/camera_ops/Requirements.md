All-Sky Camera Operations
* Scope
    1. This portion of the project is concerned with operating the camera and acquiring images.
    2. Create the necessary software interfaces required to satisfy the presentation aspect of this project.
    3. Control of the acquisition portion of this project is limited to start and stop. Configuration of the acquisition operation will be done by a config file.

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
        17. Original file path
        
        
        
        
 The following shows the FITS header of the existing All-sky camera at DCT:
 ![alt_text](https://github.com/LowellObservatory/All-Sky/blob/master/header.png)
 
 The FITS header as written by INDI:
 ![alt_text](https://github.com/LowellObservatory/All-Sky/blob/master/indihdr.png)
 
 The proposed FITS header composed by the ASC software initially, then by LOFITS eventually:
 
 ![alt_text](https://github.com/LowellObservatory/All-Sky/blob/master/prophdr.png)\
Note: When possible retrieve information like LST at exposure start time and sun/moon angle from the TCS via the broker for puposes of the FITS header.
 
* Technical Requirements (continued)                                    
    7. File naming. Suggested file naming 'UTdate'_sequence number.fits\
       Example: 20190205_0001.fits \
    8. Include in a separate configuration file a list of the header keywords. \
    9. Provide a method to easily add new FITS keywords. The class or method(s) used to populate the FITS header must be adaptable in order to allow new keywords and associated values. \
    10. Provide a configuration file from which several parameters may be edited.  Possible items to include in the
    configuration file are as follows:                                        
       &nbsp; &nbsp; &nbsp; &nbsp; - Default cadence    
       &nbsp; &nbsp; &nbsp; &nbsp; - Default sun angle for start and end of a nightly sequence.    
       &nbsp; &nbsp; &nbsp; &nbsp; - Binning mode.    
       &nbsp; &nbsp; &nbsp; &nbsp; - Exposure min and max times.   
       &nbsp; &nbsp; &nbsp; &nbsp; - Camera handle, identifier or driver name needed by the software to identify the specific
                                     camera make and model.
                                                                         

      

    
    

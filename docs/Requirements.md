All-sky camera

* Scope:
    1. This project will provide software that will operate the allsky camera in a mostly autonomous manner, save the
       raw images and provide the overlay images which correspond in time with the sky images.
    2. Replace the existing software with something new that is well documented and tested and done through the full software
       development protocol.

* Purpose:
  - See what the weather is doing.
  - Where is the telescope pointing?  This impacts observing.
  - User community: Control room, off-site, visitor center, public access for Bob Ayers.
  - Need policy decision about whether public images show DCT pointing position.
      There seems to be a political problem with this.  Tentative answer is not to show DCT pointing.

* Functional Requirements:
 * Essential:
    1. Takes images reliably at configurable cadence.  The FITS files are stored.
    2. Image display required.
    3. Movie animation display required.
    4. Run all night without breaking or losing images on the longest night.
       [Calibration done off-line]
  * Requirements for observers and TOs:  
    1. Where is the DCT pointing?
    2. Equatorial and alt-az grids, and compass points (NSEW)
    3. Star names
  * Interaction or configuration: System
    1. Cadence (within limits)
    2. Upper limit to exposure time 
    3. Lower limit to exposure time (likely to be system dependent)
    4. Number of frames in the movie
  * Interaction or configuration: User
    1. Overlay selections (applies to still images and movies)
    2. Inverted image
    3. Make a movie of 10 frames.  The user gets to select whether the movie is
        made of every image, 10 in a row, every other image, every third one, etc.
  
* Technical Requirements:
  1. Make the camera interface software module so it can be replaced.
  2. Need a start/stop approach for TOs to re-start the system.
  3. Image display with selected overlays is via xxx (GUI? web page?)
    Public image display is without overlays.
  4. Interaction/configuration mechanism
    a) Config file controlled by TO only, by some TBD means.
    b) A browser-side configuration that can be done independently.
  5. Control the dew heater. Control the camera's built-in dew heater with a PDU
     based on the current humidity measurement.
  6. Control of the camera will be done using availabe INDI drivers. The camera control
     portion of the software will be designed such that if and when the camera is replaced
     with a different manufacture's camera very little will have to be changed with regard
     to the camera control module.
  7. The overlay grids to be provided are,
     a) Equatorial grid
     b) Alt/Az grid
     c) Star labels
     d) Moon and planets
     e) Current telescope position.
     f) Of the overlay grids to be provided only 1, item e) Telescope Position, must be 
        calculated in real time. Item d) Moon and Planets should probably also be calculated
        in real time but they could be saved during the day before the observing night.
    
* Admin-User Requirement:
  1. Provide the tools needed to realign the overlay image(s) to the allsky image after
     the camera has been moved and the orientation of the sky has changed.
  2. One possible solution will be to produce an image where bright stars
      can be selected via the mouse to very good accuracy. These pixel coordinates are
      converted to sky coordinates and offsets are applied to the overlays so that they
      align well with the sky image. 
  3. The process of realigning the images when the sky orientation has changed must be
     something anyone can do with adequate instruction.
            
* Possible extensions
  - Extinction map.
  
Questions
1. Is it possible to have the user control overlays at the browser end?  Is this even
   desirable?  This is a research project.  Dyer will research this. 
2. Night Summary Image.  The purpose of the night summary image is to provide a way for 
   determining a night's sky conditions for historical purposes in a very fast way.
   Suppose I am a student working for Michael Mommert on a project to provide weather and
   sky conditions that can be interpreted by a script for the purpose of establishing a
   threshold for opening/closing of a telescope.  I will want to use previous data in order
   to test my algorithms and code.  Rather than having to look through an entire night's
   data it will be preferable to look at a single image which shows the night's sky 
   variability in a single glance. The night summary image provides this quick synopsis
   of a night's sky conditions.
  
  The below figure will be modified and replaced soon.
  ![alt text](https://github.com/LowellObservatory/All-Sky/blob/master/asc_flowch_001.png)
   



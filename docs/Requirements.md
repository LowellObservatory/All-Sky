`This document is now superseded by the requirements documents found under /camera_ops and /presentation`

All-Sky Camera

* Scope:
    1. This project will provide software that will operate the allsky camera in a mostly autonomous manner, save the
       raw images `[and provide the overlay images which correspond in time with the sky images ???]`.
    2. Replace the existing software with something new that is well documented and tested and done through the full software development protocol.
    3. This project does not include any type of image display or user accessibility. However, as with good software deployment, the code must be modularized to accommodate the inclusion of those items deemed outside of the current scope of this project. 

* Purpose:
  - See what the weather is doing.
  - Where is the telescope pointing?  This impacts observing. `Outside of scope?`
  - User community: Control room, off-site, visitor center, public access for Bob Ayers.  `Outside of scope?`
  - Need policy decision about whether public images show DCT pointing position. 
      There seems to be a political problem with this.  Tentative answer is not to show DCT pointing.  `Outside of scope?`
  - To provide allsky camera data for purposes determined by the project sponsor.

* Functional Requirements:
 * Essential:
    1. Takes images reliably at configurable cadence.  The FITS files are stored.
    2. Image display required.  `Outside of scope?`
    3. Movie animation display required. `Outside of scope?`
    4. Run all night without breaking or losing images on the longest night.
    5. Calibration of images will be done off-line.
  * Requirements for observers and TOs:  
    1. Where is the DCT pointing? `Outside of scope?`
    2. Equatorial and alt-az grids, and compass points (NSEW) `Outside of scope?`
    3. Star names `Outside of scope?`
  * Interaction or configuration: System
    1. Cadence (within limits)  `Outside of scope?`
    2. Upper limit to exposure time 
    3. Lower limit to exposure time (likely to be system dependent)
    4. Number of frames in the movie.  `Outside of scope?`
  * Interaction or configuration: User
    1. Overlay selections (applies to still images and [movies ?])  `Outside of scope?`
    2. Inverted image  `Outside of scope?`
    3. [Make a movie of 10 frames.  The user gets to select whether the movie is
        made of every image, 10 in a row, every other image, every third one, etc.] `Outside of scope?`
  
* Technical Requirements:
  1. Make the camera interface software module so it can be replaced.
  2. Need a start/stop approach for TOs to re-start the system.  `Outside of scope?`
  3. Image display with selected overlays is via xxx (GUI? web page?)  `Outside of scope?`
    Public image display is without overlays. `Outside of scope?`
  4. Interaction/configuration mechanism  `Outside of scope?`
    a) Config file controlled by TO only, by some TBD means.  `Outside of scope`
    b) A browser-side configuration that can be done independently.  `Outside of scope`
  5. Control the dew heater. Control the camera's built-in dew heater with a PDU
     based on the current humidity measurement.
  6. Control of the camera will be done using availabe INDI drivers. The camera control
     portion of the software will be designed such that if and when the camera is replaced
     with a different manufacturer's camera very little will have to be changed with regard
     to the camera control module.  `[ Proven to be feasible ]`
  7. The overlay grids to be provided are,  `Outside of scope?`
     a) Equatorial grid
     b) Alt/Az grid
     c) Star labels
     d) Moon and planets
     e) Current telescope position.
     f) Of the overlay grids to be provided only 1, item e) Telescope Position, must be 
        calculated in real time. Item d) Moon and Planets should probably also be calculated
        in real time but they could be saved during the day before the observing night.
    
* Admin-User Requirement:  `Outside of scope?`
  1. Provide the tools needed to realign the overlay image(s) to the allsky image after
     the camera has been moved and the orientation of the sky has changed.
  2. One possible solution will be to produce an image where bright stars
      can be selected via the mouse to very good accuracy. These pixel coordinates are
      converted to sky coordinates and offsets are applied to the overlays so that they
      align well with the sky image. 
  3. The process of realigning the images when the sky orientation has changed must be
     something anyone can do with adequate instruction.
            
* Possible extensions
  - Extinction map.   `Outside of scope?`
  
Questions
1. Is it possible to have the user control overlays at the browser end?  Is this even
   desirable?  This is a research project.  Dyer will research this. `Outside of scope?`
   



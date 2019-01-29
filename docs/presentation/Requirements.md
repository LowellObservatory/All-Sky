All-Sky Camera Presention 

* Scope:
  1. Replace the existing software with something new that is well documented and tested and done through the full software development protocol.

* Purpose:
  - See what the weather is doing.
  - Where is the telescope pointing?  This impacts observing.
  - User community: Control room, off-site, visitor center, public access for Bob Ayers. 
  - Need policy decision about whether public images show DCT pointing position. 
      There seems to be a political problem with this.  Tentative answer is not to show DCT pointing. 
  - To provide allsky camera data for purposes determined by the project sponsor.


* Functional Requirements:
 * Essential:
    1. Image display required. 
    2. Movie animation display required.
    3. Run all night without breaking or losing images on the longest night.
  * Requirements for observers and TOs:  
    1. Where is the DCT pointing? 
    2. Equatorial and alt-az grids, and compass points (NSEW)
    3. Star name labels
  * Interaction or configuration: System
    1. Cadence (within limits) 
    2. Upper limit to exposure time 
    3. Lower limit to exposure time (likely to be system dependent)
    4. Number of frames in the movie. 
  * Interaction or configuration: User
    1. Overlay selections (applies to still images and movies)
    2. Inverted image 
    3. Make a movie of 10 frames.  The user gets to select whether the movie is
        made of every image, 10 in a row, every other image, every third one, etc.
        
* Technical Requirments:
  1. Need a start/stop approach for TOs to re-start the system.
  2. Image display with selected overlays is via xxx (GUI? web page?)
    Public image display is without overlays. (Without ALL overlays? Why not include star labels and grid?)
  3. Interaction/configuration mechanism 
    a) Config file controlled by TO only, by some TBD means. 
    b) A browser-side configuration that can be done independently. 
  4. The overlay grids to be provided are, 
     a) Equatorial grid
     b) Alt/Az grid
     c) Star labels
     d) Moon and planets
     e) Current telescope position.
     f) Of the overlay grids to be provided only 1, item e) Telescope Position, must be 
        calculated in real time. Item d) Moon and Planets should probably also be calculated
        in real time but they could be saved during the day before the observing night.        
  5. Provide the tools needed to realign the overlay image(s) to the allsky image after
     the camera has been moved and the orientation of the sky has changed.
  6. One possible solution will be to produce an image where bright stars
      can be selected via the mouse to very good accuracy. These pixel coordinates are
      converted to sky coordinates and offsets are applied to the overlays so that they
      align well with the sky image. 
  7. The process of realigning the images when the sky orientation has changed must be
     something anyone can do with adequate instruction.
     
     

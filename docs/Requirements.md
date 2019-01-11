All-sky camera

Replace the existing software with something new that is well documented and tested and done through the full software development protocol.

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

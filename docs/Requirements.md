All-sky camera

Replace the existing software with something new that is well documented and tested and done through the full software development protocol.

* Purpose:
  See what the weather is doing.
  
  Where is the telescope pointing?  This impacts observing.
  
  User community: Control room, off-site, visitor center, public access for Bob Ayers.
  
    Need policy decision about whether public images show DCT pointing position.
      There seems to be a political problem with this.

* Requirements:
Functional
 Essential:
  Takes images reliably at configurable cadence.  The FITS files are stored.
  Image display required.
  Movie animation display required.
  Run all night without breaking or losing images on the longest night.
  [Calibration done off-line]
 Requirements for observers and TOs:  
  1. Where is the DCT pointing?
  2. Equatorial and alt-az grids, and compass points (NSEW)
  3. Star names
 Interaction or configuration
   System
      Cadence (within limits)
      Upper limit to exposure time 
      Lower limit to exposure time (likely to be system dependent)
      Number of frames in the movie
   User
      Overlay selections (applies to still images and movies)
      Inverted image
      Make a movie of 10 frames.  The user gets to select whether the movie is
        made of every image, 10 in a row, every other image, every third one, etc.
  
Technical
  Make the camera interface software module so it can be replaced.
  Need a start/stop approach for TOs to re-start the system.
  Image display with selected overlays is via xxx (GUI? web page?)
    Public image display is without overlays.
  Interaction/configuration mechanism
    a) Config file controlled by TO only, by some TBD means.
    b) A browser-side configuration that can be done independently.

Possible extensions
  Extinction map.
  
Questions
1. Is it possible to have the user control overlays at the browser end?  Is this even
   desirable?  This is a research project.  Dyer will research this.

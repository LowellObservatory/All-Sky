Update 12 March 2019
The files that were referenced below have been replaced with prototype code that is more focused on the purposes intended for this project.

===============================================================================================================================

The current state of the prototype code as of 19 February 2019.

This program requires the installation of the pyindi-client available for Linux at https://pypi.org/project/pyindi-client/.
pyindi-client installs a shared object file from the INDI C++ code base. I have been unable to locate a macOS version of pyindi-client which would install a .dynlib file instead of the .so file. 

All files should be installed in a directory called "indidev" under your home directory.
This must include the file "exp.cfg" within the indidev/ directory. Edit the exp.cfg file to include only a single line "0.14" with no quotes. This will set an exposure time that will be useful in a well lit room.\
Next, run check4server.py to start the INDI server with the proper driver and appropriate arguments.\
Next, edit front_end.py to include cs.acquire(rangeof=1) on the very last line. This will take a single picture of the desired exposure length.\
Run front_end.py which will save a fits file to a data date utc directory of the current utc day. For example, if the data date directory does not already exist, it will be created as the file /home/username/20190220/20190220_0001.fits

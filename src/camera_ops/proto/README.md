The current state of the prototype code as of 19 February 2019.

This program requires the installation of the pyindi-client available for Linux at https://pypi.org/project/pyindi-client/.
pyindi-client installs a shared object file from the INDI C++ code base. I have been unable to locate a macOS version of pyindi-client which would install a .dynlib file instead of the .so file. 

All files should be installed in a directory called "indidev" under your home directory.
This must include the file "exp.cfg" within the indidev/ directory. Edit the exp.cfg file to include only a single line "0.14" with no quotes. This will set an exposure time that will be useful in a well lit room.
First, run check4server.py to start the INDI server with the proper driver and appropriate arguments.
Next, edit front_end.py to include cs.acquire(rangeof=1) on the very last line. This will take a single picture of the desired exposure length.

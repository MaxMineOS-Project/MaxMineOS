# MaxMineOS
MaxMineOS! Written on Python!
# About
This OS is written on Python and works on Windows, and there is an experimental version for Linux.
# Install HOWTO
This time, you can install system by running `setup.exe`

When your system is installed, just run `run.ps1` or `run.bat` to start the system

# Package Running HOWTO
You can install and run any package by running command `pkg install <package>`

When the package installed, run it: `<package> <args>`

# Important
System is downloading from server.
This means you cannot access previos versions of system. 

e.g. If latest release is 4, you cannot download release 3

# Important for Linux users
if you catch this error:
ModuleNotFoundError: No module named 'pendulum'
and before it: /bin/sh: 1: pip: not found
or some like this, try to install pip:
Ubuntu and Ubuntu-like: sudo apt install python3-pip
RedHat and RedHat-like: sudo yum install python3-pip
Then try again!

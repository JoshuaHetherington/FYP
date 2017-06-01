Installing
	These instructions are for the Fedora 24 OS I have installed on my Oracle VM VirtualBox. Terminal commands are in quotes.

Basics
	Make sure you have Python 3 installed and also for installing dependencies I have used pip3.
        Run "sudo dnf install python3-pip" 
        Also make sure you install git: "sudo dnf install git"

Python dependencies
        "pip3 install numpy" (used for random number generating)

Install Pygame
        Pygame dependencies
        "sudo dnf install mercurial libfreetype6-dev libsdl-dev libsdl-image1.2-dev libsdl-ttf2.0-dev libsmpeg-dev libportmidi-dev 
        libavformat-dev libsdl-mixer1.2-dev libswscale-dev libjpeg-dev"

        Then install Pygame itself
        "pip3 install hg+http://bitbucket.org/pygame/pygame"
        
        See website if encountering any issue. https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation
        Any issues I had were down to missing libraries, please ensure you have everything installed.

Install Pymunk
        We want version 4, this is written for Python 2 so we need to adjust a couple of things.
        
        Navigate back to your home or downloads directory
        "wget https://github.com/viblo/pymunk/archive/pymunk-4.0.0.tar.gz"

        Unpack it
        "tar zxvf pymunk-4.0.0.tar.gz"

        Update pymunk to use python 3, first navigate to the pymunk directory
        "cd pymunk-pymunk-4.0.0/pymunk"

        Then run
        "2to3 -w *.py"

        Next we need to install it
        "cd .. python3 setup.py install"

        See website if encountering any issues. http://www.pymunk.org/en/latest/

Running
        If everything installed correctly then navigate to the folder with my FYP files and run
        "python3 joshTest.py"

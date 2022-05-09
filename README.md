# HDTS
Hard Drive Tracking System


Platform/Installation Instructions for Windows Machine
    Github Repository: https://github.com/KevinAofia/HDTS.git

    1. Setting up Django
        - You have to get the latest version of Django. Go to https://www.djangoproject.com/ to download the lastest version
        - Once you go into the django website, click on "Download latest release #.#.#"

    2. Downloading and setting up python 
        - Go to https://www.python.org/downloads/ and download the latest python
        - Once you are setting it up, make sure to click on a selection of adding python as a PATH variable
            - If you accidentally missed this, you can just go to your environmental variables and add python as a PATH variable
        - Once you download and set python as a PATH variable, you will need to restart your PC/laptop so that the changes are saved and can be used throughout your PC

    3. Open up a Windows terminal and type the following:
        pip install django
        (If you get an error saying that pip doesnt exist, you probably did not add python as a PATH variable correctly)

    4. Download VisualStudio Code or any Software that allows you to use Django and mysqli
        - If you want to use Visual Studio Code, you can use this link https://code.visualstudio.com/download
        - Add python as an extension
        - Add django as an extension
        - You might need to restart your pc for this to make changes in the system

    5. Code:
        - Create a folder in your PC/laptop, this folder will contain all the contents downloaded from the github repository
        - Open up Visual Studio Code and open the folder you want the project to be in
        - Open up a terminal and type the following:
            git clone https://github.com/KevinAofia/HDTS.git
            git remote add origin https://github.com/KevinAofia/HDTS.git
        - The previous step will allow you to clone the project and allow you to make any changes to it

    6. How to run the code:
        - Open up a terminal and cd into wherever you find the manage.py file
        - If you type "dir" and you see manage.py as one of the files within the directory you're in, you are in the right place!
        - Type the following in the same terminal:
            python manage.py migrate
            python manage.py runserver

        - If it ran correctly, no errors should be displayed. However, if you got an error, you might have not installed python/django correctly on your visual studio code
        - A URL will be ouputted after running python manage.py runserver, if so, you can either enter the URL it gave you on a browser server or can control left click on it so it opens up in a browser. 
        - After clicking on the url, the url should open up the project on your localhost
#--------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------------------------------------------------------#
Platform/Installation Instructions for Mac Machine
    Github Repository: https://github.com/KevinAofia/HDTS.git

    2. Downloading and setting up python 
        - Go to brew.sh and download it
        - Open up a terminal and type the following:
            brew install python3
        - To check if you have correctly set up python type the following:
            python3
            - If no errors were displayed, you are good to go. If you see any errors, you probably didn't install python right
        - To check if you have correctly set up python type the following:
            pip
            If no errors were displayed, you are good to go. If you see any errors, you probably didn't install python right

    1. Setting up Django
        - After setting up python open up a terminal and type:
            pip install django
        - If after installing it, it says that pip might need an upgrade, type the following:
            pip install --upgrade pip
    
    4. Download VisualStudio Code or any Software that allows you to use Django and mysqli
        - If you want to use Visual Studio Code, you can use this link https://code.visualstudio.com/download
        - Add python as an extension
        - Add django as an extension
        - You might need to restart your pc for this to make changes in the system

    5. Code:
        - Create a folder in your PC/laptop, this folder will contain all the contents downloaded from the github repository
        - Open up Visual Studio Code and open the folder you want the project to be in
        - Open up a terminal and type the following:
            git init
            git remote add origin https://github.com/KevinAofia/HDTS.git
            git clone https://github.com/KevinAofia/HDTS.git
            
        - The previous step will allow you to clone the project and allow you to make any changes to it

    6. How to run the code:
        - Open up a terminal and cd into wherever you find the manage.py file
        - If you type "dir" and you see manage.py as one of the files within the directory you're in, you are in the right place!
        - Type the following in the same terminal:
            python manage.py migrate
            python manage.py runserver

        - If it ran correctly, no errors should be displayed. However, if you got an error, you might have not installed python/django correctly on your visual studio code
        - A URL will be ouputted after running python manage.py runserver, if so, you can either enter the URL it gave you on a browser server or can control left click on it so it opens up in a browser. 
        - After clicking on the url, the url should open up the project on your localhost


Resources:
    If you are having a hard time installing django/python/project on your local machine, you can use this video as reference 
        - https://www.youtube.com/watch?v=2FvIa4BADvA&t=329s&ab_channel=ProgrammingKnowledge2
    
    - https://www.youtube.com/watch?v=e_o1nacGQiw&ab_channel=MLittleProgramming
    - https://code.visualstudio.com/docs/python/tutorial-django
Code Structure:
    Code is structured according to the default Django setup. Below are definitions for the most important files and folders in the program.

    admin.py: 
        - File where all models (objects) are registered to be used by the site
        - Each model is registered using a function in rapid succession

    urls.py:
        - File where all front end sites are given WWW urls, a view, and a name for the rest of the program to work with
        - Each url is defined by a function and entered as an element of an array called urlpatterns

    views.py:
        - File where all front end sites can give and take (POST and GET) information to and from the program
        - Each view is represented as a function to be run any time the front end site needs to be presented
     
    models.py:
        - File where the configuration models are initialized
    
    Some files are crated automatically and are empty due to this.

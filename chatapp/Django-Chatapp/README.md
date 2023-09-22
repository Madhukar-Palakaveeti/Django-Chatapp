# Django-Chatapp
 A fully decoupled django backend for a real-time chatting application.

# Introduction
A standalone backend for a real-time one-on-one chat application containing apis for User Authentication and websocket connections.

# Instructions
- To run the application locally, clone this repository to the
   local machine.
- Then create a virtual environment with venv or anaconda.
- Now make sure to install all the dependencies by running:
    ```bash
        $ pip install -r requirements.txt
    ```
    
- After that run the migrations.
    ```bash
       $ python manage.py makemigrate
       $ python manage.py migrate
    ```
- Now run the server.
    ```bash
        $ python manage.py runserver
    ```
    
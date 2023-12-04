# chatbot
Base for python chatbot. Uses callback API.
Quick rundown of files:

### flask_catcher
This is your web-app that takes requests from VK server.

### main_app
This is a sync file between web and all other modules. Takes data from flask and sends it into main class

### panopticon
This is a sync class between all the parts of application. Stores chats and other classes

### listener
This is a class that handles data, makes sure that it can be handled correctly and sends it into logger

### logger
Main class for chatbot. It handles all the messages and commands and stores all the logic 

### chat
Stores chat and methods for interacting with it. 

### user
Stores users, if needed. 

### misc
Just some misc functions.

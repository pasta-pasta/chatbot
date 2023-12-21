# chatbot
Base for python chatbot. Uses callback API.
Quick rundown of files:

### web_catcher
This is your web-app that takes requests from VK server and sends them to handling.

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

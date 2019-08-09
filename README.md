# Sovereignty
Attempt at a C2 using flask for control and python bots

# Server
Uses flask to host a web page with fields for IP of the bot to execute on
as well as the command to execute. Prints what was entered in each field. 
When bots check in, if they are not in the list of active bots, they will 
be added to it

# Bot

Sends a GET with its IP to recieve list of commands to run and executes them. Sends back 
list of successful commands. 

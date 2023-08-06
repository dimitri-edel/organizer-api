# organizer_api
## URL routes of the API
### Authentication
Registration **dj-rest-auth/registration/**
Login **dj-rest-auth/login/**
Logout **dj-rest-auth/logout/**
### Team app
Team list **team/**
TeamList allows user to view teams, or create their own teams
Teams can only be created by authenticated users by sending a **POST-request** to this url
To create a **new team** you need to send a **POST-request** to this url
Team details **team/<int:pk>/**
Providing an integer as the **argument** will return a **JSON-object** containing the requested team
if you send a **GET-request** to this url
You need to send a **PUT-request** to update a team
To **delete a team** you need to send a **DELETE-request** to this url
List of team mates **teammates/** 
List of team memberships **membership/**
The list will only contain teams that the are not owned by the current user
A certain membership **'membership/<int:pk>**
List of tasks **task/**
TeamList allows user to view tasks, or create their own tasks
Tasks can only be created by authenticated users by sending a **POST-request** to this url
Individual task **task/<int:pk>**
Providing an integer as the **argument** will return a **JSON-object** containing the requested task
if you send a **GET-request** to this url
You need to send a **PUT-request** to update a task
To **delete a task** you need to send a **DELETE-request** to this url
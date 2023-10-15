# ORGANIZER API

The API allows a front end application to store and access data for a basic organizer.
## FEATURES
---
## Authentication
Users can register with the API. Upon registration they can sign in or out, using their credentials.
[See URL Requests for Authentication](#authentication)

---

### Forming Teams
Authenticated users can create Teams. A Team entity contains the id of the user whoe created it and the name of the team. The user who created the team can also rename it or delete it. [See URL Requests for Forming Teams](#forming-teams)
Authenticated users can [view a list of teams](#list-of-teams), [join teams](#create-memebership), [leave teams](#quit-membership).

---

### Task Management
Authenticated users can [list](#list-of-tasks), [create](#create-task), [edit](#update-task-by-id), 
[retrieve](#retrieve-task-by-id) and [delete](#delete-task-by-id) Tasks.

Also, the users can assign tasks to their teammates. In order to assign a task to a teammate, you will need to specify
their user-ID in your request, when creating or editing a task. Follow [this link](#list-of-teammates) to see how to
retrieve a list of teammates with their IDs.

---

### PEP8 and Pylint
For linting the code I used pylint to validate the code. Thus, it is mandatory that Pylint be used to validate the code on another machine, because it was necessary to apply a few instructions for that tool in the code. For instance, it does not recognize dynamically attached properties and will throw an error, even if the property is valid.

---

## MODEL
Here is a sketch of how the model types are related to each other.

![Model](images/organizer_model.jpg)

---

## URL ROUTES FOR REQUESTS

All of the following URLs must be appended to the **ROOT URL** of the API.
**ROOT URL** [deployedURL]

### Authentication

#### REGISTRATION
---
Request Method: **POST**

Content-Type: **application/json** or **multipart/form-data***

URL: **/dj-rest-auth/registration/**

Body:
<code>
{
    "username" : "desired username",
    "password1" : "password",
    "password2" : "password"
}
</code>

Required fields:
- **username** the username under which the user will be registered
- **password1** password
- **password2** password

---

##### Response if SUCCESSFUL
Status Code: 201 Created

Content-Type: **application/json**

Body: 
<code>
"access_token":"token_value", "refresh_token":"token_value", 
"user":{ 
    "pk", "integer", "username":"some name", "email", "some email", "first_name", "john", "last_name": "doe"
}
</code>

---

##### ERROR User already exists
Status Code: 400 Bad Request

Content-Type: **application/json**

Body: 
<code>
{
    "username": [
        "A user with that username already exists."
    ]
}
</code>

---
##### ERROR Password validation errors
Status Code: 400 Bad Request

Content-Type: **application/json**

Body: 
<code>
{
    "password1": [
        "This password is too short. It must contain at least 8 characters.",
        "This password is too common.",
        "This password is entirely numeric."
    ]
}
</code>

If password1 and password2 don't match the Body will look like this:
<code>
{
    "non_field_errors": [
        "The two password fields didn't match."
    ]
}
</code>

---

#### LOGIN
---
Request Method: **POST**

Content-Type: **application/json** or **multipart/form-data***

URL **/dj-rest-auth/login/**

Body: 
<code>
{
    "username": "someusername",
    "password": "somepassword"
}
</code>


---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: **application/json**

Body: 
<code>
"access_token":"token_value", "refresh_token":"token_value", 
"user":{ 
    "pk", "integer", "username":"some name", "email", "some email", "first_name", "john", "last_name": "doe"
}

</code>

---
##### Respoonse if no password was provided
Status Code: 400 Bad Request

Content-Type: **application/json**

Body: 
<code>
{
    "password": [
        "This field may not be blank."
    ]
}
</code>

---
##### Respoonse if the username and password do not exist
Status Code: 400 Bad Request

Content-Type: **application/json**

Body: 
<code>
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
</code>

---
#### LOGOUT
Request Method: **POST**

URL : **/dj-rest-auth/logout/**

**No Payload required**

---

#### USER AND ACCESS TOKENS
**Request user data for for an authenticated user**

Request Method: **GET**

URL:  **/dj-rest-auth/user/**

**No Payload required**

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: **application/json**

Body: 
<code>
{
    "pk": 11,
    "username": "tester4",
    "email": "",
    "first_name": "",
    "last_name": ""
}
</code>

**Access tokens** will also be attached to the response in **cookies**.

---
##### Response if NOT LOGGED IN
Status Code: 401 Unauthorized

Content-Type: **application/json**

Body: 
<code>
{
    "detail": "Authentication credentials were not provided."
}
</code>

---
#### REFRESH ACCESS TOKENS
Request Method: **POST**

URL: **/dj-rest-auth/token/refresh/**

**No Payload required, except for the cookies in the request**

---
##### Response if NOT LOGGED IN
Status Code: 401 Unauthorized

Content-Type: **application/json**

Body: 
<code>
{
    "detail": "No valid refresh token found.",
    "code": "token_not_valid"
}
</code>

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: **application/json**

Body: 
<code>
{
    "access": "a-long-string-of-jibber-jabber",
    "access_token_expiration": "2023-08-26T11:05:05.727454Z"
}
</code>

**Access tokens** will be attached to the **Cookies** in the Response as well.

---
### Team app

**The following URLs will only work for authenticated users!**
---
#### LIST OF TEAMS
Request Method: **GET**

URL: **/team/**

##### PARAMETERS
- **search** filters the list by username and name of the team. For example: "/team/?search=dj" will give you a list of all teams whose name begin with dj or whose owners username begins with dj
- **ordering** orders the list by  name. For example "team/?search=dj&ordering=name will give you a list of teams whose owners username begins with dj or whose name begins with dj. The list will be ordered by username in ascending order. If you want the filter to order in descending order just add a **-** at the front like so: ordering=-name.
- **name** or **owner__username** will filter the results by either name of team or username of its owner
- **offset** and **limit** are used for pagination. By default the pagination is set to offset=0 and limit=3. Which means that each page will have three items. But if you want to up the number of items you can just set limit=[a number]. For instance, if I want to have 5 items per page and want to begin with the third entry: &offset=2&limit=5

---
##### Response
Status Code: 200 OK

Conent-Type: application/json

Body:
<code>
{
    "count": 8,
    "next": "http://127.0.0.1:8000/team/?limit=3&offset=3",
    "previous": null,
    "results": [
        {
            "id": 2,
            "owner": "dj_admin",
            "name": "Administration changed",
            "is_member": false
        },
        {
            "id": 6,
            "owner": "dj_test",
            "name": "Chill Team",
            "is_member": false
        }
        ...
    ]
}
</code>

The data is **paginated**. Thus,**count** is the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each team
- **id** is the id of the team
- **owner** is the username of the one who owns the team
- **name** is the name of the team
- **is_member** is a boolean that signigies whether or not user requesting the information is member of that team

---
#### CREATE NEW TEAM
Request Method **POST**

Content-Type: **application/json** or **multipart/form-data**

URL: **/team/**

Body: **{ "name":"name of team" }**

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Conent-Type: application/json

Body:
<code>
{
    "count": 8,
    "next": "http://127.0.0.1:8000/team/?limit=3&offset=3",
    "previous": null,
    "results": [
        {
            "id": 2,
            "owner": "dj_admin",
            "name": "Administration changed",
            "is_member": false
        },
        {
            "id": 6,
            "owner": "dj_test",
            "name": "Chill Team",
            "is_member": false
        }
        ...
    ]
}
</code>

---
##### Response if NAME FIELD IS EMPTY
Status Code: 400 Bad Request

Conent-Type: application/json

Body:
<code>
{
    "name": [
        "This field may not be blank."
    ]
}
</code>

---
#### RETRIEVE TEAM
Request Method: **GET**

URL: **/team/<int:pk>/**, where the private key(ID) of the team msut be specified in the path

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: application/json
Body:
<code>
{
    "id": 7,
    "owner": "dj_admin",
    "name": "New team",
    "is_member": false
}
</code>

Fields: 
- **id** is the private key of the team
- **owner** is the username of the one who created the team
- **name** is the name of the team,
- **is_member** is a boolean value that specified if the user in the request is a member of that team

---
###### Response if NOT FOUND
Status Code: 404 Not Found

Content-Type: application/json

Body:
<code>
{
    "detail": "Not found."
}
</code>

---
#### UPDATE TEAM
Request Method: **PUT**

URL:  **/team/<int:pk>/** pk is the private key of the team, which is an integer value

Content-Type: **application/json** or **multipart/form-data**

Body:  **{ "name": "new value" }**

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: **application/json**

Body: 
<code>
{
    "id": 7,
    "owner": "your username",
    "name": "XXX Team",
    "is_member": false
}
</code>

Fields: 
- **id** is the private key of the team
- **owner** is the username of the one who created the team
- **name** is the name of the team,
- **is_member** is a boolean value that specified if the user in the request is a member of that team

---
##### Response if NAME FIELD IS EMPTY
Status Code: 400 Bad Request

Content-Type: **application/json**

Body: 
<code>
{
    "name": [
        "This field may not be blank."
    ]
}
</code>

---
#### DELETE TEAM
Request Method: **DELETE**

URL:  **/team/<int:pk>/** pk is the private key of the team, which is an integer value

**No Payload required**

---
##### Response if SUCCESSFUL
Status Code: 204 No Conent

---
###### Response if NOT FOOUND
Status Code: 404 Not Found

Content-Type: application/json

Body:
<code>
{
    "detail": "Not found."
}
</code>

---
#### LIST OF TEAMMATES
Request Method: **GET**

URL: **/teammates/** 

**No Payload required**

##### Response if SUCCESSFUL
Status Code : 200 OK

Contenxt-Type: application/json

Body:
<code>
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "team_name": "DJ Team",
            "team": 1,
            "user_id": 3,
            "member": "dj_test"
        },
        {
            "id": 6,
            "team_name": "DJ Team",
            "team": 1,
            "user_id": 4,
            "member": "tester1"
        }
    ]
}
</code>


The data is paginated. Thus, **count** is the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each teammate:
- **id** is the id of the team
- **team_name** is the name of the team
- **user_id** is the id of the user that is a member of the team
- **member** is the username of the teammate

---
#### LIST OF TEAM MEMBERSHIPS
**NOTE! The list will only contain teams that the are not owned by the user in the request!**

Request Method: **GET**

URL: **/membership/**

**No Payload required**

---
##### Responose if SUCCESSFUL
Status Code: 200 OK

Content-Type: application/json

Body:
<code>
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 14,
            "team_name": "Testing",
            "team": 4,
            "user_id": 1,
            "member": "dj_admin"
        },
        {
            "id": 13,
            "team_name": "Extensive testing",
            "team": 12,
            "user_id": 1,
            "member": "dj_admin"
        }
    ]
}
</code>

The data is paginated. Thus  **count** is the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each membership:
- **id** is the membership id
- **team_name** is the name of the team that the membership is of
- **user_id** is the own user.id
- **member** is your username

---
#### CREATE MEMEBERSHIP
Response Method: **POST**

Content-Type: **application/json** or **multipart/form-data**

URL: **/membership/**

Body:
<code>
{
    "team": 12    
}    
</code>

Fields:
- **team** is the private key (ID) of the team that the user wants to join

---
##### Response if SUCCESSFUL
Status Code: 201 Created

Content-Type: application/json

Body:
<code>
{
    "id": 15,
    "team_name": "Extensive testing",
    "team": 12,
    "user_id": 1,
    "member": "dj_admin"
}
</code>

Fields:
- **id** is the membership id
- **team_name** is the name of the team that the membership is of
- **user_id** is the own user.id
- **member** is your username

---
#### QUIT MEMBERSHIP
Request Method: **DELETE**

URL: **/leave/team/<int:team_id>**

**No Payload required**

---
##### Response if SUCCESSFUL
Status Code: 204 No Content

---
##### Response if NOT ALLOWED or NOT FOUND
Status Code: 404 Not Found

Conent-Type: application/json

Body:
<code>
{
    "detail": "Not found."
}
</code>

---

#### LIST OF TASKS
Request Method: **GET**

URL:  **/tasks/**

**No Payload required**

##### PARAMETERS
- **search** allows you to search for items by title, username of owner or due_date. For example, /tasks/?search=2023-09 will give you all tasks that are due in September 2023. /tasks/?search=tester will give a list that contains tasks whose title begins with tester or whose owners username begins with tester. However, it will only list either your own tasks or tasks that have been assigned to you by other users.
- **ordering** allows you to order the results by due_date, priority or status. For example: /tasks/?ordering=priority will give you a list that is ordered by priority in ascending order. To order it in descending order add a **-** after **=**, like so &ordering=-priority.
- **owner, due_date, category, priority, status** any one of these parameters can be used to filter the results. For instance, /tasks/?owner=tester?category=0 will give you all Chores of the user tester, provided that the user has assigend any tasks to you.

**NOTE! due_date is a datetime object so it expects a specific time. It is useless when it comes to filtering out tasks that belong to a specific day. For that purpose it is better to use the search filter as shown in the example above.**

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: application/json

Body:
<code>
{
    "count": 35,
    "next": "https://organizer-api-f1f640e8d82c.herokuapp.com/tasks/?limit=3&offset=3",
    "previous": null,
    "results": [
        {
            "id": 20,
            "owner": "dj_admin",
            "is_owner": true,
            "asigned_to": null,
            "title": "ADASFAD",
            "comment": "rzuzr4uz6r4uru",
            "due_date": "15 Sep 2023 15:41",
            "category": 0,
            "priority": 2,
            "status": 0,
            "file": null
        },
        {
            "id": 31,
            "owner": "dj_admin",
            "is_owner": true,
            "asigned_to": null,
            "title": "third thing",
            "comment": "coment coment coment coment coment coment coment coment coment coment coment coment coment coment coment coment coment coment",
            "due_date": "01 Sep 2023 20:57",
            "category": 0,
            "priority": 0,
            "status": 0,
            "file": null
        },
        {
            "id": 25,
            "owner": "dj_admin",
            "is_owner": true,
            "asigned_to": null,
            "title": "some other task for septemper",
            "comment": "comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...",
            "due_date": "01 Sep 2023 17:07",
            "category": 0,
            "priority": 1,
            "status": 0,
            "file": null
        }
    ]
}
</code>

The **data** field is paginated. Thus, **count** is the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.

The array holds a set of dictionaries with the following attributes for each Task:
- **id** is the id of the Task
- **owner** is the username of the one who ones the task
- **is_owner** is a boolean that signifies if the user in the request is the owner of the Task
- **asigned_to** is the id of the user who the task is assigned to, if the task is not assigned the value is **null**
- **asigned_to_username** the username of the user who the task was assigned to, otherwise **null**
- **title** The name of the Task
- **comment** Comment for the task or **null**
- **due_date** The due date and time in the following format: "05. Sep 2023 10:15"
- **category** A number from 0 to 2 (0- Chore, 1- Errand, 2- Work)
- **priority** A number from 0 to 2 (0- High, 1- Middle, 2- Low)
- **status** A number from 0 to 2 (0- Open, 1- Progressing, 2- Done)
- **file** URL of a image file that was attached to the task or **null**

---
#### CREATE TASK
Request Method: **POST**

Content-Type: **application/json** or **multipart/form-data**

URL:  **/tasks/**

Body:
<code>
    {
        "asigned_to": null,
        "title": "some other task for septemper",
        "comment": "comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ..comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...",
        "due_date": "2023-09-01T17:07",
        "category": 0,
        "priority": 1,
        "status": 0,
        "file": null
    }
</code>

Fields:
- **asigned_to** is the id of the user who the task is assigned to, if the task is not assigned the value is **null**
- **asigned_to** the user-id of the teammate, to whomm this task will be assigned, otherwise **null**
- **title** The name of the Task
- **comment** Comment for the task or **null**
- **due_date** The due date and time in the following **format**: "2023-09-01T10:00" Year-Month-Day T Hour-Minute
- **category** A number from 0 to 2 (0- Chore, 1- Errand, 2- Work)
- **priority** A number from 0 to 2 (0- High, 1- Middle, 2- Low)
- **status** A number from 0 to 2 (0- Open, 1- Progressing, 2- Done)
- **file** image file ("jpg", "png", "webp", "bmp") or **null**

**NOTE! Use form-data if you want to upload an image file in the request**
---

##### Response if SUCCESSFUL
Status Code: 200 OK

Context-Type: application/json

Body:
<code>
{
    "id": 57,
    "owner": "dj_admin",
    "is_owner": true,
    "asigned_to": null,
    "title": "some other task for septemper",
    "comment": "comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ..comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...comenting ...",
    "due_date": "01 Sep 2023 17:15",
    "category": 0,
    "priority": 1,
    "status": 0,
    "file": null
}
</code>

---
##### Response if VALIDATION ERRORS
**The response will return a jason file that contains the field name that failed validation and an array of possible reasons**

Status-Code: 400 Bad Request

Content-Type: application/json

Body:
<code>
{
    "due_date": [
        "Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."
    ]
}
</code>

---
#### RETRIEVE TASK BY ID
Request Method: **GET**

URL: **/task/<int:pk>** pk is the private key (ID) of the task 

**No Payload required**

---
##### Response if SUCCESSFUL
Status Code: 200 OK

Content-Type: application/json

Body:
<code>

    "id": 36,
    "owner": "dj_admin",
    "is_owner": false,
    "asigned_to": null,
    "title": "Do something",
    "comment": "bla bla la  la  la  la  la  la  la  la  la  la  la  la  la  la  la  la  la  la  la",
    "due_date": "21 Aug 2023 10:06",
    "category": 0,
    "priority": 0,
    "status": 2,
    "file": null
}
</code>

The data in the Response will have the follwing fields:
- **id** is the id of the Task
- **owner** is the username of the one who ones the task
- **is_owner** is a boolean that signifies if the user in the request is the owner of the Task
- **asigned_to** is the id of the user who the task is assigned to, if the task is not assigned the value is **null**
- **asigned_to_username** the username of the user who the task was assigned to, otherwise **null**
- **title** The name of the Task
- **comment** Comment for the task or **null**
- **due_date** The due date and time in the following format: "05. Sep 2023 10:15"
- **category** A number from 0 to 2 (0- Chore, 1- Errand, 2- Work)
- **priority** A number from 0 to 2 (0- High, 1- Middle, 2- Low)
- **status** A number from 0 to 2 (0- Open, 1- Progressing, 2- Done)
- **file** URL of a image file that was attached to the task or **null**

If the task is not found the **Response** will have the status **400** Bad Request

---
##### UPDATE TASK BY ID
Request Method: **PUT**

Content-Type: **application/json** or **multipart/form-data**

URL: **/task/<int:pk>**

Body:
<code>
{ 
    "title": "New title",
    "due_date": "2023-09-15T18:41",
    "category": 0,
    "priority": 2,
    "status": 0
}
</code>

**NOTE! Use form-data if you want to upload an image file in the request**

Fields:
The **nullable fields** must have an **empty string** if you want them to be blank.
The **required fields**, which are title, due_date, category, priority and status, must be supplied in the request. 
**See the boday of the request above**

- **asigned_to** is the id of the user who the task is assigned to, if the task is not assigned the value is **null**
- **asigned_to** the user-id of the teammate, to whom the task must be assigned, otherwise **null**
- **title** The name of the Task
- **comment** Comment for the task or **null**
- **due_date** The due date and time in the following format: "05. Sep 2023 10:15"
- **category** A number from 0 to 2 (0- Chore, 1- Errand, 2- Work)
- **priority** A number from 0 to 2 (0- High, 1- Middle, 2- Low)
- **status** A number from 0 to 2 (0- Open, 1- Progressing, 2- Done)
- **file** image file ("jpg", "png", "webp", "bmp") or **null**

If the task is not found the **Response** will have the status **400** Bad Request

---
#### DELETE TASK BY ID
Request Method: **DELETE**

URL: **/task/<int:pk>** pk is the private key (ID) of the task

**No Payload required**

---
##### Response if DELETED
Status-Code: 204 No Content
---
##### Response if NOT FOUND
Status Code: 404 Not found
---
## Tests
### Authentication
Authentication has been tested by using the Views provided by DRF.
Also, the application uses dj-rest-auth. Which is a well tested app.
But it seems that this version does have a few bugs, whose fix was
provided by Code Institute and can be found in organizer_api_prj.views.py
---
#### Registration
- I have registered several users.
- The validation works.
- The users are added as expected.
---
#### Login
- Users can sign in
- The validation works.


---
### Test Listing Tasks
As a **User** I can **retrieve a list their own tasks** so that **the front end can display them**
- [x] Tasks list only contains tasks that either belong to the user or have been assigned to the user
- [x] Task list can be ordered by due_date, title
- [x] Task can be searched by title, due_date
- [x] Task list can be filtered by due_date
- [x] Tasks are serialized in JSON format

### Test Creating Tasks
As an **authenticated user** I can **create tasks**
- [x] The current user becomes the owner of the task
- [x] Task fields are validated
- [x] The created task reflects the submitted Task

### Test Deleting Tasks
As a **authenticated user** I can **delete tasks** 
- [x] Tasks can be deleted by the owner
- [x] Task can be deleted by the assigned teammate

### Test Updating Tasks
As an **authenticated user** I can **update tasks**
- [x] The updated task reflects the submitted data 
- [x] Access granted only to the owner or a teammate, to whom the task was assigned

### Test Listing Teams
As a **authenticated user** I can **retrieve a list of teams**
- [x] All teams are listed
- [x] Teams can be filtered by username

### Test creating Teams
As a **authenticated user** I can **create teams** 
- [x] User can create a team
- [x] User creating the team is made the owner of the team
- [x] The created team reflects the submitted data
- [x] The same team cannot be created twice (team.owner + team.name) must be unique

### Test updating Teams
As an **atuhenticated user** and owner of the team I can **update teams**
- [x] The team is updated correctly
- [x] The validation works

### Test joining Teams
As a **authenticated user** I can **join other teams**
- [x] Membership entry is created correctly - your user becomes member of the targeted team
- [x] Membership allows team owners to assign a task to you as a teammate

### Test leaving Teams
As a **authenticated user** I can **leave teams**
- [x] Upon leaving a team, the team owner cannot assign tasks to the user
- [x] The membership entry is deleted

### Test Listing Tasks
As a **User** I can **retrieve a list their own tasks** so that **the front end can display them**
- [x] Tasks list only contains tasks that either belong to the user or have been assigned to the user
- [x] Task list can be ordered by due_date, title
- [x] Task can be searched by title, due_date
- [x] Task list can be filtered by due_date
- [x] Tasks are serialized in JSON format

### Test Creating Tasks
As an **authenticated user** I can **create tasks**
- [x] The current user becomes the owner of the task
- [x] Task fields are validated
- [x] The created task reflects the submitted Task

### Test Deleting Tasks
As a **authenticated user** I can **delete tasks** 
- [x] Tasks can be deleted by the owner
- [x] Task can be deleted by the assigned teammate

### Test Updating Tasks
As an **authenticated user** I can **update tasks**
- [x] The updated task reflects the submitted data 
- [x] Access granted only to the owner or a teammate, to whom the task was assigned

### Test Listing Teams
As a **authenticated user** I can **retrieve a list of teams**
- [x] All teams are listed
- [x] Teams can be filtered by username
- [x] Teams can be filtered by title(team name)

### Test creating Teams
As a **authenticated user** I can **create teams** 
- [x] User can create a team
- [x] User creating the team is made the owner of the team
- [x] The created team reflects the submitted data
- [x] The same team cannot be created twice (team.owner + team.name) must be unique

### Test updating Teams
As an **atuhenticated user** and owner of the team I can **update teams**
- [x] The team is updated correctly
- [x] The validation works

### Test joining Teams
As a **authenticated user** I can **join other teams**
- [x] Membership entry is created correctly - your user becomes member of the targeted team
- [x] Membership allows team owners to assign a task to you as a teammate

### Test leaving Teams
As a **authenticated user** I can **leave teams**
- [x] Upon leaving a team, the team owner cannot assign tasks to the user
- [x] The membership entry is deleted

---
## Deployment
To deploy this application it is required to set environment variables that it uses.

### Cloudinary account
If you register with Cloudinary, you will get a URL that can be used for storing files.

**CLOUDINARY_URL** = 'cloudinary://long-string-of-mumbo-jumbo'
This variable must be set to carry that URL

You can use any other storage system, all you need to do is override the **DEFAULT_FILE_STORAGE**
variable in settings.py. Of course you might have to add another line or two of code to settings.py
depending on what the storage system requires. For cloudinary it is for instance mandoatory that 
the cloudanry storage dictionary be added to settings.py. Here is what it looks like in my file:

<code>
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL': os.environ['CLOUDINARY_URL']
}
</code>

By default, Django stores files locally, using the MEDIA_ROOT and MEDIA_URL settings. 
In that case the whole cloudinary storage business must be removed from settings.py
and **MEDIA_ROOT** and **MEDIA_URL** specified. The former is the **absolute path** on the
machine running the script and the latter is the **URL** that must be used in the requests 
for the files.

### Database settings
The application uses a django.db.backends.postgresql_psycopg2 engine, so it does expect the DBMS to be PostgresSQL.
Here is the code-snippet from settings.py
<code>
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': os.environ['DB_NAME'],

        'USER': os.environ['DB_USER'],

        'PASSWORD': os.environ['DB_PASSWORD'],

        'HOST': os.environ['DB_HOST'],

        'PORT': os.environ['DB_PORT'],
    }
}
</code>

However, you can use any other engine. Only in that case, you will have to override this part in settings.py.
And use the settings dictated by the vondor of the engine. Which I am sure will not differ by much from the ones
that you see above.

Here is the set of varaibles used by this application:
**DB_NAME** = name of the database
**DB_USER** = name of the user that has access to the database
**DB_PASSWORD** = the password
**DB_HOST** = either the IP of the host or hostname(Domain)
**DB_PORT** = the port number

### Client origin
**CLIENT_ORIGIN** = URL at which the Front end was deployed
This setting is required by django-cors-headers, which is a Django application 
for handling the server headers required for Cross-Origin Resource Sharing (CORS).

Here is a code-snippet from settings.py:
<code>
    # Allow Request from ...
    if 'CLIENT_ORIGIN' in os.environ:
    CORS_ALLOWED_ORIGINS = [
        os.environ.get('CLIENT_ORIGIN')
    ]
</code>

### Secret key
**SECRET_KEY** = some random string of characters that will be used as a secret key for encryption

### Debugging
In order to use the views for debugging you can set 
DEV = "1"
#### To turn the debugging mode back off
Just remove the variable all together

In the deployed version, it can be switched on and off. But must be removed for comercial 
deployment.

#### ALLOWED_HOSTS
In settings.py there is an array that is called ALLOWED_HOSTS. It is necessary that the **hostname or IP** be added to that array.

---
#### Deployment on heroku
To deploy the application on heroku, the **requirements.txt** must be in the folder.
The **Procfile** must be in place and contain this code:

<code>
 release: python manage.py makemigrations && python manage.py migrate
 web: gunicorn organizer_api_prj.wsgi
</code>

The Procfile is used for initializing the application every time it is deployed.
The code above states that before deployment the comands makemigrations and then migrate must be executed.
It also tells the gunicorn server the name of the WSGI file, which is a python script file that instanciates this application in WSGI-mode.

The **variables** mentioned above translate to **ConfigVars** on heroku. Those can be found in **Settings** Tab
of the deployed app. As soon as all of those variables are set to **valid values** it can be deployed.
On heroku just go to **Deploy** Tab and click on the button that reads **'Deploy'**
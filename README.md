# organizer_api
## URL routes of the API
### Authentication
#### Request user object an access tokens
Request user object for the context **[deployedURL]/dj-rest-auth/user/**
Returns pk, username, email, first_name, last_name
The request will also store an access token, in a cookie, that expires in 5 minutes
The request will aslo store a refresh token, in a cookie,  that can be used to refresh access token
#### Request to refresh access tokens
POST Request to refresh access token **[deployedURL]/dj-rest-auth/token/refresh/**
#### Request to register a user
Post request for Registration **[deployedURL]/dj-rest-auth/registration/**
The Content Type of the POST request must be **multipart/form-data**
#### Request to login a user
POST request for Login **[deployedURL]/dj-rest-auth/login/**
The Content Type of the POST request must be **multipart/form-data**
The form must contain the following fields:
username, email, password
Returns **Token key**
#### Request to logout a user
To logout a user just send a POST request to **[deployedURL]/dj-rest-auth/logout/**

### Team app
The following URLs will only work for authenticated users.
#### Request a list of teams
Send a GET-Request to the URL **[deployedURL]/team/**
The response will contain a JSON dictionary in its data field.
The format of the JSON data will look like this:
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
The **data** field is paginated so **count** the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each team
- **id** is the id of the team
- **owner** is the username of the one who owns the team
- **name** is the name of the team
- **is_member** is a boolean that signigies whether or not user requesting the information is member of that team

#### Create new Team
Teams can only be created by authenticated users by sending a **POST-request** to  **[deployedURL]/team/**
The Content Type of the POST request must be **multipart/form-data**
The Form must contain only one field **name**

#### Retrieve a Team
Send a GET-Request to this url **[deployedURL]/team/<int:pk>/**
The Response will contain a **JSON-object** containing the requested team
in its **data** field that will have the following attributes: **id, owner, name, is_member**
and the HTTP STATUS 200 return in the Response object

If there is no such team the **data** field will have this attribute "details":"Not found"
and the HTTP STATUS 404 returned in the Response object

#### Udate a Team
You need to send a **PUT-request** to **[deployedURL]/team/<int:pk>/**
The Content Type of the POST request must be **multipart/form-data**
The Form must contain only one field **name**

If the name is blank, then the Response will have the STATUS 400 and contain
the following attribute: 
"name": [
        "This field may not be blank."
    ]

To **delete a team** you need to send a **DELETE-request** to **[deployedURL]/team/<int:pk>/**

#### Get a list of teammates
Send a GET-Request to **[deployedURL]/teammates/** 
The **data** field in the Response will have a list of teammates that looks like this:
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
The **data** field is paginated so **count** the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each teammate:
- **id** is the id of the team
- **team_name** is the name of the team
- **user_id** is the id of the user that is a member of the team
- **member** is the username of the teammate

#### Get a List of team memberships 
Send a GET-Request to **[deployedURL]/membership/**
The list will only contain teams that the are not owned by the current user
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
The **data** field is paginated so **count** the number of entries, **next** is the index of the next page,
**previous** is the index of the previous page, **results** is the actual data in form of an array.
The array holds a set of dictionaries with the following attributes for each membership:
- **id** is the membership id
- **team_name** is the name of the team that the membership is of
- **user_id** is the own user.id
- **member** is your username

#### Quit a team membership
Send a **DELETE-Request** to **[deployedURL]/leave/team/<int:team_id>**

#### Get a List of Tasks
Send a **GET-Request** to **[deployedURL]/task/**
The **data** field is paginated so **count** the number of entries, **next** is the index of the next page,
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

#### Create a Task
Send a **POST-Request** to **[deployedURL]/task/**
The Content Type of the POST request must be **multipart/form-data**
The Form must contain the following fields:
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
The Response will contain the same fields plus the **id** as the first field([see task list](#get-a-list-of-tasks))

#### Retrieve a Task by id
Send a **GET-request** to this url **[deployedURL]/task/<int:pk>**
The **data** field in the Response will have the follwing fields:
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

##### Update an existing task by id
Send a **PUT-request** to this url **[deployedURL]/task/<int:pk>**
The Content Type of the PUT request must be **multipart/form-data**
and contain these fields. The **nullable fields** must have an **empty string** if you want them to be blank
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

#### Delete an existing task by id
To **delete a task** you need to send a **DELETE-request** to this url **[deployedURL]/task/<int:pk>**
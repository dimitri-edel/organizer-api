# organizer_api

## Tests
### Authentication
Authentication has been tested by using the Views provided by DRF.
Also, the application uses dj-rest-auth. Which is a well tested app.
But it seems that this version does have a few bugs, whose fix was
provided by Code Institute and can be found in organizer_api_prj.views.py
#### Registration
- I have registered several users.
- The validation works.
- The users are added as expected.

#### Login
- Users can sign in
- The validation works.

#### Logout
- Users can log out

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


## URL routes of the API
### Authentication
#### Request a user object and access tokens
Request user object for the context **[deployedURL]/dj-rest-auth/user/**

Returns fileds **pk, username, email, first_name, last_name**

The request will also store an access token, in a cookie, that expires in 5 minutes
The request will aslo store a refresh token, in a cookie,  that can be used to refresh access token

#### Request to refresh access tokens
POST Request to refresh access token **[deployedURL]/dj-rest-auth/token/refresh/**

#### Request to register a user
Post request for Registration **[deployedURL]/dj-rest-auth/registration/**
The Content Type of the POST request must be **multipart/form-data**
Required fields in the form:
**username, password1, password2**

#### Request to login a user
POST request for Login **[deployedURL]/dj-rest-auth/login/**
The Content Type of the POST request must be **multipart/form-data**
The form must contain the following fields:
**username, password**

Returns **Token key**

#### Request to logout a user
To logout a user just send a POST request to **[deployedURL]/dj-rest-auth/logout/**

### Team app

**The following URLs will only work for authenticated users!**

#### Request a list of teams
Send a GET-Request to the URL **[deployedURL]/team/**
The response will contain a JSON dictionary in its data field.
The format of the JSON data will look like this:

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

<code>
"name": [
        "This field may not be blank."
    ]
</code>


To **delete a team** you need to send a **DELETE-request** to **[deployedURL]/team/<int:pk>/**

#### Get a list of teammates
Send a GET-Request to **[deployedURL]/teammates/** 
The **data** field in the Response will have a list of teammates that looks like this:

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

#### Deployment on heroku
To deploy the application on heroku, the requirements.txt must be in the folder.
The Procfile must be in place and contain this code:

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
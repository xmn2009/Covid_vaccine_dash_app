# Special Instructions
 
## 1. Web application URL
https://groupl-dash-app.herokuapp.com/

It might take some time for the web page to load. 

## 2. Deployment

### 2.1 Heroku account
- Install the Heroku Command Line Interface (CLI) [[link]](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)
- login with credential:

>  $ heroku login  

### 2.2 Create a new folder for the project:

> $ mkdir groupL_dash_app

> $ cd groupL_dash_app

### 2.3 Initialize the folder with git and a virtualenv

>$ git init

>$ py -m venv venv

>$ cd venv/Scripts/activate.bat

>$ pip install dash

>$ pip install plotly

>$ pip install pandas

>$ pip install DateTime

>$ pip install gunicorn

### 2.4 Initialize the folder with app.py, a .gitignore file, requirements.txt, and a Procfile for deployment:

#### 2.4.1 Put app.py into the directory

- Make sure only use the necessary packages in the requirements.txt, 
- Make sure app.py file contains “server = app.server” under “app = dash.Dash(__name_, external_stylesheets=es)”

#### 2.4.2 .gitignore file
>
> venv
> *.pyc
> .DS_Store
> .env
> .idea
> stat.ipynb

#### 2.4.3 Procfile file
>
>web: gunicorn app:server

#### 2.4.4 requirements.txt
>
>$ pip freeze > requirements.txt

### 2.5 Use git to add, (if file update, needs to push again)
>
> $ git add . # add all files to git
>
>$ git commit -m 'Inital push'
>
>$ git push heroku master # deploy code to heroku

### 2.6 Once successfully compiled, use below to run the app:
>
>$ heroku ps:scale web=1  # run the app with a 1 heroku "dyno"
>$ heroku open

### 2.7 Debug heraku
>
>$ heroku logs --tail
>
> If cvs file reading fails, another solution is [[link]](https://stackoverflow.com/questions/57204186/dash-app-deployed-on-heroku-cannot-read-csv-file)

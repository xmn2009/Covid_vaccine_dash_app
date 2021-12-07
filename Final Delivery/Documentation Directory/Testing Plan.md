# Testing Plan

## 1. Test locally

Below is the instruction for the windows system. 

1. Clone the repo:
```
$ gh repo clone github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021
```

2. Go into the directory, and create a virtual environment:

```
$ py -m venv venv
```

3. Install the packages:
```
$ pip install -r requirements.txt
```

4. Run the app:

```
$ .\venv\Scripts\python.exe .\app.py
```
Once the app is up running, open the web page at browser at: 
- http://127.0.0.1:8050/
- Ctrl + shift + c to stop


## 2. Debug with Heroku

Heroku deployment could be debugged with the following step:

go to the web application directory, then type the following command

```
$ heroku logs --tail
```


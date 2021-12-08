# 1. Summary

Using data visualization and modeling tools to analyze the public COVID-19 related health care data. Our goal is to provide real-world evidence for a major controversial topic about COVID-19 coronavirus vaccine effectiveness based on US COVID-19 related health care data.

# 2. Authors and contact information

Fall 2021, CS6440, Group L: 

- Zuodong Jiang: jzd@gatech.edu
- Xinying Jia: xjia61@gatech.edu
- Mengna Xia: mxia38@gatech.edu

# 3. Web Application URL

[**Covid-19 (Coronavirus) Vaccine Effectiveness Analysis**](https://groupl-dash-app.herokuapp.com/)

Initial load might take some time, as Heroku free account is used. 

# 4. Source Code

## 4.1 Git repo
[Georgia Tech GitHub Repo]( https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021)

## 4.2 File list

- [app.py](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/app.py) is the source code for the web application
- [stat.ipynb](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/stat.ipynb) used to calculate Pearson r and granger causality
- [requirements.txt](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/requirements.txt) for packages needed in the app.py
- All the .csv files are needed to run the app.py

## 4.3 Dataset

- “owid-covid-data (1).csv” and “covid-variants.csv”, were collected from [“Our World in Data”](https://ourworldindata.org/)
- “Rates_of_COVID-19_Cases_or_Deaths_by_Age_Group_and_Vaccination_Status.csv” was collected from [CDC](https://data.cdc.gov/Public-Health-Surveillance/Rates-of-COVID-19-Cases-or-Deaths-by-Age-Group-and/3rge-nu2a).
- “Austria.csv”, “Bulgaria.csv”, “France.csv”, “Germany.csv”, “Italy.csv”, “Netherlands.csv”, “Portugal.csv”, “Spain.csv”, “United States.csv” are datasets for Pearson R and Granger causality in time series and were generated using [stat.ipynb](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/stat.ipynb) file.

## 4.4 Directories
1 [Final Delivery Directory](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/tree/master/Final%20Delivery)

2 [Research Directory](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/tree/master/Final%20Delivery/Research%20Directory)

3 [Documentation Directory](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/tree/master/Final%20Delivery/Documentation%20Directory)

## 4.5 Documentations
1 [Final Gantt Chart](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/Final%20Gantt%20Chart.md)

2 [User Manual](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/Application%20Manual.md)

3 [Special Instructions of deployment](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/Special%20Instructions.md)

4 [Research Directory of all historical files](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/tree/master/Final%20Delivery/Research%20Directory)

5 [Desgin Documentation](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/Documentation%20Directory/Desgin%20Doc.md)
	5.1 [Mockups](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/images/mockups.png) 
	5.2 [Use Case Diagram](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/images/useCase.png)
	5.3 [Web Application Architecure](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/images/useCase.png)

6 [Testing Plan locally and remotely](https://github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021/blob/master/Final%20Delivery/Documentation%20Directory/Testing%20Plan.md)

# 5. Installation and run locally

Below is the instruction for the windows system. 

1. Clone the repo
```
$ gh repo clone github.gatech.edu/mxia38/groupL_dash_app_cs6440_Fall2021
```

2. Go into the directory, and create a virtual environment

```
$ py -m venv venv
```

3. Activate the virtual environment
```
$ .\venv\Scripts\activate.bat
```

4. Install the packages
```
$ pip install -r requirements.txt
```

5. Run the app

```
$ .\venv\Scripts\python.exe .\app.py
```
6. Once the app is up running, open the web page at browser at: 
```
http://127.0.0.1:8050/
```
7. To stop, press
``` 
Ctrl + shift + c
```
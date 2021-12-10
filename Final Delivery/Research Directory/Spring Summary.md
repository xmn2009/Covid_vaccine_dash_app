# Practicum Sprint #1


## 1	PROBLEM (TOPIC)
In this study, we will use data visualization and modeling tools to analyze the public COVID-19 related health care data. Our goal is to provide real-world evidence for several major controversial topics about COVID-19 coronavirus:  
1. Evaluation of COVID-19 vaccine effectiveness based on US COVID-19 related health care data. 2. Evaluation of COVID-19 vaccine effectiveness on different populations (race, age, gender) 3. Analysis of the impact of state-specific COVID-19 related policies on virus infection.

### 1.1	Specify if this is your own/team idea or a mentor project
This is a team idea.

### 1.2	Provide a List of Your Top 10 Topics

1.	**Our topic: COVID-19 Vaccine Effective Analysis and Visualization;**
2.	NLP tools to search COVID-19 publication from PubMed (team idea);
3.	NLP Data Pipeline with unstructured clinical data (Jaewoo Park)
4.	FHIR IG testing with Inferno Framework (John Bender, Reece Adamson)
5.	Combating Nutritional Deficiencies (Tia Pope)
6.	Interactive FHIR Lessons (Elizabeth Shivers)
7.	FHIR IG Analytics (John Bender, Reece Adamson)
8.	COVID-19 Remote Vital Signs Monitoring (Raj Vansia)
9.	Medication Reminder App (Pillbox) (Ross Raiff)
10.	ALMA (Tia Pope)

## 2	AREA OF FOCUS
 We will be focusing on the Special Topics of Covid-19.
## 3	BACKGROUND AND SIGNIFICANCE
“COVID-19 is an infectious disease caused by SARS-CoV-2” (Coronavirus) . The syndrome caused by the disease varies, some develop into severe acute respiratory syndrome which needs intensive unit care or cause death; some only have mild symptoms such as a fever, cough, loss of smell and taste…, while some do not even develop any noticeable symptoms (COVID-19).

On March 11, 2020, WHO declares COVID-19 a pandemic. A year later, the US public started to inoculate with the COVID-19 vaccine. Starting late 2020, an accelerated distribution of vaccines has begun, with several vaccines granted emergency use authorization by the U.S. FDA (Wiersinga, 2020). So far, about 51.1% of the total pollution have received full doses of vaccinations of COVID (COVID-19) . From what we have learned as yet, the vaccines are not 100% effective at preventing infection, which means a person who is fully vaccinated might still get COVID-19. However, it seems the vaccine is helping on preventing the infected individuals from developing into serious illness or even causing death. There is still a huge population that is deeply skeptical about the safety and effectiveness of the mRNA vaccine and causing them reluctant to receive the inoculation (Robson, 2021). As the death rate of COVID-19 keeps on ramping, a lot of different voices are still questioning the effectiveness of the vaccine.

In this project, we will evaluate the effectiveness of the COVID-19 vaccine in preventing disease and death by using big data analysis and modeling tools.  And we will display our result in an interactive interface that the user could set up filters and parameters to see the details of the result.

## 4	PROPOSED SOLUTION OR IDEA

1.	A time-series analysis will be conducted by comparing the COVID-19 infection number versus the vaccination number, to evaluate if vaccination effectively reduces the infections over time. 
2.	Hospitalization data and vaccination data will be analyzed and plotted, to evaluate if vaccination could reduce the risk of infections.
3.	The death with vaccination data will be compared to see if vaccines could truly reduce the death. 
4.	All the comparison results will be analyzed by different US states, to see if there are any differences. There is a possibility that the differences are caused by the states’ local policies. Further, 
5.	All the comparisons results will be analyzed by different Races/Ethnicity, to evaluate the effectiveness of vaccinations by Race/Ethnicity. 
6.	All the data/analysis/comparisons will be present with an interactive interface as a visualization.  The users will be able to set up filters and parameters to see the details of our study.

## 5	COMPLEXITY OR EFFORT

- Collecting vaccination data by different times, states, races/ethnicity, and ages completely could be challenged. We expected some data may not be available. 
- By now, we believe that four major types of data are needed in this project: the number of vaccinations, the number of COVID-19 infections, and the number of COVID-19 related hospitalizations, and the number of COVID-19 death. More data might be collected as the project move forward. 
- The data should be collected and analyzed in a time-series manner from March to July 2021, and futher analyzed by different US states,and by different groups of the population (race/ethnicity/age). 
- As the public health care of COVID-19 related data will be used, there is no privacy and security issue. 
- Python Dash/plotly is selected to build interactive web applications for result display. The user could define the limitations with the button, and the redefine-result will be present. We don’t have much experience with the framework. So, it might take us some time to get onto the right track.
## 6	TENTATIVE TEAM MEMBERS & ROLES (IF APPLICABLE)
We have 3 members in the team: Zuodong Jiang, Xinying Jia, Mengna Xia. 

Roles for the project: 

 6.1 Project Manager: Zuodong Jiang
Set up meeting agenda and time, make sure all member finish their tasks on time based on the Gantt table. 

6.2 Analyst:  
- Zuodong Jiang: 
Collect data from ourwoldindata.org
Person r and Granger causality in time series analysis
- Xinying Jia:
Collect data from CDC.org
Analyze the immune of age groups/vaccine brands vs. deaths/confirmed cases
- Mengna Xia:
Analyze the normalized data of total vaccinations vs. new cases/hospital patients/ICU patients
The sum and mean values for the statistical box

6.3 Developer: 
- Mengna Xia
The overall design and layout of the web application
The coding of interactive function parts
- Xinying Jia:
Building the group git repo
Develop the “fully vaccinations vs. un-vaccinations” figure and its sidebar
- Zuodong Jiang
Develop the dash table to display the correlation and granger results.

6.4 Quality assurance: Mengna Xia

6.5 Deployment: Mengna Xia
Deploy the web application on heroku.com



## 7	REFERENCES
- Coronavirus. (n.d.). Retrieved from who.int: https://www.who.int/health-topics/coronavirus#tab=tab_1
- COVID-19. (n.d.). Retrieved from wikipedia.org: https://en.wikipedia.org/wiki/COVID-19
- FDA. (2020, Novermber 11). Emergency use authorization for vaccines explained. Retrieved from fda.gov: https://www.fda.gov/vaccines-blood-biologics/vaccines/emergency-use-authorization-vaccines-explained
- Robson, D. (2021, Jul 20). Why some people don't want a Covid-19 vaccine. Retrieved from bbc.com: https://www.bbc.com/future/article/20210720-the-complexities-of-vaccine-hesitancy
- Wiersinga, W. J. (2020). Pathophysiology, transmission, diagnosis, and treatment of coronavirus disease 2019 (COVID-19): a review. Jama, 782-793

# Practicum Sprint #2

## PROJECT DESIGN 
Project Summary
The US public started to receive COVID19 vaccines around March 2021 and about 51.1% of the total population have received full doses of vaccinations now (COVID-19, 2021). However, there is still a huge population that is deeply skeptical about the safety and effectiveness of the mRNA vaccine and causing them reluctant to receive the inoculation (Robson, 2021)
In this study, we will use data visualization and modeling tools to analyze the public COVID-19 related health care data. Our goal is to provide real-world evidence for several major controversial topics about COVID-19 coronavirus:  
First, vaccine effectiveness will be quantified synchrony correlation between time series data by trying different statistical methods. We propose higher vaccination effectiveness can be proven by a lower correlation between vaccination and infection data. Then we will evaluate COVID-19 vaccine effectiveness based on COVID-19 related health care data.  Finally, we will display our data on the interactive webpage, so the reader could have a better visualization of our conclusion. 

## Tools and Technology
-	Jupyter Notebook will be used as an IDE.
-	Python libraries used for data extraction, cleaning, and transformation: Pandas, NumPy. 
-	Python libraries sci-kit learn used for machine learning model, script. stats used for correlation analysis
-	Python Plotly libraries will be used to select to build interactive web applications for data visualization. 
-	The interactive application will be uploaded and hosted in one free plotly account. 
-	Code will share between members on the GitHub repo

## Data Sources
The covid-19 data was collected from “Our World in Data” (Coronavirus Pandemic (COVID-19)). The original data sources for each data are as follows:
-	Confirmed cases and deaths data comes from the COVID-19 Data Repository by the Center for Systems Science and Engineering (CSSE) at Johns Hopkins University (JHU) (COVID-19 Content Portal);
-	Hospitalizations and intensive care unit (ICU) admissions data comes from the European Centre for Disease Prevention and Control (ECDC) for a select number of European countries, and government sources are from Switzerland, the UK, the US, Canada, Israel...
-	The data of COVID-19 testing and vaccinations against COVID-19 are collected by the Our World in Data team from official reports;
-	The data for other variables are collected from a variety of sources (United Nations, World Bank, Global Burden of Disease, Blavatnik School of Government, etc.).

## Diagrams
![architecture](../images/architecture.png)

Figure 1—	Web Application Architecture

![use_case](../images/useCase.png)

Figure 2—	Use case diagram for web application

![oriMockups](../images/oriMockups.png)

Figure 3—	screen mockups

## REFERENCES
- Coronavirus Pandemic (COVID-19). (n.d.). Retrieved from ourworldindata.org: https://ourworldindata.org/coronavirus
- COVID-19. (2021, Oct. 21). Retrieved from wikipedia.org: https://en.wikipedia.org/wiki/COVID-19
- COVID-19 Content Portal. (n.d.). Retrieved from CSSE: https://systems.jhu.edu/research/public-health/ncov/
- ECDC. (n.d.). Retrieved from ecdc.europa.eu/en: https://www.ecdc.europa.eu/en
- Robson, D. (2021, Jun 20). Why some people don't want a Covid-19 vaccine. Retrieved from bbc.com: https://www.bbc.com/future/article/20210720-the-complexities-of-vaccine-hesitancy

## Appendix

### IMPLEMENTATION PLAN

##### Project Tasks
-	Sprint 1: proposal of the project, background, content, potential risk. 
-	Sprint 2:  web application starting design, including the detailed plan, schedule, diagram, mockup, implementation plan, etc.
-	Sprint 3: data collecting, cleaning, and transformation.
-	Sprint 4: data analysis to find a good statistics metric to quantify synchrony between time-series correlation between covid-19 infection and vaccination data. 
-	Sprint 5: finalize the data analysis, to see if we still could achieve our original goal, do we need to add/remove some of our original goals.  
-	Sprint 6: start to build a web application.
-	Sprint 7: combine the web application with analyzed data.
-	Sprint 8: QA with test cases.
-	Sprint 9: deploy the web application.
-	Sprint 10：working on the presentation

##### Project Timeline
Table 1 —	Project schedule

| Week # | Week of | Task | Reading/Videos |
| ------ | ------  | -----| ------  |
5	09/20/2021	Choosing project topic and areas	
6	09/27/2021		
7	10/04/2021		
8	10/11/2021	Web application starting design, including the detailed plan, schedule, diagram, mockup, implementation plan, etc.	https://www.coursera.org/specializations/software-design-architecture


9	10/18/2021	Data collecting, cleaning, and transformation.	-	https://github.com/owid/covid-19-data/tree/master/public/data
-	https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_numpy.html

10	10/25/2021	Data analysis to find a good metric to measure the correlation between covid-19 infection and vaccination data.	-	https://scikit-learn.org/stable/
-	https://www.youtube.com/watch?v=0B5eIE_1vpU

11	11/01/2021	Finalize the data analysis, to see if we still could achieve our Original goal, do we need to add/remove some of our original goals. 	
12	11/08/2021	Build a web application.	https://plotly.com/python/

13	11/15/2021	Combine the web application with analyzed data.	
14	11/22/2021	QA with test cases.	
15	11/29/2021	Deploy the web application.	
16	12/06/2021	Prepare presentation	
17	12/13/2021	Finalize and submit all the files	
			
Needs/ Risks
1.	There is a limited time (less than 10 weeks).
2.	Communication between team members, and with the mentor.
3.	Data source:
o	Covid-19 data from specific countries with some time range could be missing. 
o	The quality of data needs to be validated. Only high-quality data should be selected for the study. 
4.	Data analysis
o	It is critical to find a correct method to measure the reverse correlation between infection and vaccination. 
o	Team members need to learn how to use different python libraries for data analysis, visualization.
5.	Developing and publishing the web application
o	Team members need to learn how to create a Plotly visualization and embed it on websites. 


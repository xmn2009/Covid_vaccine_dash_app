# Design Document

### Version Description

For Web Applicatin v 15: lastest update

**Author**: \<cs6440 Fall 2021 Group L>

## 1 Design Consideration

### 1.1 Assumptions
- This  web application is designed to run on web browser.
- Development will happen in Python JDK and Jupyter Notebook.
- User knows how to use web browser.
- User has some background knowledge of the COVID-19 pandemic.

### 1.2 Constraints

- Development tool : PyCharm and Jupyter Notebook
- SDK: Android SDK
- Programing Language: Python 3.9
- Language: English
- Input: Multi-touch
- Output: See section 1.3
- Device: See section 1.3 
- User Interface: Android pre-built UI components
- operating system: See section 1.3 

### 1.3 System Environment
#### Hardware
- There is no specific requirement on hardware

#### Software
- Web browser

## 2 Architectural Design
### 2.1 Component Diagram
![Cryptogram UML](./images/architecture.png)

Diagram above shows the architectural of the web application.


### 2.2 Deployment Diagram

The web application is design to be deployed on Heroku.com. See detail with special instructions [deployment](../Special Instructions.md)

## 3 Low-Level Design

In the component diagram in section 2.1 the **Android Device** and **Datastore** represent business concepts of the application. The **Datastore** is used for data storage and retrieval, while the **Android Device** is used to obtain user input and output data to the user. As such these two components are stereotyped as <<Entity>> to represent their purpose in the diagram.

3.0.1. **Administrator portal** component is used to manage the application, it provides the functionality of getting a collection of cryptogram statistics and disabling cryptograms which eventually deduct points from the creator of the cryptogram. It also accesses the datastore where cryptogram data is stored using a port.

![Administrator portal](./images/3.0.1-v3.png)

3.0.2. **Player Activities** This component handles the creation of a new player and login of a player. It has two ports which depend on the **Cryptogram manager component** to create a cryptogram and to solve a cryptogram.

![Player Activities](./images/3.0.2-v3.png)

3.0.3. **Cryptogram UI** component takes user input from the touch screen of the Android device, and sends output to the Android device for the end user to see. It is made up of the various activities of the android application. Because this component is part of GUI its implementation is not reflected in the design

3.0.4 **Cryptogram manager** component provides an interface for players to solve and create cryptograms, and also an interface for the administrator to disable a cryptogram. It stores and retrieves cryptogram data in the datastore. It provides the information about the cryptogram to the UI for display to the user.

![Cryptogram manager](./images/3.0.4-v3.png)


### 3.1 Class Diagram
![Cryptogram UML](./images/class_diagram-v3.png)

## 4 User Interface Design
#### Application Login:
![Login Page](./images/AppLoginPage_v3.png)

#### UI for Players:
![Player's Interfaces](./images/Interfaces_player_v3.png)

#### UI for Administrators:
![Adm's Interfaces](./images/Interfaces_Adm_v3.png)

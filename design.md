# Design

This design documents illustrate how the Team-beta Student IQ test implements the following @ref Requirements.

@section Project Project Overview

Student IQ test developed using HTML, CSS, PYTHON and SQL. This application helps user can take 10 minutes test to test the knowledge 
on different topics.

# Features
1. Register: Create a new account by providing your username, password, and email.
2. Login: Login to your account using your credentials. If the credentials are not match it will show the error message.
3. Dashboard: Access your personalized dashboard, which displays your profile information and previous test results.
4. Quiz: Take the IQ test by answering a series of questions. It has a time limit to finish the test. It will show on right side of the corner.
5. Result: After completing the quiz, view your IQ score and detailed analysis (bar chat, pie chat).

@section ModelViewController Model View Controller

This design applies the [Model View Controller](https://en.wikipedia.org/wiki/Model–view–controller) Design Pattern.

## Model

The Model consists of the following components:


@anchor R23_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/questions_fetch.py<br>
@anchor R79_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/quiz_analysis.py<br>
@anchor R104_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/app.py


## View

The View consists of the following components: 

@anchor R17_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/templates/register.html<br>
@anchor R20_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/templates/login.html<br>
@anchor R73_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/templates/quiz.html


## Controller

The Controller consists of the following component:

@anchor R68_0 https://github.com/WSUCEG-7140/Team-Beta/blob/main/instance/users.db


## Forms

We use csv file to store the questions. The csv file consists various types of questions.

https://github.com/WSUCEG-7140/Team-Beta/blob/main/quiz.csv

# Agile Central Command
An application that holds all features needed for the agile methodology that integrates with Jira

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installation
#### Django
1. Clone project
2. ```pip install virtualenv``` (*)
3. ```cd Group10-Agile-Command-Central-API```
4. ```virtualenv env -p python3``` (*)
5. ```source env/bin/activate```
6. ```pip install -r requirements.txt```
7. ```python manage.py migrate```
8. Install Pep8, MySQL, Redis (*)
9. ```python manage.py runserver```

Note: * skip this step if this is not the first time you set up the project

#### Pep8 Style Guide
- Visual Studio Code: https://code.visualstudio.com/docs/python/linting
- Atom: https://atom.io/packages/pep8
- Sublime Text: https://packagecontrol.io/packages/Python%20PEP8%20Autoformat

#### MySQL (Linux)
- Checkout this page to install MySQL: https://www.digitalocean.com/community/tutorials/how-to-use-mysql-or-mariadb-with-your-django-application-on-ubuntu-14-04
- Do not install MySQL Community Server on Mac
- Install MySQL with brew
1. ```brew install mysql```
2. ```brew services start mysql```
3. ```mysql -uroot```
4. ```CREATE DATABASE agilecommandcentral CHARACTER SET UTF8;```
5. ```CREATE USER group10@localhost IDENTIFIED BY 'password';```
6. ```GRANT ALL PRIVILEGES ON agilecommandcentral.* TO group10@localhost;```

#### Redis for Django Channels (Linux)
- ```brew install redis```
- ```brew services start redis```

## Running tests
1. Coverage
    - Everytime you add some code to the project run this: ```coverage run --source ='.' manage.py test```
    - Read coverage report: ```coverage report```
2. Jira shell
    - Play with Jira API: ```jirashell -s jira-board-url```

## Deployment
How to deploy...

## Built With
* Django - Web framework
* React - Front End
* Jira API - Integration
* AWS - Deployment
* iOS - Mobile Development

## Authors
* Katherine Rosenfeld - Front End
* Kyle Capehart - Database, AWS, Jira API
* Lee Alan Wildes - AWS, Front End
* Leonardo Araque - Mobile Development
* Tuan Pham - Backend, REST API, Jira API

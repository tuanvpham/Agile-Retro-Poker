# Agile Central Command
An application that holds all features needed for the agile methodology that integrates with Jira

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Installing
#### Django
1. Clone project
2. Install pip (package manager)

    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    sudo python get-pip.py
    ```
3. Install virtualenv (dev environment)

    ```
    pip install virtualenv
    ```
4. Change directory to project's directory
5. ```virtualenv env -p python3```
6. ```source env/bin/activate```
7. ```pip install -r requirements.txt```
8. ```python manage.py migrate```
9. To run the app: ```python manage.py runserver```
10. You will see a portal to the project on terminal (something like http://127.0.0.1:8000/).

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

- From agilecommandcentral project directory, run 
1. ```python manage.py makemigrations```
2. ```python manage.py migrate```
3. ```python manage.py runserver```


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

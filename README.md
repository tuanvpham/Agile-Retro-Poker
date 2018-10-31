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
- Check out this page to install pep8 on Visual Studio Code: https://code.visualstudio.com/docs/python/linting


## Running tests
How to run tests...

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
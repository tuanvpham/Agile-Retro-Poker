Using the Database

Make sure that mysql server is installed
https://dev.mysql.com/downloads/mysql/

start the mysql server service

from the command line:
	$ mysql -u root -p

this should connect to your server

create the database, make sure you name it dacc_db
	$ CREATE DATABASE dacc_db;
	$ USE dacc_db;

then using the path to the dacc.sql script
	$ source %path%

insert the password that you used into core/views.py and agilecommandcentral/settings.py

the start the django app server and navigate to http://127.0.0.1:8000/core/

if you get an error about the msql connector not being installed then use this command
	$ pip install mysql-connector-python-rf

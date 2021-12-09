

# Capstone Project - restock_checker 
**Danny Li, Alden Lee, Ethan Tam, Oscar Andrade, David Xue**


Our Project Aims to allow for people and users to keep track of various high demand items. We've currently implemented an email notification system for users to be notified of restocks. We also have a search bar for users to search the 200 or so products tracked on our page.

Live version can be found: restockchecker.herokuapp.com 

Note: *LIVE CURRENTLY*





# Django Section



requires:

pip install django

pip install python-decouple

pip install mysqlclient

(you will also need to have MYSQL installed as we'll be using MYSQL for our database)

Note: you'll also need to set your mysql username to **root** , mysql password to **password** and have a mysql database called **restock** 

To get the all tables into your database, run the command:
"python manage.py migrate"

pip install gunicorn

pip install whitenoise

pip install pyscopg2

**No longer uses python manage.py runserver**

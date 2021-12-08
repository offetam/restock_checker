

# Capstone Project - restock_checker 
**Danny Li, Alden Lee, Ethan Tam, Oscar Andrade, David Xue**

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

To run program:
To login to heroku, run: "heroku login"
To run locally, run: "heroku local"
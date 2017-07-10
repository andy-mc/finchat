FinChat
=======

Simple chat with a bot integrated that makes queries to yahoo finance.

Users has a profile page where all messages from a given user can be seen.

The authentication, signup, loging and logout are built on top of djangos auth
system.


>> How to running locally:

Create a virtual env for the project, the project runs in python 3
and them install the requirements with:

    pip install -r requirements.txt

The project uses channel, for this reason you will need Redis 
running locally as well, for install redis on mac you can use brew:

    brew install redis

And running redis locally on a diferent terminal with:
	
	redis-server

By default redis run on port 6379, you can change this on the settings.py file

You can create a superuser acount for logging in and out with:
    
    python manage.py createsuperuser

Finally migrate the proyects model and run the project locally with:

    python manage.py migrate
    python manage.py runserver


>> How to use the finBot:


# FinChat with Django
========================

Simple chat that can make calls to an external finbot_rpc_server
a service that makes queries to yahoo finance.

Users has a profile page where all messages from the log-in user can be seen.

The authentication, signup, loging and logout are built on top of djangos auth-system.


# How to running locally:

Create a virtual env for the project (you'll need python 3)
and them install the requirements with:

    pip install -r requirements.txt

The project uses channels, for this reason you'll need Redis running locally, for install redis on mac you can use brew:

    brew install redis

And running redis locally on a diferent terminal with:
    
    redis-server

By default redis run on port 6379, you can change this on the settings.py file

Additionally you need to run a finbot_rpc_server to response all
the calls asking for financial information, more on how to run 
finbot_rpc_server on:
    
    https://github.com/andy-mc/finbot_rpc_server

You can create a superuser acount for logging in and out with:
    
    python manage.py createsuperuser

Finally migrate the proyects models and run the project locally with:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver


# How to use the finBot:

    ## make sure finbot_rpc_server is running.

    Simply send a chat message of the format /command=stock
    for example, /stock=AAPL and the finbot will return the financial information:

        AAPL (Apple Inc.) quote is $144.18 per share

    The bot has 2 commands:
        1) /stock=AAPL  -->  return the close price for a given stock.
        2) /day_range=AAPL  -->  return the day high/low price for a given stock.


>> If you want to run the test suit, simply run:

    python manage.py test

Fake data for testing purposes could be generated using UserFactory, MessageFactory 
in chat.factories.py

If python manage.py test through and error please try again, I been having problems
trying too create unique usernames each time python manage.py test run, is not a 
frequent error but could happen.
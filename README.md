# FinChat with Django

Simple chat with a bot integrated that makes queries to yahoo finance.

Users has a profile page where all messages from the log-in user can be seen.

The authentication, signup, loging and logout are built on top of djangos auth-system.


# How to running locally:

Create a python 3 virtual env for the project
and them install the requirements with:

    pip install -r requirements.txt

The project uses channels with RabbitMQ, for this reason you'll need RabbitMQ running locally,
for install RabbitMQ on mac you can use brew:

    brew install rabbitmq

to install RabbitMQ on others OS please check, https://www.rabbitmq.com/download.html

Run RabbitMQ locally on a second terminal with:
    
    rabbitmq-server

for RabbitMQ customization Check CHANNEL_LAYERS config in settings.py.

You can create a superuser acount for logging in and out with:
    
    python manage.py createsuperuser

Finally migrate the proyects models and run the project locally with:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver


# How to use the finBot:

    Simply send a chat message of the format /command=stock
    for example, /stock=AAPL and the bot will return the financial information:

        AAPL (Apple Inc.) quote is $144.18 per share

    The bot has 2 commands:

        1) /stock=AAPL  -->  return the close price for a given stock.
        2) /day_range=AAPL  -->  return the day high/low price for a given stock.


>> If you want to run the test suit, simply run:

    python manage.py test

Fake data for testing purposes could be generated using UserFactory, MessageFactory 
in chat.factories.py from the django shell.

If python manage.py test through and error please try again, I been having problems
trying too create unique usernames each time python manage.py test run, is not a 
frequent error but could happen.
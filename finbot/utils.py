import bs4 as bs
import urllib.request

from datetime import datetime


def stock_bot(stock):
    """
    Make a query to yahoo to get the stock_name and the previous close price of a given stock
    """
    link = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{}%22)&env=store://datatables.org/alltableswithkeys"
    link = link.format(stock)
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    table = soup.find('quote')
    stock_name = table.find('name').text
    previous_close = table.find('previousclose').text

    return "{} ({}) quote is ${} per share".format(stock, stock_name, previous_close)


def day_range_stock_bot(stock):
    """
    Make a query to yahoo to get the stock_name and day low/high prices of a given stock
    """
    link = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22{}%22)&env=store://datatables.org/alltableswithkeys"
    link = link.format(stock)
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source, 'lxml')

    table = soup.find('quote')
    stock_name = table.find('name').text
    days_low = table.find('dayslow').text
    days_high = table.find('dayshigh').text

    return "{} ({}) Days Low quote is ${} and Days High quote is ${}".format(stock, stock_name, days_low, days_high)


def finbot(user_message):
    """
    Take a user_message compounded by a command and a stock 
    and return the bot_response to given command.
    """
    command, stock = user_message.strip().split('=')
    now = datetime.now().strftime('%b %-d %-I:%M %p')

    if command.strip() == '/stock':
        stock_quote = stock_bot(stock)

    if command.strip() == '/day_range':
        stock_quote = day_range_stock_bot(stock)

    bot_response = {
        "username": "finbot",
        "message": stock_quote,
        "timestamp": now,
    }

    return bot_response

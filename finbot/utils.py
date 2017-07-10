from datetime import datetime


def stock_bot(stock):
    """
    ????????
    """
    return "APPL (apple INC) quote is $93.42 per share"


def day_range_stock_bot(stock):
    """
    ????????
    """
    return "APPL (apple INC) Days Low quote is $ 92.11 and Days High quote is $94.15"


def finbot(command):
    """
    ????????
    """
    action, stock = command.strip().split('=')
    now = datetime.now().strftime('%b %-d %-I:%M %p')

    if action.strip() == '/stock':
        stock_quote = stock_bot(stock)

    if action.strip() == '/day_range':
        stock_quote = day_range_stock_bot(stock)

    bot_message = {
        "username": "finbot",
        "message": stock_quote,
        "timestamp": now,
    }

    return bot_message

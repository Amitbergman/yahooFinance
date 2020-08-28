from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from openpyxl import load_workbook
from datetime import datetime, date
import keys
import requests
from bs4 import BeautifulSoup

PriceToSellNvidia = 480
PriceToSellDelta = 42


def mainFunction():
    stocks = ["MSFT", "IBM", "NVDA", "DAL"]
    prices = []
    for stock in stocks:
        prices.append(getPrice(stock))
    
    nvdaShouldBeSold = prices[2] > PriceToSellNvidia
    deltaShouldBeSold = prices[3] > PriceToSellDelta

    if (nvdaShouldBeSold):
        sendEmailAlert("Time to sell Nvidia!", prices)
    elif (deltaShouldBeSold):
        sendEmailAlert("Time to sell Delta!", prices)
    else:
        sendEmailAlert("Everything is regular", prices)
    date_today = date.today()
    prices.append(date_today)
    writeRowToExcel("stocks.xlsx", prices)

def writeRowToExcel(excelName, rowToAdd):

    wb = load_workbook(excelName)
    # Select First Worksheet
    ws = wb.worksheets[0]

    ws.append(rowToAdd)

    wb.save(excelName)
    wb.close()
    


def getPrice(stockSymbol):
    #stockSymbol is : MSFT for Microsoft

    url = "https://finance.yahoo.com/quote/{}".format(stockSymbol)
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    currentPrice = soup.find_all('span',attrs={"class": "D(ib)"})
    for element in currentPrice:
        classes = element.attrs['class']
        l = ['36px' in st for st in classes]
        if (any(l)):
            price = element
            break
    
    print("{} : {}".format(stockSymbol, price.get_text()))
    return float(price.get_text())

"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

def sendEmailAlert(text, prices):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    port = 465  # For SSL
    password = keys.keys['password']
    pricesAsStrings = [str(price) for price in prices]
# Create a secure SSL context
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = text
    message["From"] = "BOT"
    message["To"] = keys.keys['myMail']

    part1 = MIMEText(', '.join(pricesAsStrings), "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(keys.keys['botMail'], password)
        # TODO: Send email here
        server.sendmail(keys.keys['botMail'], keys.keys['myMail'], message.as_string())
        print(message.as_string())
        print("cool! Email sent!")


mainFunction()

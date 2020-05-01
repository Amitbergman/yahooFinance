import yfinance as yf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from openpyxl import load_workbook
from datetime import datetime, date
import keys

def mainFunction():
    (msft,ibm) = createTickers("MSFT", "IBM")
    msft_price = getPrice(msft)
    ibm_price = getPrice(ibm)

    prices_array = [msft_price, ibm_price]

    sendEmailWithPrices(prices_array)

    date_today = date.today()
    prices_array.append(date_today)
    writeRowToExcel("stocks.xlsx", prices_array)

def writeRowToExcel(excelName, rowToAdd):

    wb = load_workbook(excelName)
    # Select First Worksheet
    ws = wb.worksheets[0]

    ws.append(rowToAdd)

    wb.save(excelName)
    wb.close()
    

def createTickers(stockName1, stockName2):
    ticker1 = yf.Ticker(stockName1)
    ticker2 = yf.Ticker(stockName2)
    return (ticker1, ticker2)

def getPrice(stock):
    return stock.info['regularMarketPreviousClose']


"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

def sendEmailWithPrices(prices_array):

    server = smtplib.SMTP('smtp.gmail.com', 587)
    port = 465  # For SSL
    password = keys.keys['yahoo']

# Create a secure SSL context
    context = ssl.create_default_context()
    text = f"The prices of msft stock today was: {prices_array[0]}.\n The price of IBM was: {prices_array[1]}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Report for Amit"
    message["From"] = "Amit"
    message["To"] = keys.keys['myMail']

    part1 = MIMEText(text, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(keys.keys['botMail'], password)
        # TODO: Send email here
        server.sendmail(keys.keys['botMail'], keys.keys['myMail'], message.as_string())
        print(message.as_string())
        print("cool! Email sent!")


mainFunction()
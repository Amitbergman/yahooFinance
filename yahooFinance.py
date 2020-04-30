import yfinance as yf
msft = yf.Ticker("MSFT")
ibm = yf.Ticker("IBM")

msft_price = msft.info['regularMarketPreviousClose']
ibm_price = ibm.info['regularMarketPreviousClose']

prices = [msft_price, ibm_price]
print(prices)

"""The first step is to create an SMTP object, each object is used for connection 
with one server."""

import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

import smtplib, ssl

port = 465  # For SSL
password = "Beni1234"

# Create a secure SSL context
context = ssl.create_default_context()
message = f"The prices of msft stock today was: {msft_price}.\n The price of IBM was: {ibm_price}"
print(message)
with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("benbenelieli123beni@gmail.com", password)
    # TODO: Send email here
    server.sendmail("benbenelieli123beni@gmail.com", "amitbergman@gmail.com", message)

    print("cool!")
    
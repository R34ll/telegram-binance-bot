import telebot
import config
from binance import Client


from matplotlib import pyplot as plt
from matplotlib import dates as mdates

import pandas as pd
import datetime
import io




def get_btc_usdt(msg):
        client = Client(config.BINANCE_API_KEY, config.BINANCE_API_SECRET_KEY)
        

        def unix_to_datetime(unix_time):
            return datetime.datetime.fromtimestamp(unix_time/1000.0)
    
        def date_to_unix(date):
            date = datetime.datetime.now()
            date = date.replace(hour=0, minute=0, second=0, microsecond=0)
            date = date - datetime.timedelta(days=14)
            return int(date.timestamp() * 1000)


        crypto = "BTCUSDT"

        klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_1HOUR, date_to_unix(datetime.datetime.now()))
        values = [[unix_to_datetime(el[0]), float(el[1])] for el in klines]


        # Get the current ticker price
        ticker = client.get_ticker(symbol=crypto)
        current_price = float(ticker['lastPrice'])


        # Create a DataFrame from the data
        df = pd.DataFrame(values, columns=['ds', 'y'])

        # Plot the data
        fig, ax = plt.subplots()
        plt.title("BTC HISTORIC (Last 2 weeks)")
        plt.grid(True)
        ax.plot(df['ds'], df['y'], ls=":")

        # Format x-axis labels as dates
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # Show every day
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))  # Format as DD/MM/YY

        fig.set_size_inches(15, 6)  # Adjust the width as needed

        # Rotate x-axis labels for better visibility
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=35, ha='right')

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        # Send the plot as a photo in the Telegram chat
        caption = f"__Bitcoin Price Today__:  *${int(current_price)}*"
        bot.send_photo(msg.chat.id, img, caption=caption, parse_mode="MarkdownV2")





if __name__ == "__main__":
    bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)



    @bot.message_handler(commands=["start"])
    def on_ready(msg):
        greeting_message = f"Hello *{msg.from_user.first_name}*"
        return bot.reply_to(msg, greeting_message, parse_mode="MarkdownV2")


    @bot.message_handler(commands=["BTC"])
    def handle_btc_msg(msg):
        get_btc_usdt(msg)



    bot.infinity_polling()







from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests
import time
debug=False
updater = Updater(token='1213698143:AAFRC-uNPz_2Xi-5Suy-F95E4Z7Ein-SccA', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, I am CoronaIndia Bot. I am happy to help you. You can get the latest statistics of Covid-19 from me.\nSend /total for Total Statistics \nSend /state state_name to get State Statistics")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def total(update, context):
    url = 'https://api.covid19india.org/data.json'
    r = requests.get(url)
    data = r.json()
    state_data_with_total = data["statewise"]
    for item in state_data_with_total:
        if (item['state'] == "Total"):
            total_stat = item
            break
        else:
            total_stat = None
    reply = "COVID-19 Statistics:- Total cases : "+str(total_stat["confirmed"])+", Active cases : " +str(total_stat["active"])+", Recovered Cases : "+str(total_stat["recovered"])+", Deceased : "+str(total_stat["deaths"])
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

total_handler = CommandHandler('total', total)
dispatcher.add_handler(total_handler)

def state(update, context):
    rec_state = ' '.join(context.args)
    if(rec_state.strip()!=''):
        url = 'https://api.covid19india.org/data.json'
        r = requests.get(url)
        data = r.json()
        state_data = data["statewise"]
        flag=0
        for dict in state_data:
            curr_state=dict["state"]
            
            if(rec_state.upper() in curr_state.upper()):
                flag=1
                reply= "COVID-19 Statistics for "+dict["state"]+"  :- Total cases : "+str(dict["confirmed"])+", Active cases : " +str(dict["active"])+", Recovered Cases : "+str(dict["recovered"])+", Deceased : "+str(dict["deaths"])
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply)  
        if(flag==0):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Couldn't find that. Try again")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have to enter a state")


state_handler = CommandHandler('state', state)
dispatcher.add_handler(state_handler)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

print("Starting the bot...")
if(debug==False):
    while(True):
        try:
            updater.start_polling()
        except:
            print("An exception occurred. Sleeping for 5 Seconds")
            time.sleep(5)
else:
    updater.start_polling()
    updater.idle()







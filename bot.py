from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests
import time
import telegram
debug=True

#687807496
adminbot = telegram.Bot(token='1153123573:AAF-rWy5KcStsIb8mxhgXF5FKqhFJdzuWmI')
if(debug):
    updater = Updater(token='1233520288:AAEGhHdGospRuaoQZldP8-xqBI4Lj5pRNsg', use_context=True)
else:
    updater = Updater(token='1213698143:AAFRC-uNPz_2Xi-5Suy-F95E4Z7Ein-SccA', use_context=True)

url = 'https://api.covid19india.org/data.json'
districtsUrl='https://api.covid19india.org/v2/state_district_wise.json'

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

state_codes= ['TT','MH', 'DL', 'TN', 'RJ', 'MP', 'UP', 'GJ', 'TG', 'AP', 'KL', 'JK', 'KA', 'HR', 'WB', 'PB', 'BR', 'OR', 'UT', 'CT', 'HP', 'AS', 'JH', 'CH', 'LA', 'AN', 'GA', 'PY', 'MN', 'TR', 'MZ', 'AR', 'DN', 'NL', 'ML', 'DD', 'LD', 'SK']

def start(update, context):
    welcome="Hi, I am CoronaIndia Bot\n"
    total="For total stats send or click on /total\n"
    state="For State stats send \"/state state_name\" For example \"/state telangana\"\n"
    state_code="Or send /<state-code> For example /AP\nTo get list of statecodes send or clik on \n/codelist"
    reply=welcome+total+state+state_code
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    adminbot.send_message(chat_id="687807496", text="New start -->"+str(update._effective_chat))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def state_code(update,context):
    text=update.message.text
    code=text[1:].upper()
    if (code=="TT"):
        total(update, context)
    else:
        r = requests.get(url)
        data = r.json()
        state_data = data["statewise"]
        for state in state_data:
            if(state['statecode']==code):
                curr_state=state
                reply="COVID-19 Statistics for "+curr_state["state"]+"  :-\n\nTotal cases : "+str(curr_state["confirmed"])+", Active cases : " +str(curr_state["active"])+", Recovered Cases : "+str(curr_state["recovered"])+", Deceased : "+str(curr_state["deaths"])+"\n\nDistrict Wise Total Confirmed:\n\n"
                reply+=get_dist_wise(curr_state["state"])
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply)


for code in state_codes:
    state_code_handler=CommandHandler(code, state_code)
    dispatcher.add_handler(state_code_handler)

def state_code_list(update,context):
    r = requests.get(url)
    data = r.json()
    state_data = data["statewise"]
    reply="STATE CODES\n"
    for state in state_data:
        reply= reply +state["state"]+" : "+state["statecode"]+"\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

state_code_list_handler = CommandHandler('codelist', state_code_list)
dispatcher.add_handler(state_code_list_handler)

def total(update, context):
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
        r = requests.get(url)
        data = r.json()
        state_data = data["statewise"]
        flag=0
        for dict in state_data:
            curr_state=dict["state"]
            
            if(rec_state.upper() in curr_state.upper()):
                flag=1
                reply= "COVID-19 Statistics for "+dict["state"]+"  :-\n\nTotal cases : "+str(dict["confirmed"])+", Active cases : " +str(dict["active"])+", Recovered Cases : "+str(dict["recovered"])+", Deceased : "+str(dict["deaths"])+"\n\nDistrict Wise Total Confirmed:\n\n"
                reply+=get_dist_wise(dict["state"])
                context.bot.send_message(chat_id=update.effective_chat.id, text=reply)  
        if(flag==0):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Couldn't find that. Try again")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You have to enter a state")


state_handler = CommandHandler('state', state)
dispatcher.add_handler(state_handler)

def get_dist_wise(state):
    r = requests.get(districtsUrl)
    data = r.json()
    flag=False
    for state_data in data:
        if (state_data["state"]==state):
            response=state_data["districtData"]
            flag=True
    if(flag):
        reply=""
        for district in response:
            reply+=district["district"]+" : "+str(district["confirmed"])+"\n"
        return reply
    else:
        return None




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







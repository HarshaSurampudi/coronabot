import telegram
bot = telegram.Bot(token='1153123573:AAF-rWy5KcStsIb8mxhgXF5FKqhFJdzuWmI')
import requests

url = 'https://api.covid19india.org/data.json'
try:
    r = requests.get(url)
    data = r.json()
    state_data_with_total = data["statewise"]
    for item in state_data_with_total:
        if (item['state'] == "Total"):
            total_stat = item
            break
        else:
            total_stat = None    
    reply = "Total cases : "+str(total_stat["confirmed"])+"(+"+str(total_stat["deltaconfirmed"])+")"+"\nActive cases : " +str(total_stat["active"])+"(+"+str(int(total_stat["deltaconfirmed"])-int(total_stat["deltarecovered"])-int(total_stat["deltadeaths"]))+")"+"\nRecovered Cases : "+str(total_stat["recovered"])+"(+"+str(total_stat["deltarecovered"])+")"+"\nDeceased : "+str(total_stat["deaths"])+"(+"+str(total_stat["deltadeaths"])+")"

    if(total_stat is not None):
        print("Sending Hourly Update...")
        bot.send_message(chat_id="@covid19trackerindia", text=reply)
    else:
        print("Empty response received")
except Exception as e:
    print(e)


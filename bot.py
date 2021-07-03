from telegram import ChatAction, Bot, ParseMode
from os import getenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from dotenv import load_dotenv
import requests, json
from datetime import datetime
load_dotenv()

TOKEN = getenv('TOKEN')

bot = Bot(token=TOKEN)



today_dt = datetime.now()
today_dt = today_dt.strftime("%d-%m-%Y")
# print(today_dt)

    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, Send me your area PINCODE  ')

def vaccine_update (update, context) :
        
    try:    
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
            pincode = update.effective_message.text
          

            
            
            # pincode = int(input("Enter your pincode: "))
            
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={pincode}&date={today_dt}"

            response = requests.get(url, headers = headers)
            json_data = json.loads(response.text)
        
            if len(json_data['sessions']) == 0:
                # print("Sorry, No Slots Available! Try again later...")
                 update.message.reply_text("Sorry, No Slots Available! Try again later...")
            else:   
                for center in json_data['sessions']:
                    vac_updt = f"\nCenter Id: {center['center_id']}\nAddress: {center['name']}, {center['address']}\nDistrict: {center['district_name']}\n1st Dose Availability: {center['available_capacity_dose1']}\n2nd Dose Availability: {center['available_capacity_dose2']}\nMin Age Limit: {center['min_age_limit']}yrs\nVaccine: {center['vaccine']}\nFee: Rs {center['fee']}/-\n"
                    for slot in center['slots']:
                        timng = f"Time Slot: {slot}"
                         
                    final_updt = vac_updt + timng
                    update.message.reply_text(f'{final_updt}')

    except:            

    
        # print("Invalid Pincode! Please try again")
        update.message.reply_text("Invalid Pincode! Please try again")
        




updater = Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, vaccine_update))
updater.start_polling()
updater.idle()
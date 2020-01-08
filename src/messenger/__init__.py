from src.messenger.facebook_messenger import Messenger
from fbmessenger.thread_settings import PersistentMenu, PersistentMenuItem, MessengerProfile, GreetingText, GetStartedButton
from src.states import State
import json
import os

texts = json.load(open(os.path.abspath(os.path.join(os.getcwd(), "src/texts.json")), 'r'))


msngr = Messenger()
greeting_text = GreetingText(texts["greetings"])


schedule_order_now_menu_item = PersistentMenuItem(item_type="postback", title="Schedule Order Now", payload=State.SCHEDULE_ORDER)
login_item = PersistentMenuItem(item_type="postback", title="Login", payload=State.LOGIN)
register_item = PersistentMenuItem(item_type="postback", title="Register", payload=State.REGISTER)

menu = PersistentMenu(menu_items=[schedule_order_now_menu_item, login_item, register_item])


messenger_profile = MessengerProfile(persistent_menus=[menu], greetings=[greeting_text], get_started=GetStartedButton(payload=State.HI))
msngr.set_messenger_profile(messenger_profile.to_dict())

print("msngr profile set")

def handle_message(json_response):
    msngr.handle(json_response)
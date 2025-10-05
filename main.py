import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
API_KEY = "7f92c6a23ac995c46bd62dc8567769f1"
TOKEN = "8450438222:AAHRDN2Cw4TR3SJbkEY_IpFyxxBdl3T_J14"
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def get_song(message):
    bot.send_message(message.chat.id, "what is your fav song at the moment :) ?")
    bot.register_next_step_handler(message, get_artist)
def get_artist(message):
    song_name = message.text
    bot.send_message(message.chat.id, "What is the name of the artist of that song ?")
    bot.register_next_step_handler(message, recommond_song, song_name)
def recommond_song(message, song_name):
    artist_name = message.text
    simliar_tracks = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist_name}&track={song_name}&api_key={API_KEY}&format=json").json()["similartracks"]["track"]
    for i in simliar_tracks[:6]:
        track_info = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={API_KEY}&artist={i["artist"]["name"]}&track={i["name"]}&format=json").json()["track"]
        track_cover = track_info["album"]["image"][3]["#text"]
        track_url = track_info["url"]
        markup = InlineKeyboardMarkup()
        btn_label = f"{i["name"]} - {i["artist"]["name"]}"
        track_url_btn = InlineKeyboardButton(text=btn_label, url=track_url)
        markup.add(track_url_btn)
        bot.send_photo(message.chat.id, track_cover, reply_markup=markup)
bot.infinity_polling()
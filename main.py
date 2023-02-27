import os
import io
import re
import requests
import mutagen
from mutagen.mp3 import MP3
from music_tag import load_file
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config


Bot = Client(
    "MusicBot",
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)


START_TXT = """
Hi {}, I'm Music Channel Manager.

I can manage your music channel with some cool features like appending your predefined username to the musics tags, getting a short demo of the musics and posting the musics artworks.

Just add me to a channel and post a music to get started.
"""

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Source Code', url='https://github.com/samadii/MusicChannelManagerV2'),
        ]]
    )


@Bot.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TXT.format(update.from_user.mention)
    reply_markup = START_BTN
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

    
@Bot.on_message(filters.channel & filters.audio)
async def music(bot, m):
    file = await m.download("temp/file.mp3")
    await m.delete()
    music = load_file("temp/file.mp3")
    
    try:
        artwork = music['artwork']
        image_data = artwork.value.data
        img = Image.open(io.BytesIO(image_data))
        img.save("artwork.jpg")
    except ValueError:
        artwork = None 

    if artwork is not None:
        try:
            await bot.send_photo(
                chat_id=m.chat.id,
                caption="🎤" + a + " - " + t + "🎼" + "\n\n" + f"🆔👉 {Config.USERNAME}",
                photo=open('artwork.jpg', 'rb')
            )
        except Exception as e:
            print(e)

    audio = MP3(file)
    length = audio.info.length * 0.33
    l2 = (audio.info.length * 0.33) + 60
    if audio.info.length > l2:
        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + file + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
    else:
        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + file + "\" -ac 1 -map 0:a -codec:a libopus -b:a 128k -vbr off -ar 24000 temp/output.ogg")
    sendVoice(m.chat.id, "temp/output.ogg", f"🎤{a} - {t}🎼\n\n🆔👉 {Config.USERNAME}")
    
    fname = remove_tags(m.audio.file_name)
    title = remove_tags(f"{music['title']}")
    artist = remove_tags(f"{music['artist']}")
    album = remove_tags(f"{music['album']}")
    genre = remove_tags(f"{music['genre']}")
    comment = remove_tags(f"{music['comment']}")
    lyrics = remove_tags(f"{music['lyrics']}")
    
    # remove tags
    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('lyrics')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    
    # apply new tags
    music['artist'] = artist + Config.custom_tag
    music['title'] = title + Config.custom_tag
    music['album'] = album + Config.custom_tag
    music['genre'] = genre + Config.custom_tag
    music['comment'] = comment + Config.custom_tag
    music['lyrics'] = lyrics + Config.custom_tag
    music.save()

    if Config.CAPTION == "TRUE":
        caption = "✏️ Title: " + t + "\n" + "👤 Artist: " + a + "\n" + "💽 Album: " + al + "\n" + "🎼 Genre: " + g + "\n\n" + f"🆔👉 {Config.USERNAME}"
    else:
        caption = m.caption if m.caption else " "

    try:
        if artwork is not None:
            await bot.send_audio(
                chat_id=m.chat.id,
                file_name=fname,
                performer=a,
                title=t,
                duration=m.audio.duration,
                caption=caption,
                thumb=open('artwork.jpg', 'rb'),
                audio='temp/file.mp3'
            )
        elif artwork is None:
            await bot.send_audio(
                chat_id=m.chat.id,
                file_name=fname,
                performer=a,
                title=t,
                duration=m.audio.duration,
                caption=caption,
                audio='temp/file.mp3'
            )
    except Exception as e:
        print(e)

def remove_tags(arg):
    if arg.__contains__("@") or arg.__contains__(".me/"):
        arg = re.sub(r'\S*[t|T].me\S*|\S*@\S*', '', arg).replace('  ', ' ')
    if arg.startswith(' '):
        arg = arg.split(' ', 1)[+1]
    return arg
    
def sendVoice(chat_id,file_name,text):
    url = "https://api.telegram.org/bot%s/sendVoice"%(Config.BOT_TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption' : text}
    r= requests.post(url, files=files, data=data)
   

Bot.run()

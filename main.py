import os
import io
import requests
import mutagen
from mutagen.mp3 import MP3
from music_tag import load_file
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config


Bot = Client(
    "Bot",
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
async def tag(bot, m):
    fname = m.audio.file_name
    m = await bot.get_messages(m.chat.id, m.message_id)
    file = await m.download(file_name="temp/file.mp3")
    await m.delete()
    music = load_file("temp/file.mp3")
    t = f"{music['title']}"
    a = f"{music['artist']}"
    al = f"{music['album']}"
    g = f"{music['genre']}"
    c = f"{music['comment']}"
    l = f"{music['lyrics']}"
    ar = music['artwork']
    image_data = ar.value.data
    img = Image.open(io.BytesIO(image_data))
    img.save("artwork.jpg")
  
    if fname.__contains__("@") or fname.__contains__(".me/"):
        first = fname.split(' ')[0]
        last = fname.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            filename = fname.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            filename = fname.split(f"{fname.rsplit(' ', 1)[1]}")[0]
    else:
        filename = fname

    if g.__contains__("@") or g.__contains__(".me/"):
        first = g.split(' ')[0]
        last = g.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            genre = g.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            genre = g.split(f"{g.rsplit(' ', 1)[1]}")[0]
    else:
        genre = g
    
    if l.__contains__("@") or l.__contains__(".me/"):
        first = l.split(' ')[0]
        last = l.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            lyrics = l.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            lyrics = l.split(f"{l.rsplit(' ', 1)[1]}")[0]
    else:
        lyrics = l

    if c.__contains__("@") or c.__contains__(".me/"):
        first = c.split(' ')[0]
        last = c.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            comment = c.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            comment = c.split(f"{c.rsplit(' ', 1)[1]}")[0]
    else:
        comment = c

    if t.__contains__("@") or t.__contains__(".me/"):
        first = t.split(' ')[0]
        last = t.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            title = t.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            title = t.split(f"{t.rsplit(' ', 1)[1]}")[0]
    else:
        title = t

    if al.__contains__("@") or al.__contains__(".me/"):
        first = al.split(' ')[0]
        last = al.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            album = al.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            album = al.split(f"{al.rsplit(' ', 1)[1]}")[0]
    else:
        album = al

    if a.__contains__("@") or a.__contains__(".me/"):
        first = a.split(' ')[0]
        last = a.rsplit(' ')[0]
        if first.__contains__("@") or first.__contains__(".me/"):
            artist = a.split(f'{first}')[+1]
        if last.__contains__("@") or last.__contains__(".me/"):
            artist = a.split(f"{a.rsplit(' ', 1)[1]}")[0]
    else:
        artist = a

    try:
        await bot.send_photo(
            chat_id=m.chat.id,
            caption="🎤" + artist + " - " + title + "🎼" + "\n\n" + f"🆔👉 {Config.USERNAME}",
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
    sendVoice(m.chat.id, "temp/output.ogg", f"🎤{artist} - {title}🎼\n\n🆔👉 {Config.USERNAME}")
        
    music.remove_tag('comment')
    music.remove_tag('artist')
    music.remove_tag('lyrics')
    music.remove_tag('title')
    music.remove_tag('album')
    music.remove_tag('genre')
    music['artist'] = artist + Config.custom_tag
    music['title'] = title + Config.custom_tag
    music['album'] = album + Config.custom_tag
    music['genre'] = genre + Config.custom_tag
    music['comment'] = comment + Config.custom_tag
    music['lyrics'] = lyrics + Config.custom_tag
    music.save()
    if Config.CAPTION == "TRUE":
        caption = "✏️ Title: " + title + "\n" + "👤 Artist: " + artist + "\n" + "💽 Album: " + album + "\n" + "🎼 Genre: " + genre + "\n\n" + f"🆔👉 {Config.USERNAME}"
    else:
        caption = m.caption
    try:
        await bot.send_audio(
            chat_id=m.chat.id,
            file_name=filename + ".mp3",
            caption=caption,
            thumb=open('artwork.jpg', 'rb'),
            audio="temp/file.mp3"
        )
    except Exception as e:
        print(e)


def sendVoice(chat_id,file_name,text):
    url = "https://api.telegram.org/bot%s/sendVoice"%(Config.BOT_TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id, 'caption' : text}
    r= requests.post(url, files=files, data=data)
   
Bot.run()

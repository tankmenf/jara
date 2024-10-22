import speech_recognition as sr
from PIL import Image
import pytesseract
import discord
from discord.ext import commands
import os, random
import requests
from deep_translator import GoogleTranslator

to_translate = 'I want to translate this text'
translated = GoogleTranslator(source='auto', target='de').translate(to_translate)

recognizer = sr.Recognizer()
def recognize_speech(audio_file):
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language="ru-RU")
            return text
    except sr.UnknownValueError:
        return "Не удалось распознать речь"

def recognize_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="ru-RU")
    return text

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.command('duck')
async def duck(ctx):
    '''По команде duck возвращает фото утки'''
    print('hello')
    image_url = get_duck_image_url()
    await ctx.send(image_url)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def check(ctx):
    if ctx.message.attachments:
        text2=await ctx.send ("Подождите немного")
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            
            
            text=recognize_speech(attachment.filename)
            await text2.edit (content=text)

@bot.command()
async def translate_auto_en(ctx, *, to_translate):
    translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    await ctx.send(translated)

@bot.command()
async def translate_auto_ru(ctx, *, to_translate):
    translated = GoogleTranslator(source='auto', target='ru').translate(to_translate)
    await ctx.send(translated)

bot.run('TOKEN')

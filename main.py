import speech_recognition as sr
from PIL import Image
import pytesseract
import discord
from discord.ext import commands
import os, random
import requests
from deep_translator import GoogleTranslator
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

to_translate = 'I want to translate this text'
translated = GoogleTranslator(source='auto', target='de').translate(to_translate)

def obrabotatb_kartinky(spisok):
    np.set_printoptions(suppress=True)

    # Load the model
    model = load_model("keras_model.h5", compile=False)

    # Load the labels
    class_names = open("labels.txt", "r", encoding="UTF-8").readlines()

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open(spisok).convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    return class_name[2:]

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

@bot.command()
async def kartinka(ctx):
    if ctx.message.attachments:
        text2=await ctx.send ("Подождите немного")
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{attachment.filename}")
            
            
            text=obrabotatb_kartinky(attachment.filename)
            await text2.edit (content=text)

bot.run('TOKEN')

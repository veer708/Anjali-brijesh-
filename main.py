import os
import re
import sys
import json
import time
import aiohttp
import asyncio
import requests
import subprocess
import urllib.parse
import yt_dlp
import cloudscraper
import datetime
import ffmpeg
import logging 

from yt_dlp import YoutubeDL
import yt_dlp as youtube_dl
import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput
from pytube import YouTube
from aiohttp import web
from core import *
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# Initialize the bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

API_ID    = os.environ.get("API_ID", "24495656")
API_HASH  = os.environ.get("API_HASH", "61afcf68c6429714dd18acd07f246571")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7832919263:AAErMbCTcdG7UNDxSUGGkMbufqZLrJISyas") 

# Define aiohttp routes
routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response("https://text-leech-bot-for-render.onrender.com/")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def start_bot():
    await bot.start()
    print("Bot is up and running")

async def stop_bot():
    await bot.stop()

async def main():
    if WEBHOOK:
        # Start the web server
        app_runner = web.AppRunner(await web_server())
        await app_runner.setup()
        site = web.TCPSite(app_runner, "0.0.0.0", PORT)
        await site.start()
        print(f"Web server started on port {PORT}")

    # Start the bot
    await start_bot()

    # Keep the program running
    try:
        while True:
            await bot.polling()  # Run forever, or until interrupted
    except (KeyboardInterrupt, SystemExit):
        await stop_bot()
  
import random

# Inline keyboard for start command
keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/sanjaykagra86"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/SSC_Aspirants_7"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/SSC_Aspirants_7"),
        ],
    ]
)

# Inline keyboard for busy status
Busy = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="📞 Contact", url="https://t.me/sanjaykagra86"),
            InlineKeyboardButton(text="🛠️ Help", url="https://t.me/SSC_Aspirants_7"),
        ],
        [
            InlineKeyboardButton(text="🪄 Updates Channel", url="https://t.me/SSC_Aspirants_7"),
        ],
    ]
)

               

# Image URLs for the random image feature
image_urls = [
    "https://i.ibb.co/dpRKmmj/file-3957.jpg",
    "https://i.ibb.co/NSbPQ5n/file-3956.jpg",
    "https://i.ibb.co/Z8R4z0g/file-3962.jpg",
    "https://i.ibb.co/LtqjVy7/file-3958.jpg",
    "https://i.ibb.co/bm20zfd/file-3959.jpg",
    "https://i.ibb.co/0V0BngV/file-3960.jpg",
    "https://i.ibb.co/rQMXQjX/file-3961.jpg",
    # Add more image URLs as needed
]

@bot.on_message(filters.command('h2t'))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    # Check if user is a premium user
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text(
            "🚫 **You are not a premium user.**\n\n"
            "🔑 Please contact my admin at: **@SanjayKagra86** for subscription details."
        )
        return

    # Inform the user to send the HTML file and its name
    await message.reply_text(
        "🎉 **Welcome to the HTML to Text Converter!**\n\n"
        "Please send your **HTML file** along with your desired **file name**! 📁\n\n"
        "For example: **'myfile.html'**\n"
        "Once you send the file, we'll process it and provide a neatly formatted text file for you! ✨"
    )

    try:
        # Wait for user to send HTML file
        input_message: Message = await bot.listen(message.chat.id)
        if not input_message.document:
            await message.reply_text(
                "🚨 **Error**: You need to send a valid **HTML file**. Please send a file with the `.html` extension."
            )
            return

        html_file_path = await input_message.download()

        # Ask the user for a custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "For example: **'output'** or **'video_list'**\n\n"
            "If you're unsure, we'll default to 'output'."
        )

        # Wait for the custom file name input
        file_name_input: Message = await bot.listen(message.chat.id)
        custom_file_name = file_name_input.text.strip()

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"

        await file_name_input.delete(True)

        # Process the HTML file and extract data
        with open(html_file_path, 'r') as f:
            soup = BeautifulSoup(f, 'html.parser')
            tables = soup.find_all('table')
            if not tables:
                await message.reply_text(
                    "🚨 **Error**: No tables found in the HTML file. Please ensure the HTML file contains valid data."
                )
                return

            videos = []
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:  # Ensure there's both a name and link
                        name = cols[0].get_text().strip()
                        link = cols[1].find('a')['href']
                        videos.append(f'{name}: {link}')

        # Create and send the .txt file with the custom name
        txt_file = os.path.splitext(html_file_path)[0] + f'_{custom_file_name}.txt'
        with open(txt_file, 'w') as f:
            f.write('\n'.join(videos))

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your neatly formatted text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download and use the extracted content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

@bot.on_message(filters.command('t2t'))
async def text_to_txt(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    # Check if the user is a premium user
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text(
            "🚫 **You are not a premium user.**\n\n"
            "🔑 Please contact my admin at: **@SanjayKagra86** for subscription details."
        )
        return

    # Inform the user to send the text data and its desired file name
    await message.reply_text(
        "🎉 **Welcome to the Text to .txt Converter!**\n\n"
        "Please send the **text** you want to convert into a `.txt` file.\n\n"
        "Afterward, provide the **file name** you prefer for the .txt file (without extension)."
    )

    try:
        # Wait for the user to send the text data
        input_message: Message = await bot.listen(message.chat.id)

        # Ensure the message contains text
        if not input_message.text:
            await message.reply_text(
                "🚨 **Error**: Please send valid text data to convert into a `.txt` file."
            )
            return

        text_data = input_message.text.strip()

        # Ask the user for the custom file name
        await message.reply_text(
            "🔤 **Now, please provide the file name (without extension)**\n\n"
            "For example: **'output'** or **'document'**\n\n"
            "If you're unsure, we'll default to 'output'."
        )

        # Wait for the custom file name input
        file_name_input: Message = await bot.listen(message.chat.id)
        custom_file_name = file_name_input.text.strip()

        # If the user didn't provide a name, use the default one
        if not custom_file_name:
            custom_file_name = "output"

        await file_name_input.delete(True)

        # Create and save the .txt file with the custom name
        txt_file = os.path.join("downloads", f'{custom_file_name}.txt')
        os.makedirs(os.path.dirname(txt_file), exist_ok=True)  # Ensure the directory exists
        with open(txt_file, 'w') as f:
            f.write(text_data)

        # Send the generated text file to the user with a pretty caption
        await message.reply_document(
            document=txt_file,
            caption=f"🎉 **Here is your text file**: `{custom_file_name}.txt`\n\n"
                    "You can now download your content! 📥"
        )

        # Remove the temporary text file after sending
        os.remove(txt_file)

    except Exception as e:
        # In case of any error, send a generic error message
        await message.reply_text(
            f"🚨 **An unexpected error occurred**: {str(e)}.\nPlease try again or contact support if the issue persists."
        )

# Define paths for uploaded file and processed file
UPLOAD_FOLDER = '/path/to/upload/folder'
EDITED_FILE_PATH = '/path/to/save/edited_output.txt'

@bot.on_message(filters.command('e2t'))
async def edit_txt(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    # Check if the user is a premium user
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text(
            "🚫 **You are not a premium user.**\n\n"
            "🔑 Please contact my admin at: **@SanjayKagra86** for subscription details."
        )
        return

    # Prompt the user to upload the .txt file
    await message.reply_text(
        "🎉 **Welcome to the .txt File Editor!**\n\n"
        "Please send your `.txt` file containing subjects, links, and topics."
    )

    # Wait for the user to upload the file
    input_message: Message = await bot.listen(message.chat.id)
    if not input_message.document:
        await message.reply_text("🚨 **Error**: Please upload a valid `.txt` file.")
        return

    # Get the file name
    file_name = input_message.document.file_name.lower()

    # Define the path where the file will be saved
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, file_name)

    # Download the file
    uploaded_file = await input_message.download(uploaded_file_path)

    # After uploading the file, prompt the user for the file name or 'd' for default
    await message.reply_text(
        "🔄 **Send your .txt file name, or type 'd' for the default file name.**"
    )

    # Wait for the user's response
    user_response: Message = await bot.listen(message.chat.id)
    if user_response.text:
        user_response_text = user_response.text.strip().lower()
        if user_response_text == 'd':
            # Handle default file name logic (e.g., use the original file name)
            final_file_name = file_name
        else:
            final_file_name = user_response_text + '.txt'
    else:
        final_file_name = file_name  # Default to the uploaded file name

    # Read and process the uploaded file
    try:
        with open(uploaded_file, 'r', encoding='utf-8') as f:
            content = f.readlines()
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to read the file.\n\nDetails: {e}")
        return

    # Parse the content into subjects with links and topics
    subjects = {}
    current_subject = None
    for line in content:
        line = line.strip()
        if line and ":" in line:
            # Split the line by the first ":" to separate title and URL
            title, url = line.split(":", 1)
            title, url = title.strip(), url.strip()

            # Add the title and URL to the dictionary
            if title in subjects:
                subjects[title]["links"].append(url)
            else:
                subjects[title] = {"links": [url], "topics": []}

            # Set the current subject
            current_subject = title
        elif line.startswith("-") and current_subject:
            # Add topics under the current subject
            subjects[current_subject]["topics"].append(line.strip("- ").strip())

    # Sort the subjects alphabetically and topics within each subject
    sorted_subjects = sorted(subjects.items())
    for title, data in sorted_subjects:
        data["topics"].sort()

    # Save the edited file to the defined path with the final file name
    try:
        final_file_path = os.path.join(UPLOAD_FOLDER, final_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            for title, data in sorted_subjects:
                # Write title and its links
                for link in data["links"]:
                    f.write(f"{title}:{link}\n")
                # Write topics under the title
                for topic in data["topics"]:
                    f.write(f"- {topic}\n")
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to write the edited file.\n\nDetails: {e}")
        return

    # Send the sorted and edited file back to the user
    try:
        await message.reply_document(
            document=final_file_path,
            caption="🎉 **Here is your edited .txt file with subjects, links, and topics sorted alphabetically!**"
        )
    except Exception as e:
        await message.reply_text(f"🚨 **Error**: Unable to send the file.\n\nDetails: {e}")
    finally:
        # Clean up the temporary file
        if os.path.exists(uploaded_file_path):
            os.remove(uploaded_file_path)

from pytube import Playlist
import youtube_dl

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def read_subscription_data():
    """
    Reads subscription data from a JSON file to verify premium users.
    """
    try:
        with open("subscription_data.json", "r") as file:
            return json.load(file)  # Expected format: [["user_id", "expiry_date"], ...]
    except FileNotFoundError:
        return []

def sanitize_filename(name):
    """
    Sanitizes a string to create a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_playlist_videos(playlist_url):
    """
    Retrieves video titles and URLs from a YouTube playlist.
    """
    try:
        playlist = Playlist(playlist_url)
        playlist_title = playlist.title
        videos = {video.title: video.watch_url for video in playlist.videos}
        return playlist_title, videos
    except Exception as e:
        logging.error(f"Error retrieving playlist videos: {e}")
        return None, None

def get_channel_videos(channel_url):
    """
    Retrieves video titles and URLs from a YouTube channel.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            if 'entries' in result:
                channel_name = result['title']
                videos = {entry['title']: entry['url'] for entry in result['entries'] if 'url' in entry}
                return videos, channel_name
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving channel videos: {e}")
        return None, None

def save_to_file(videos, name):
    """
    Saves video titles and URLs to a .txt file.
    """
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            formatted_url = url if url.startswith("https://") else f"https://www.youtube.com/watch?v={url}"
            file.write(f"{title}: {formatted_url}\n")
    return filename

# --- Bot Command ---

@bot.on_message(filters.command('yt2t'))
async def ytplaylist_to_txt(client: Client, message: Message):
    """
    Handles the extraction of YouTube playlist/channel videos and sends a .txt file.
    """
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    # Verify premium user
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text(
            "🚫 **You are not a premium user.**\n\n"
            "🔑 Please contact my admin at: **@SanjayKagra86** for subscription details."
        )
        return

    # Request YouTube URL
    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist or Channel URL:**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    # Process the URL
    if 'playlist' in youtube_url:
        playlist_title, videos = get_playlist_videos(youtube_url)
        if videos:
            file_name = save_to_file(videos, playlist_title)
            await message.reply_document(
                document=file_name, 
                caption=f"🎉 **Here is the text file with titles and URLs of the playlist:** `{playlist_title}`"
            )
            os.remove(file_name)
        else:
            await message.reply_text("⚠️ **Unable to retrieve the playlist. Please check the URL.**")
    else:
        videos, channel_name = get_channel_videos(youtube_url)
        if videos:
            file_name = save_to_file(videos, channel_name)
            await message.reply_document(
                document=file_name, 
                caption=f"🎉 **Here is the text file with titles and URLs of the channel:** `{channel_name}`"
            )
            os.remove(file_name)
        else:
            await message.reply_text("⚠️ **No videos found or the URL is invalid. Please try again.**")

# --- Configuration ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# --- Utility Functions ---

def read_subscription_data():
    """
    Reads subscription data from a JSON file to verify premium users.
    """
    try:
        with open("subscription_data.json", "r") as file:
            return json.load(file)  # Expected format: [["user_id", "expiry_date"], ...]
    except FileNotFoundError:
        return []

def sanitize_filename(name):
    """
    Sanitizes a string to create a valid filename.
    """
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '_')

def get_videos_with_ytdlp(url):
    """
    Retrieves video titles and URLs using `yt-dlp`.
    If a title is not available, only the URL is saved.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'skip_download': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=False)
            if 'entries' in result:
                title = result.get('title', 'Unknown Title')
                videos = {}
                for entry in result['entries']:
                    video_url = entry.get('url', None)
                    video_title = entry.get('title', None)
                    if video_url:
                        videos[video_title if video_title else "Unknown Title"] = video_url
                return title, videos
            return None, None
    except Exception as e:
        logging.error(f"Error retrieving videos: {e}")
        return None, None

def save_to_file(videos, name):
    """
    Saves video titles and URLs to a .txt file.
    If a title is unavailable, only the URL is saved.
    """
    filename = f"{sanitize_filename(name)}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        for title, url in videos.items():
            if title == "Unknown Title":
                file.write(f"{url}\n")
            else:
                file.write(f"{title}: {url}\n")
    return filename

# --- Bot Command ---

@bot.on_message(filters.command('yt2txt'))
async def ytplaylist_to_txt(client: Client, message: Message):
    """
    Handles the extraction of YouTube playlist/channel videos and sends a .txt file.
    """
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    # Verify premium user
    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text(
            "🚫 **You are not a premium user.**\n\n"
            "🔑 Please contact my admin at: **@SanjayKagra86** for subscription details."
        )
        return

    # Request YouTube URL
    await message.delete()
    editable = await message.reply_text("📥 **Please enter the YouTube Playlist or Channel URL:**")
    input_msg = await client.listen(editable.chat.id)
    youtube_url = input_msg.text
    await input_msg.delete()
    await editable.delete()

    # Process the URL
    title, videos = get_videos_with_ytdlp(youtube_url)
    if videos:
        file_name = save_to_file(videos, title)
        await message.reply_document(
            document=file_name, 
            caption=f"🎉 **Here is the text file with titles and URLs:** `{title}`"
        )
        os.remove(file_name)
    else:
        await message.reply_text("⚠️ **Unable to retrieve videos. Please check the URL.**")

# Start command handler
@bot.on_message(filters.command(["start"]))
async def start_command(bot: Client, message: Message):
    # Send a loading message
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Loading... ⏳🔄"
    )
  
    # Choose a random image URL
    random_image_url = random.choice(image_urls)
    
    # Caption for the image
    caption = (
        "**𝐇𝐞𝐥𝐥𝐨 𝐃𝐞𝐚𝐫 👋!**\n\n"
        "➠ **𝐈 𝐚𝐦 𝐚 𝐓𝐞𝐱𝐭 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭 𝐌𝐚𝐝𝐞 𝐖𝐢𝐭𝐡 ♥️**\n"
        "➠ **Can Extract Videos & PDFs From Your Text File and Upload to Telegram!**\n"
        "➠ **For Guide Use Command /guide 📖**\n\n"
        "➠ **Use /moni Command to Download From TXT File** 📄\n\n"
        "➠ **𝐌𝐚𝐝𝐞 𝐁𝐲:** @SanjayKagra86🩷"
    )

    # Send the image with caption and buttons
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=random_image_url,
        caption=caption,
        reply_markup=keyboard
    )

    # Delete the loading message
    await loading_message.delete()

# Retrieve the cookies file path from the environment variable or set the default path
COOKIES_FILE_PATH = os.getenv("COOKIES_FILE_PATH", "youtube_cookies.txt")
ADMIN_ID = 5548106944  # Admin ID for restricting the command

@bot.on_message(filters.command("cookies") & filters.private)
async def cookies_handler(client: Client, m: Message):
    """
    Command: /cookies
    Allows the admin to upload or update the cookies file dynamically.
    """
    # Check if the user is the admin 🛑
    if m.from_user.id != ADMIN_ID:
        await m.reply_text("🚫 You are not authorized to use this command.")
        return

    await m.reply_text(
        "📂 Please upload the cookies file in .txt format. 📄",
        quote=True
    )

    try:
        # Wait for the admin to send the cookies file ⏳
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file type (it should be a .txt file) ✅
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("❌ Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file to the specified path 💾
        cookies_path = await input_message.download(file_name=COOKIES_FILE_PATH)

        # Read the cookies data from the uploaded file 📑
        with open(cookies_path, 'r') as file:
            cookies_data = file.read()  # Read the cookies data

        # Save the cookies data into youtube_cookies.txt 📝
        with open("youtube_cookies.txt", 'w') as file:
            file.write(cookies_data)  # Overwrite the old cookies with new data

        await input_message.reply_text(
            f"✅ Cookies file has been successfully updated.\n📂 Saved at: `{COOKIES_FILE_PATH}`"
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")


# Retrieve the cookies file path from the environment variable or set the default path
INSTAGRAM_COOKIES_PATH = os.getenv("INSTAGRAM_COOKIES_PATH", "instagram_cookies.txt")
ADMIN_ID = 5548106944  # Admin ID for restricting the command

@bot.on_message(filters.command("instacookies") & filters.private)
async def instacookies_handler(client: Client, m: Message):
    """
    Command: /instacookies
    Allows the admin to upload or update the Instagram cookies file dynamically.
    """
    # Check if the user is the admin 🛑
    if m.from_user.id != ADMIN_ID:
        await m.reply_text("🚫 You are not authorized to use this command.")
        return

    await m.reply_text(
        "📂 Please upload the Instagram cookies file in .txt format. 📄",
        quote=True
    )

    try:
        # Wait for the admin to send the cookies file ⏳
        input_message: Message = await client.listen(m.chat.id)

        # Validate the uploaded file type (it should be a .txt file) ✅
        if not input_message.document or not input_message.document.file_name.endswith(".txt"):
            await m.reply_text("❌ Invalid file type. Please upload a .txt file.")
            return

        # Download the cookies file to the specified path 💾
        cookies_path = await input_message.download(file_name=INSTAGRAM_COOKIES_PATH)

        # Read the cookies data from the uploaded file 📑
        with open(cookies_path, 'r') as file:
            cookies_data = file.read()  # Read the cookies data

        # Save the cookies data into the Instagram cookies file 📝
        with open(INSTAGRAM_COOKIES_PATH, 'w') as file:
            file.write(cookies_data)  # Overwrite the old cookies with new data

        await input_message.reply_text(
            f"✅ Instagram cookies file has been successfully updated.\n📂 Saved at: `{INSTAGRAM_COOKIES_PATH}`"
        )

    except Exception as e:
        await m.reply_text(f"⚠️ An error occurred: {str(e)}")

import json
import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message

# File paths
SUBSCRIPTION_FILE = "subscription_data.txt"
CHANNELS_FILE = "channels_data.json"

# Admin ID
ADMIN_ID = 5548106944

# Function to read subscription data
def read_subscription_data():
    if not os.path.exists(SUBSCRIPTION_FILE):
        return []
    try:
        with open(SUBSCRIPTION_FILE, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    except Exception as error:
        print(f"Error reading subscription data: {error}")
        return []

# Function to read channels data
def read_channels_data():
    if not os.path.exists(CHANNELS_FILE):
        return []
    try:
        with open(CHANNELS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Channels data contains invalid JSON format.")
        return []
    except Exception as error:
        print(f"Error reading channels data: {error}")
        return []

# Function to write subscription data
def write_subscription_data(data):
    try:
        with open(SUBSCRIPTION_FILE, "w") as file:
            for user in data:
                file.write(",".join(user) + "\n")
    except Exception as error:
        print(f"Error writing subscription data: {error}")

# Function to write channels data
def write_channels_data(data):
    try:
        with open(CHANNELS_FILE, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as error:
        print(f"Error writing channels data: {error}")

# Admin-only decorator
def admin_only(func):
    async def wrapper(client, message: Message):
        if message.from_user.id != ADMIN_ID:
            await message.reply_text("❌ You are not authorized to use this command. Please contact the admin.")
            return
        await func(client, message)
    return wrapper

#=================== GUIDE FOR USERS =====================

@bot.on_message(filters.command("guide"))
async def guide_handler(client: Client, message: Message):
    guide_text = (
        "🌟 **Welcome to the Bot Guide** 🌟\n\n"
        "🔑 **How to Get Started with Premium**:\n\n"
        "1️⃣ Contact the owner to buy a premium plan. 💰\n"
        "2️⃣ Once you're a premium user, check your plan anytime with `/myplan`. 🔍\n\n"
        "📖 **Premium User Commands**:\n\n"
        "1️⃣ `/h2t` - Convert an **HTML file** to a **TXT file**. 📄➡️📜\n"
        "2️⃣ `/t2t` - Convert plain **text** into a **TXT file**. ✍️➡️📜\n"
        "3️⃣ `/e2t` - Filter your **TXT file** and extract important details. 🔍📜\n"
        "4️⃣ `/yt2t` - Convert a **YouTube playlist URL** into a **TXT file**. (Not Working Properly ❌)\n"
        "5️⃣ `/yt2txt` - Convert a **YouTube playlist URL** into a **TXT file** (Recommended ✅).\n"
        "6️⃣ `/moni` - Process a `.txt` file with advanced logic. 📂📜\n"
        "   *(Note: Use this command in channels or groups for proper functionality.)*\n"
        "7️⃣ `/add_channel -100{channel_id}` - Add a channel to the bot. ➕📢\n"
        "8️⃣ `/remove_channel -100{channel_id}` - Remove a channel from the bot. ❌📢\n"
        "9️⃣ `/stop` - Stop the bot's current task. 🚫\n"
        "   *(Note: Use this command in channels or groups for proper functionality.)*\n"
        "🔟 `/id` - Get your user ID. 🆔\n"
        "1️⃣1️⃣ `/myplan` - View your active premium plan and details. 📋\n\n"
        "⚙️ **Admin Commands**:\n\n"
        "1️⃣ `/adduser` - Add a user to the premium list. ➕👤\n"
        "2️⃣ `/removeuser` - Remove a user from the premium list. ❌👤\n"
        "3️⃣ `/allowed_channels` - List all channels allowed for the bot. 📃\n"
        "4️⃣ `/cookies` - Manage cookies for browser-based operations. 🍪\n"
        "5️⃣ `/instacookies` - Add or update cookies for Instagram tasks. 📸🍪\n\n"
        "💡 **General Tips**:\n\n"
        "✨ Use these commands as instructed for the best experience.\n"
        "✨ Admin commands require proper permissions.\n"
        "✨ If you face any issues, contact the bot owner for assistance. 💬\n\n"
        "🤔 **Still have questions?** Feel free to ask! 💡"
    )
    await message.reply_text(guide_text)


#=================== USER COMMANDS =====================

# 1. /adduser - Add a new user to subscription
@bot.on_message(filters.command("adduser") & filters.private)
@admin_only
async def add_user(client, message: Message):
    try:
        _, user_id, expiration_date = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data.append([user_id, expiration_date])
        write_subscription_data(subscription_data)
        await message.reply_text(f"🎉 **User {user_id} added!**\n📅 **Expiration Date**: {expiration_date}")
    except ValueError:
        await message.reply_text("❌ **Invalid command format.**\nUse: `/adduser <user_id> <expiration_date>`")

# 2. /removeuser - Remove a user from subscription
@bot.on_message(filters.command("removeuser") & filters.private)
@admin_only
async def remove_user(client, message: Message):
    try:
        _, user_id = message.text.split()
        subscription_data = read_subscription_data()
        subscription_data = [user for user in subscription_data if user[0] != user_id]
        write_subscription_data(subscription_data)
        await message.reply_text(f"🚫 **User {user_id} removed!**")
    except ValueError:
        await message.reply_text("❌ **Invalid command format.**\nUse: `/removeuser <user_id>`")

# 3. /myplan - Show user's subscription plan
@bot.on_message(filters.command("myplan") & filters.private)
async def my_plan(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if user_id == str(ADMIN_ID):
        await message.reply_text("✨ **You have permanent access!**\nYou are the admin. 💎")
    elif any(user[0] == user_id for user in subscription_data):
        expiration_date = next(user[1] for user in subscription_data if user[0] == user_id)
        await message.reply_text(
            f"**📅 Your Premium Plan Status**\n\n"
            f"🆔 **User ID**: `{user_id}`\n"
            f"⏳ **Expiration Date**: `{expiration_date}`\n"
            f"🔒 **Status**: *Active*"
        )
    else:
        await message.reply_text("❌ **You are not a premium user.**\nPlease upgrade your plan. 💳")

ADMIN_ID = 5548106944

# Helper function to check admin privilege
def is_admin(user_id):
    return user_id == ADMIN_ID

# Command to show all users (Admin only)
@bot.on_message(filters.command("users") & filters.private)
async def show_users(client, message: Message):
    user_id = message.from_user.id

    # Check if the user is the admin
    if not is_admin(user_id):
        await message.reply_text("❌ You are not authorized to use this command.")
        return

    # Read subscription data
    subscription_data = read_subscription_data()

    # Check if there are any users in the subscription data
    if subscription_data:
        # Prepare the header and user details without markdown formatting
        users_list = "\n".join(
            [f"{idx + 1}.\n"
             f"User ID: {user[0]}\n"
             f"Expiration Date: {user[1]}\n"
             f"———"  # Separator for better readability
             for idx, user in enumerate(subscription_data)]
        )

        # Send the list to the admin
        await message.reply_text(
            f"👥 Current Subscribed Users:\n\n{users_list}"
        )
    else:
        await message.reply_text("ℹ️ No users found in the subscription data.")

# 4. /add_channel - Add channel to the user's allowed list
@bot.on_message(filters.command("add_channel"))
async def add_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("🚫 **You are not a premium user.**\nPlease subscribe first.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id not in channels:
            channels.append(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"✅ **Channel {channel_id} added!**")
        else:
            await message.reply_text(f"❗ **Channel {channel_id} is already added.**")
    except ValueError:
        await message.reply_text("❌ **Invalid command format.**\nUse: `/add_channel <channel_id>`")

# 5. /remove_channel - Remove channel from the user's allowed list
@bot.on_message(filters.command("remove_channel"))
async def remove_channel(client, message: Message):
    user_id = str(message.from_user.id)
    subscription_data = read_subscription_data()

    if not any(user[0] == user_id for user in subscription_data):
        await message.reply_text("🚫 **You are not a premium user.**\nPlease subscribe first.")
        return

    try:
        _, channel_id = message.text.split()
        channels = read_channels_data()
        if channel_id in channels:
            channels.remove(channel_id)
            write_channels_data(channels)
            await message.reply_text(f"❌ **Channel {channel_id} removed.**")
        else:
            await message.reply_text(f"⚠️ **Channel {channel_id} not found.**")
    except ValueError:
        await message.reply_text("❌ **Invalid command format.**\nUse: `/remove_channel <channel_id>`")

#=================== ADMIN COMMANDS =====================

# /id Command - Show Group/Channel ID
@bot.on_message(filters.command("id"))
async def id_command(client, message: Message):
    chat_id = message.chat.id
    await message.reply_text(
        f"🎉 **Success!**\n\n"
        f"🆔 **This Group/Channel ID:**\n`{chat_id}`\n\n"
        f"📌 **Use this ID for further requests.**\n\n"
        f"🔗 To link this group/channel, use the following command:\n"
        f"`/add_channel {chat_id}`"
    )

# /allowed_channels - Show all allowed channels (Admin only)
@bot.on_message(filters.command("allowed_channels"))
async def allowed_channels(client, message: Message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        await message.reply_text("❌ **You are not authorized to use this command.**")
        return

    channels = read_channels_data()
    if channels:
        channels_list = "\n".join([f"📱 - {channel}" for channel in channels])
        await message.reply_text(f"**📋 Allowed Channels:**\n\n{channels_list}")
    else:
        await message.reply_text("ℹ️ **No channels are currently allowed.**")

# /remove_all_channels - Remove all channels (Admin only)
@bot.on_message(filters.command("remove_all_channels"))
async def remove_all_channels(client, message: Message):
    user_id = message.from_user.id

    if user_id != ADMIN_ID:
        await message.reply_text("❌ **You are not authorized to use this command.**")
        return

    write_channels_data([])
    await message.reply_text("✅ **All channels have been removed successfully.**")

# 6. /stop - Stop the bot process
@bot.on_message(filters.command("stop"))
async def stop_handler(client, message: Message):
    if message.chat.type == "private":
        user_id = str(message.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await message.reply_text("😔 **You are not a premium user.**\nPlease subscribe to get access! 🔒")
            return
    else:
        channels = read_channels_data()
        if str(message.chat.id) not in channels:
            await message.reply_text("🚫 **You are not a premium user.**\nSubscribe to unlock all features! ✨")
            return

    await message.reply_text("♦️ **Bot Stopped.** Restarting now...", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

# 7. /moni - Moni handler for premium users
@bot.on_message(filters.command("moni"))
async def moni_handler(client: Client, m: Message):
    if m.chat.type == "private":
        user_id = str(m.from_user.id)
        subscription_data = read_subscription_data()
        if not any(user[0] == user_id for user in subscription_data):
            await m.reply_text("❌ **You are not a premium user.**\nPlease upgrade your subscription! 💎")
            return
    else:
        channels = read_channels_data()
        if str(m.chat.id) not in channels:
            await m.reply_text("❗ **You are not a premium user.**\nSubscribe now for exclusive access! 🚀")
            return

    editable = await m.reply_text('💾 **To Download a .txt File, Send Here ⏍**')      

    try:
        input: Message = await client.listen(editable.chat.id)
        
        # Check if the message contains a document and is a .txt file
        if not input.document or not input.document.file_name.endswith('.txt'):
            await m.reply_text("Please send a valid .txt file.")
            return

        # Download the file
        x = await input.download()
        await input.delete(True)

        path = f"./downloads/{m.chat.id}"
        file_name = os.path.splitext(os.path.basename(x))[0]

        # Read and process the file
        with open(x, "r") as f:
            content = f.read().strip()

        lines = content.splitlines()
        links = []

        for line in lines:
            line = line.strip()
            if line:
                link = line.split("://", 1)
                if len(link) > 1:
                    links.append(link)
                    
        os.remove(x)
        print(len(links))

    except:
        await m.reply_text("∝ 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐟𝐢𝐥𝐞 𝐢𝐧𝐩𝐮𝐭.")
        if os.path.exists(x):
            os.remove(x)

    await editable.edit(f"∝ 𝐓𝐨𝐭𝐚𝐥 𝐋𝐢𝐧𝐤 𝐅𝐨𝐮𝐧𝐝 𝐀𝐫𝐞 🔗** **{len(links)}**\n\n𝐒𝐞𝐧𝐝 𝐅𝐫𝐨𝐦 𝐖𝐡𝐞𝐫𝐞 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐓𝐨 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐈𝐧𝐢𝐭𝐚𝐥 𝐢𝐬 **1**")
    input0: Message = await bot.listen(editable.chat.id)
    raw_text = input0.text
    await input0.delete(True)               

    # This is where you would set up your bot and connect the handle_command function      
    await editable.edit("**Enter Batch Name or send d for grabing from text filename.**")
    input1: Message = await bot.listen(editable.chat.id)
    raw_text0 = input1.text
    await input1.delete(True)
    if raw_text0 == 'd':
        b_name = file_name
    else:
        b_name = raw_text0
        
    await editable.edit("∝ 𝐄𝐧𝐭𝐞𝐫 𝐄𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝐨𝐧 🎬\n☞ 144,240,360,480,720,1080\nPlease Choose Quality")
    input2: Message = await bot.listen(editable.chat.id)
    raw_text2 = input2.text
    await input2.delete(True)
    try:
        if raw_text2 == "144":
            res = "256x144"
        elif raw_text2 == "240":
            res = "426x240"
        elif raw_text2 == "360":
            res = "640x360"
        elif raw_text2 == "480":
            res = "854x480"
        elif raw_text2 == "720":
            res = "1280x720"
        elif raw_text2 == "1080":
            res = "1920x1080" 
        else: 
            res = "UN"
    except Exception:
            res = "UN"
    
    

    await editable.edit("**Enter Your Name or send `de` for use default**")

    # Listen for the user's response
    input3: Message = await bot.listen(editable.chat.id)

    # Get the raw text from the user's message
    raw_text3 = input3.text

    # Delete the user's message after reading it
    await input3.delete(True)

    # Default credit message
    credit = "️ ⁪⁬⁮⁮⁮"
    if raw_text3 == 'de':
        CR = '@SanjayKagra86🩷'
    elif raw_text3:
        CR = raw_text3
    else:
        CR = credit
   
    await editable.edit("🌄 Now send the Thumb url if don't want thumbnail send no ")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    await input6.delete(True)
    await editable.delete()

    thumb = input6.text
    if thumb.startswith("http://") or thumb.startswith("https://"):
        getstatusoutput(f"wget '{thumb}' -O 'thumb.jpg'")
        thumb = "thumb.jpg"
    else:
        thumb == "no"

    if len(links) == 1:
        count = 1
    else:
        count = int(raw_text)

    try:
        # Assuming links is a list of lists and you want to process the second element of each sublist
        for i in range(count - 1, len(links)):

            # Replace parts of the URL as needed
            V = links[i][1].replace("file/d/","uc?export=download&id=")\
               .replace("www.youtube-nocookie.com/embed", "youtu.be")\
               .replace("?modestbranding=1", "")\
               .replace("/view?usp=sharing","")\
               .replace("youtube.com/embed/", "youtube.com/watch?v=")
            
            url = "https://" + V
            
            if "acecwply" in url:
                cmd = f'yt-dlp -o "{name}.%(ext)s" -f "bestvideo[height<={raw_text2}]+bestaudio" --hls-prefer-ffmpeg --no-keep-video --remux-video mkv --no-warning "{url}"'
                

            if "visionias" in url:
                async with ClientSession() as session:
                    async with session.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Accept-Language': 'en-US,en;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Pragma': 'no-cache', 'Referer': 'http://www.visionias.in/', 'Sec-Fetch-Dest': 'iframe', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'cross-site', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Linux; Android 12; RMX2121) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Mobile Safari/537.36', 'sec-ch-ua': '"Chromium";v="107", "Not=A?Brand";v="24"', 'sec-ch-ua-mobile': '?1', 'sec-ch-ua-platform': '"Android"',}) as resp:
                        text = await resp.text()
                        url = re.search(r"(https://.*?playlist.m3u8.*?)\"", text).group(1)

            elif 'classplusapp' in url:
                headers = {
                    'Host': 'api.classplusapp.com',
                    'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9',
                    'user-agent': 'Mobile-Android',
                    'app-version': '1.4.37.1',
                    'api-version': '18',
                    'device-id': '5d0d17ac8b3c9f51',
                    'device-details':'2848b866799971ca_2848b8667a33216c_SDK-30',
                    'accept-encoding': 'gzip, deflate'
                }
                
                params = (('url', f'{url}'), )
                response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)                
                url = response.json()['url']

            elif "tencdn.classplusapp" in url or "media-cdn-alisg.classplusapp.com" in url or "media-cdn.classplusapp" in url:
             headers = {'Host': 'api.classplusapp.com', 'x-access-token': 'eyJjb3Vyc2VJZCI6IjQ1NjY4NyIsInR1dG9ySWQiOm51bGwsIm9yZ0lkIjo0ODA2MTksImNhdGVnb3J5SWQiOm51bGx9', 'user-agent': 'Mobile-Android', 'app-version': '1.4.37.1', 'api-version': '18', 'device-id': '5d0d17ac8b3c9f51', 'device-details': '2848b866799971ca_2848b8667a33216c_SDK-30', 'accept-encoding': 'gzip'}
             params = (('url', f'{url}'),)
             response = requests.get('https://api.classplusapp.com/cams/uploader/video/jw-signed-url', headers=headers, params=params)
             url = response.json()['url']
            
            # Handle master.mpd URLs
            elif '/master.mpd' in url:
                id = url.split("/")[-2]
                url = "https://d26g5bnklkwsh4.cloudfront.net/" + id + "/master.m3u8"

            # Sanitizing the name
            name1 = links[i][0].replace("\t", "").replace(":", "").replace("/", "").replace("+", "").replace("#", "").replace("|", "").replace("@", "").replace("*", "").replace(".", "").replace("https", "").replace("http", "").strip()
            name = f'{str(count).zfill(3)}) {name1[:60]}'

            # For master.mpd, handle m3u8 URL download
            if "/master.mpd" in url:
                if "https://sec1.pw.live/" in url:
                    url = url.replace("https://sec1.pw.live/", "https://d1d34p8vz63oiq.cloudfront.net/")

                # Command to download m3u8 file
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'
                subprocess.run(cmd, shell=True)
                
            if "edge.api.brightcove.com" in url:
                bcov = 'bcov_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MjQyMzg3OTEsImNvbiI6eyJpc0FkbWluIjpmYWxzZSwiYXVzZXIiOiJVMFZ6TkdGU2NuQlZjR3h5TkZwV09FYzBURGxOZHowOSIsImlkIjoiZEUxbmNuZFBNblJqVEROVmFWTlFWbXhRTkhoS2R6MDkiLCJmaXJzdF9uYW1lIjoiYVcxV05ITjVSemR6Vm10ak1WUlBSRkF5ZVNzM1VUMDkiLCJlbWFpbCI6Ik5Ga3hNVWhxUXpRNFJ6VlhiR0ppWTJoUk0wMVdNR0pVTlU5clJXSkRWbXRMTTBSU2FHRnhURTFTUlQwPSIsInBob25lIjoiVUhVMFZrOWFTbmQ1ZVcwd1pqUTViRzVSYVc5aGR6MDkiLCJhdmF0YXIiOiJLM1ZzY1M4elMwcDBRbmxrYms4M1JEbHZla05pVVQwOSIsInJlZmVycmFsX2NvZGUiOiJOalZFYzBkM1IyNTBSM3B3VUZWbVRtbHFRVXAwVVQwOSIsImRldmljZV90eXBlIjoiYW5kcm9pZCIsImRldmljZV92ZXJzaW9uIjoiUShBbmRyb2lkIDEwLjApIiwiZGV2aWNlX21vZGVsIjoiU2Ftc3VuZyBTTS1TOTE4QiIsInJlbW90ZV9hZGRyIjoiNTQuMjI2LjI1NS4xNjMsIDU0LjIyNi4yNTUuMTYzIn19.snDdd-PbaoC42OUhn5SJaEGxq0VzfdzO49WTmYgTx8ra_Lz66GySZykpd2SxIZCnrKR6-R10F5sUSrKATv1CDk9ruj_ltCjEkcRq8mAqAytDcEBp72-W0Z7DtGi8LdnY7Vd9Kpaf499P-y3-godolS_7ixClcYOnWxe2nSVD5C9c5HkyisrHTvf6NFAuQC_FD3TzByldbPVKK0ag1UnHRavX8MtttjshnRhv5gJs5DQWj4Ir_dkMcJ4JaVZO3z8j0OxVLjnmuaRBujT-1pavsr1CCzjTbAcBvdjUfvzEhObWfA1-Vl5Y4bUgRHhl1U-0hne4-5fF0aouyu71Y6W0eg'
                url = url.split("bcov_auth")[0]+bcov

            if "instagram.com" in url:
                if "/reel/" in url or "/p/" in url or "/tv/" in url:
                    cmd = f'yt-dlp --cookies "{INSTAGRAM_COOKIES_PATH}" -o "{name}.mp4" "{url}"'
                    subprocess.run(cmd, shell=True)
               
            if "youtu" in url:
                ytf = f"b[height<={raw_text2}][ext=mp4]/bv[height<={raw_text2}][ext=mp4]+ba[ext=m4a]/b[ext=mp4]"
            else:
                ytf = f"b[height<={raw_text2}]/bv[height<={raw_text2}]+ba/b/bv+ba"
            
            if "jw-prod" in url:
                cmd = f'yt-dlp -o "{name}.mp4" "{url}"'

            if "embed" in url:
                ytf = f"bestvideo[height<={raw_text2}]+bestaudio/best[height<={raw_text2}]"
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
           
            elif "youtube.com" in url or "youtu.be" in url:
                cmd = f'yt-dlp --cookies "{COOKIES_FILE_PATH}" -f "{ytf}" "{url}" -o "{name}.mp4"'

            else:
                cmd = f'yt-dlp -f "{ytf}" "{url}" -o "{name}.mp4"'
        
                
            try:                
                cc = f'**🎥 VIDEO ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} {res} ⎳𝓸𝓿𝓮❥❤️━━╬٨ﮩSanju٨ـﮩـ Love❥.mkv\n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                cc1 = f'**📁 FILE ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} 𝄟✮͢🦋⃟≛⃝m✮⃝oni.pdf \n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                cc2 = f'**📁 FILE ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} 𝄟✮͢🦋⃟≛⃝m✮⃝oni.html \n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                cc3 = f'**📷 IMAGE ID: {str(count).zfill(3)}.\n\n📄 Title: {name1} 𝄟✮͢🦋⃟≛⃝m✮⃝oni.png \n\n<pre><code>🔖 Batch Name: {b_name}</code></pre>\n\n📥 Extracted By : {CR}**'
                                                 
                if "drive" in url:
                    try:
                        ka = await helper.download(url, name)
                        copy = await bot.send_document(chat_id=m.chat.id,document=ka, caption=cc1)
                        count+=1
                        os.remove(ka)
                        time.sleep(1)
                    except FloodWait as e:
                        await m.reply_text(str(e))
                        time.sleep(2)
                        continue
                
                elif ".pdf" in url:
                    try:
                        await asyncio.sleep(2)
                        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")
 
                        # Create a cloudscraper session
                        scraper = cloudscraper.create_scraper()

                        # Send a GET request to download the PDF
                        response = scraper.get(url)

                        # Check if the response status is OK
                        if response.status_code == 200:
                            # Write the PDF content to a file
                            with open(f'{name}.pdf', 'wb') as file:
                                file.write(response.content)

                            # Send the PDF document
                            await asyncio.sleep(2)
                            copy = await bot.send_document(chat_id=m.chat.id, document=f'{name}.pdf', caption=cc1)
                            count += 1

                            # Remove the PDF file after sending
                            os.remove(f'{name}.pdf')
                        else:
                            await m.reply_text(f"Failed to download PDF: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        return  # Exit the function to avoid continuation

                # Handling .ws URLs
                elif ".ws" in url:
                    try:
                        await asyncio.sleep(2)
                        url = url.replace(" ", "%20")
                        scraper = cloudscraper.create_scraper()
                        response = scraper.get(url)
                        response.encoding = 'utf-8'
                        

                        if response.status_code == 200:
                            # Sanitize file name
                            import re
                            safe_name = name.replace(' ', '_')  # Replace spaces with underscores
                            # safe_name = re.sub(r'[^\w\s-]', '', name)  # Remove unsafe characters
                            # safe_name = safe_name.strip().replace(' ', '_')  # Replace spaces with underscores
                            file_path = f"{safe_name}.html"

                            # Write response content to HTML file
                            with open(file_path, "w", encoding="utf-8") as file:
                                file.write(response.text)

                            # Parse and clean content
                            from bs4 import BeautifulSoup
                            with open(file_path, "r", encoding="utf-8") as file:
                                soup = BeautifulSoup(file.read(), "html.parser")
                            clean_text = ' '.join(soup.get_text().split())

                            # Send the cleaned file or use further
                            await asyncio.sleep(2)
                            copy = await bot.send_document(chat_id=m.chat.id, document=file_path, caption=cc2)
                            count += 1

                        else:
                            await m.reply_text(f"Failed to download HTML file: {response.status_code} {response.reason}")

                    except Exception as e:
                        await m.reply_text(f"Error: {str(e)}")

                    finally:
                        # Ensure file cleanup
                        if os.path.exists(file_path):
                            os.remove(file_path)
                        
            
                # Handling image formats (JPEG, PNG, etc.)
                elif any(ext in url.lower() for ext in [".jpg", ".jpeg", ".png"]):
                    try:
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        # Replace spaces with %20 in the URL
                        url = url.replace(" ", "%20")

                        # Create a cloudscraper session for image download
                        scraper = cloudscraper.create_scraper()

                        # Send a GET request to download the image
                        response = scraper.get(url)

                        # Check if the response status is OK
                        if response.status_code == 200:
                            # Write the image content to a file
                            with open(f'{name}.jpg', 'wb') as file:  # Save as JPG (or PNG if you want)
                                file.write(response.content)

                            # Send the image document
                            await asyncio.sleep(2)  # Non-blocking sleep
                            copy = await bot.send_photo(chat_id=m.chat.id, photo=f'{name}.jpg', caption=cc3)
                            count += 1

                            # Remove the image file after sending
                            os.remove(f'{name}.jpg')

                        else:
                            await m.reply_text(f"Failed to download Image: {response.status_code} {response.reason}")

                    except FloodWait as e:
                        await m.reply_text(str(e))
                        await asyncio.sleep(2)  # Use asyncio.sleep for non-blocking sleep
                        return  # Exit the function to avoid continuation

                    except Exception as e:
                        await m.reply_text(f"An error occurred: {str(e)}")
                        await asyncio.sleep(2)  # You can replace this with more specific
                        continue

            
                else:
                    # Enhanced Show message
                    Show = f"""❊⟱ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 ⟱❊ »\n\n📄 **Title:** `{name}`\n⌨ **Quality:** {raw_text2}\n"""
                
                    # Enhanced prog message
                    prog = await m.reply_text(f"""**Downloading Video...**\n\n📄 **Title:** `{name}`\n⌨ **Quality:** {raw_text2}\n\n⚡ **Bot Made By 𝄟✮͢🦋⃟≛⃝m✮⃝oni🩷**""")
               
                    res_file = await helper.download_video(url, cmd, name)
                    filename = res_file
                    await prog.delete(True)
                    await helper.send_vid(bot, m, cc, filename, thumb, name, prog)
                    count += 1
                    time.sleep(1)

            except Exception as e:
                await m.reply_text(
                    f"⌘ 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐈𝐧𝐭𝐞𝐫𝐮𝐩𝐭𝐞𝐝\n\n⌘ 𝐍𝐚𝐦𝐞 » {name}\n⌘ 𝐋𝐢𝐧𝐤 » `{url}`"
                )
                continue

    except Exception as e:
        await m.reply_text(e)
    await m.reply_text("🔰Done Boss🔰")



bot.run()
if __name__ == "__main__":
    asyncio.run(main())

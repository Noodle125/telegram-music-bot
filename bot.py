import logging
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from pydub import AudioSegment
from pydub.playback import play

from config import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your music streaming bot. Use /play <song_url> to play music.')

# Function to play music
def play_music(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text('Please provide a URL to a music file.')
        return

    url = context.args[0]
    update.message.reply_text(f'Starting to play: {url}')
    
    # Download the music file
    os.system(f'wget {url} -O music.mp3')
    
    # Convert and play the music file
    audio = AudioSegment.from_mp3('music.mp3')
    play(audio)

# Error handler
def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    updater = Updater(TOKEN)
    
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('play', play_music))
    
    dispatcher.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

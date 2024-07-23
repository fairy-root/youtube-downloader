import os
from pytubefix import YouTube
from subprocess import call, STDOUT
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ApplicationBuilder, CallbackContext
import telegram.ext.filters as filters
import tempfile

TOKEN = 'PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE'

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Send me a YouTube link to download.')

async def fetch_video_info(update: Update, context: CallbackContext) -> None:
    youtube_url = update.message.text
    fetching_message = await update.message.reply_text('Fetching information of the video...')
    context.user_data['fetching_message'] = fetching_message
    
    context.user_data['youtube_url'] = youtube_url
    
    yt = YouTube(youtube_url)
    context.user_data['yt'] = yt
    
    keyboard = [
        [InlineKeyboardButton("Video", callback_data='video')],
        [InlineKeyboardButton("Audio", callback_data='audio')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose format:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == 'video':
        context.user_data['format'] = 'video'
        yt = context.user_data['yt']
        video_streams = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc()

        seen_resolutions = set()
        unique_video_streams = []
        for stream in video_streams:
            if stream.resolution not in seen_resolutions:
                unique_video_streams.append(stream)
                seen_resolutions.add(stream.resolution)
        
        keyboard = [[InlineKeyboardButton(stream.resolution, callback_data=stream.itag)] for stream in unique_video_streams]
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text="Select resolution:", reply_markup=reply_markup)
        
    elif query.data == 'audio':
        context.user_data['format'] = 'audio'
        yt = context.user_data['yt']
        audio_streams = yt.streams.filter(only_audio=True).order_by('abr').desc()
        
        keyboard = [[InlineKeyboardButton(stream.abr, callback_data=stream.itag)] for stream in audio_streams]
        keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text="Select bitrate:", reply_markup=reply_markup)

    elif query.data == 'back':
        keyboard = [
            [InlineKeyboardButton("Video", callback_data='video')],
            [InlineKeyboardButton("Audio", callback_data='audio')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Choose format:", reply_markup=reply_markup)

    else:
        itag = int(query.data)
        yt = context.user_data['yt']
        stream = yt.streams.get_by_itag(itag)
        download_path = tempfile.mkdtemp()
        
        downloading_message = await query.edit_message_text(text="Downloading, please wait...")
        if 'fetching_message' in context.user_data:
            await context.user_data['fetching_message'].delete()
        
        context.user_data['downloading_message'] = downloading_message
        file_path = stream.download(output_path=download_path)
        
        if context.user_data['format'] == 'video' and not stream.includes_audio_track:
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            audio_file_path = audio_stream.download(output_path=download_path)
            
            output_file_path = os.path.join(download_path, yt.title + '_merged.mp4')
            
            call([
                "ffmpeg", "-i", file_path, "-i", audio_file_path,
                "-c:v", "copy", "-c:a", "aac", output_file_path
            ], stdout=open(os.devnull, 'w'), stderr=STDOUT)
            
            with open(output_file_path, 'rb') as video:
                await query.message.reply_video(video, caption=yt.title)
                
            os.remove(audio_file_path)
            os.remove(output_file_path)
        else:
            if context.user_data['format'] == 'video':
                with open(file_path, 'rb') as video:
                    await query.message.reply_video(video, caption=yt.title)
            else:
                with open(file_path, 'rb') as audio:
                    await query.message.reply_audio(audio)
        
        os.remove(file_path)
        os.rmdir(download_path)
        
        if 'downloading_message' in context.user_data:
            await context.user_data['downloading_message'].delete()

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fetch_video_info))
    application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()

if __name__ == '__main__':
    main()
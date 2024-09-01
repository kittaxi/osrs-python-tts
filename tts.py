from gtts import gTTS
import os,re,vlc,random,asyncio,concurrent.futures

# Log files
log_file_public = r'ENTER\PATH\HERE'
log_file_private = r'ENTER\PATH\HERE'

# In-memory cache for processed lines
processed_lines_cache = set()

# Generate TTS voicelines
async def generate_speech(text):
    # Regex stuff for tidying up the read line by removing the timestamp and username
    ## Original log format = HH:MM:SS USERNAME: MessageContent
    text = re.sub(r'^\d{2}:\d{2}:\d{2}\s+.*?:\s*', '', text, flags=re.MULTILINE)

    # List of languages + random selection. 
    languages = [
        'en', 'fr', 'de', 'it',
        'nl', 'ru', 'ja', 'ko',
        'zh-CN', 'fi'
    ]
    random_language = random.choice(languages)

    # Generate the speech. Regex to make a 'safe' filename
    tts = gTTS(text, lang=f'{random_language}')
    safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', text)
    sound_file = f"{safe_filename}.mp3"
    loop = asyncio.get_event_loop()

    # Save the speech
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, tts.save, sound_file)
    return sound_file

# Play audio asynchronously
async def play_audio(sound_file):
    media = vlc.MediaPlayer(sound_file)
    media.audio_set_volume(50)
    media.set_rate(1.2)
    media.play()

    # Wait for the media to start playing and wait while the media is playing
    await asyncio.sleep(0.5)
    while media.is_playing():
        await asyncio.sleep(0.1)  # Check every 100ms

    media.stop()
    media.release()

    # Slight delay for VLC to stop, then remove the audio file
    await asyncio.sleep(0.5)
    os.remove(sound_file)
    print(f"{sound_file} has been removed successfully.")

# Process a line
async def process_line(line):
    print(f"Processing line: {line}")
    
    # Generate TTS voice
    sound_file = await generate_speech(line)

    # Staggered playback for the audio after a slight delay 
    await asyncio.sleep(1)
    await play_audio(sound_file)

# Read lines from log 
async def read_new_lines(file_path):
    lines = []
    try:
        loop = asyncio.get_event_loop()
        with open(file_path, 'r') as file:
            # Read all lines 
            lines = await loop.run_in_executor(None, file.readlines)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return lines

async def process_lines_from_log():
    # Read all lines from the log file
    lines = await read_new_lines(log_file_public)
    if lines:
        # Process each lines concurrently
        for line in lines:
            line = line.strip()
            if line and line not in processed_lines_cache:
                asyncio.create_task(process_line(line))
                processed_lines_cache.add(line)  # Add to cache

async def process_lines_from_private_log():
    # Read all lines from the log file
    lines = await read_new_lines(log_file_private)
    if lines:
        # Process each lines concurrently
        for line in lines:
            line = line.strip()
            if line and line not in processed_lines_cache:
                asyncio.create_task(process_line(line))
                processed_lines_cache.add(line)  # Add to cache

# Clear the chat log files
async def format_logs():
    open(log_file_public, 'w').close()
    open(log_file_private, 'w').close()

async def main():
    await format_logs()
    
    # Loop to read and process new lines
    while True:
        await process_lines_from_log()
        await process_lines_from_private_log()
        await asyncio.sleep(0.5)  # Check for new lines every 0.5sec

# Run loop
if __name__ == "__main__":
    asyncio.run(main())
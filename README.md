# osrs-python-tts
A silly personal project for creating TTS lines from private and public chat messages.


Showcase:
https://youtu.be/zPkyO4PbhyU
<br /> <br />
## How it works

1. TTS generation using the [gTTS](https://pypi.org/project/gTTS/) module
2. TTS playback using the [python-vlc](https://pypi.org/project/python-vlc/) module
3. Chat logs generated with the [Chat Logger](https://github.com/hex-agon/chat-logger) Runelite plugin created by hex-agon
  
The chat logs are purged on every script startup to avoid silly behavior.
<br /> <br />

## Setup & use
1. Install Python 3
2. Install VLC (newest stable version)
3. Install the Python modules with `pip install gTTS` and `pip install python-vlc`
4. Get the Chat Logger plugin from Runelite plugin hub
5. Configure the Chat Logger to log **Private Chat** and **Public Chat**.
6. Edit the script's lines 5 and 6 to point to where ever your chat logs are being saved. Default locations below
     - Public chat: `%userprofile%\.runelite\chatlogs\public\latest.log`
     - Private chat: `%userprofile%\.runelite\chatlogs\private\latest.log`
9. Save and run the script.
10. Terminate with ctrl+c when you don't want to listen to robot voices anymore :)

If you want to edit the list of TTS languages, they can be found on line 17. Refer to the [module's docs](https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang) for available languages
<br /> <br />

## Known issues

Too lazy to fix these, even if they are super simple to fix, because they're very minor bugs.

1. If there are multiple chat messages with the same content (e.g. "Ty!" shown in the showcase), there will be an error with the generation process. At least one voice line should still play.
2. Related to the above, there might be some voice lines left behind with silly filenames, e.g. `___.mp3`
3. If you quit the script before all voice lines are removed, there will be mp3 files left behind.

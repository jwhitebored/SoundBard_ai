# SoundBard_ai
A lightweight Python Discord bot that joins a voice channel, listens in real time using Vosk speech recognition, detects spoken keywords, and plays corresponding audio clips through Discord voice chat.

Designed as a clean, easy-to-understand template for voice-activated Discord automation.

Features:
• Real-time speech recognition using Vosk (offline, fast, and accurate)   
• Keyword-triggered audio responses (soundboard-style)  
• Slash-command controlled (modern Discord UX)  
• Bot reports in text what it heard  
• Simple modular design that is easy to extend for:   
	-AI speech models  
	-LLM integration  
	-More complex event pipelines  
	-Server moderation tools  

# Installation Steps  
# 1. Get GitHub Files
i. Download the zipped SoundBard_ai folder from my GitHub (click code -> download zip).  
ii. Unzip to your preferred file location.

# 2.  Get Speech Recognition Model
i. Install the speech recognition model from https://alphacephei.com/vosk/models. The 40MB small English model (https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) was used during testing, but you can choose any model with your preferred speech recognition language.  
ii. Unzip the model folder, rename the folder to "model" (without quotes), and place the folder into your SoundBard_ai folder.

# 3.  Get Discord Token
Because this bot will run locally (necessary for the speech recognition model to be used for free), you have to make your own discord bot, but just follow these steps and it will be easy:
i. Go to the discord developer portal and log in: https://discord.com/developers/docs/intro
ii. Click "Applications" on the left-hand panel.
iii. Click "New Application" on the top right of the screen, name your application SoundBard_ai, and accept the terms of service.
iv. On the left-hand panel click "Bot" and scroll down to "Privileged Gateway Intents", then toggle-on the following intents:  
• Presence Intent  
• Server Members Intent  
• Message Content Intent  

Now scroll down to "Bot Permissions" and check the following boxes to give the bot the necessary permissions to work in your discord server:  
• View Channels (under general permissions)
• Send Messages (under text permissions)  
• Connect (under voice permissions)  
• Speak (under voice permissions)  
• Use Voice Activity (under voice permissions)  
v. Scroll up and click reset token
vi. Copy this token (it is just a line of text characters).
vii. Open the SoundBard_ai.py file in a way that you can edit it:  
• On Windows you can use text-edit by changing the .py file extension to .txt (but you must change it back to .py once done editing).  
• On Mac you can simply open with text-edit.  
• If you're using linux, you already know what to do ;)  
viii. In the Python script, edit the following line (right under the import lines),  
TOKEN = "place_your_bot_token_here"  
by pasting your token within the quotes.  

And you're done with this part!

# 4. Invite Bot to Server
i. In the discord developer portal, on the left-hand panel, click OAuth2 and scroll down to OAuth2 URL Generator.
ii. Check the following boxes:
• bot
• applications.commands
iii. Scroll down and copy the Generated URL.  
iv. Open the link in a new web browser tab. You will be directed to a page where you can choose which server you'd like to add your bot to. Pick one and click Authorize. Note you must be an admin of the server that you'd like to add the bot to.  

Your bot is now added to your server.

# 5. Install FFmpeg
FFmpeg is a free, open-source software project that is a multimedia framework for handling audio, video, and other media files and streams. SoundBard_ai uses ffmpeg as dependancy. It is installed different on different operating systems.

Windows:
i. Download from https://www.ffmpeg.org/download.html (You download directly from this link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z)
ii. Unzip and rename the folder "ffmpeg"
iii. Move to c-drive so the contents of the folder reside in C:\ffmpeg
iv. Add it to your Windows PATH variables (follow this tutorial: https://www.youtube.com/watch?v=6sim9aF3g2c)
v. Verify you installed correctly by running the following command in a command prompt window:

ffmpeg -version

MacOS:
If you don't have the package manager "Homebrew" installed, run the following commands in your terminal to install it:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"  

echo >> /Users/who3/.zprofile && echo 'eval "$(/usr/local/bin/brew shellenv)"' >> /Users/who3/.zprofile && eval "$(/usr/local/bin/brew shellenv)"

Note you must replace "who3" with your username. Check that you have installed brew successfully by running  
brew update  

You can follow this video tutorial for installing home-brew if you like: https://www.youtube.com/watch?v=IWJKRmFLn-g

Then install ffmpeg in your terminal with this command:  
brew install ffmpeg  

You can follow this video tutorial for installing home-brew if you like: https://www.youtube.com/watch?v=IWJKRmFLn-g

Linux:
In your terminal run the following commands:  
sudo apt update  
sudo apt install ffmpeg  

# 6. Install Opus (For MacOS and Linux)
If you are on windows, skip this step, as Opus should bundled with you python installation. Opus is a C library that handles audio processing.  

i. For MacOS, in terminal run  
brew install opus

ii. For Linux, in terminal run  
sudo apt update
sudo apt install libopus-dev 

# 7. Create Python Environment
In your preferred Python interpreter, you must create a virtual environment with the necessary dependancies to run you bot locally. The easiest way is to create the environment using conda and the SoundBard_ai.yml file included in this repo:  

cd /path_to_SoundBard_ai_Folder/ 
conda env create --file SoundBard_ai.yml

# 8. Run SoundBard_ai and Use in Discord Server
i. In your terminal, activate your SoundBard_ai environment, then navigate to the SoundBard_ai.py file and run it:

conda activate SoundBard_ai 
cd "/filepath/"
python3 SoundBard_ai.py

ii. Now that your python script is running, you can use the discord bot within your server. Type "!join" in a text channel to make the bot join your voice channel. The bot will now listen for the keywords defined in SOUND_TRIGGERS. Type "!leave" to kick the bot from your voice channel.

iii. To turn off the bot entirely, simply close your terminal window, or keyboard-interrupt the terminal with ctrl+c.

#How to Add/Remove Custom Sounds & Triggers
Follow the the template of _sound_list.txt, where the 'trigger' in quotes on the left is what you speak, and the 'file.mp3' in quotes on the right is the .mp3 file that your bot plays aloud. Don't forget the commas at the end of each line! Once you have your updated list, copy-paste the list into the "SOUND_TRIGGERS" section near the top of the SoundBard_ai.py file. You can also add random triggers if you want to get more advanced (review the examples in SoundBard_ai.py).

Comment with questions or requests, and enjoy!

import discord
from discord.ext import commands, voice_recv
import asyncio
import speech_recognition as sr
import vosk
import json
import os
import sys
import random # <--- NEW: Import the random module

# --- Configuration ---
TOKEN = "place_your_bot_token_here"  # Replace with your bot's token. Follow the steps in the README to get your token from the discord developer portal.

# Path to your downloaded Vosk model
VOSK_MODEL_PATH = "model" 

if not os.path.exists(VOSK_MODEL_PATH):
    print(f"Error: Vosk model not found at '{VOSK_MODEL_PATH}'")
    print("Please download and extract the model, and ensure the 'model' folder is in the correct directory.")
    sys.exit(1)

# --- Define Keyword to Sound File Mapping ---
SOUND_TRIGGERS = {
        'boom': 'boom.mp3',
    'dude': 'bruh.mp3',
    'chad': 'chad.mp3',
    'based': 'chad.mp3',
    'base': 'chad.mp3',
    'chicken': 'chicken_jockey.mp3',
    'check': 'chicken_jockey.mp3',
    # --- Special entry for probabilistic playback (if you want to play certain sounds at random) ---
    'random': ('bruh.mp3', 'boom.mp3', 0.5), # (sound_file_1, sound_file_2, probability_to_play_file_1)
    'example': ('bruh.mp3', 'boom.mp3', 0.75), # (sound_file_1, sound_file_2, probability_to_play_file_1)
}

# --- Discord Client Setup ---
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# --- Speech Recognition Setup ---
try:
    vosk_model = vosk.Model(VOSK_MODEL_PATH)
    VOSK_RECOGNIZER = sr.Recognizer()
    print(f"DEBUG: Vosk model initialized successfully from {VOSK_MODEL_PATH}")
except Exception as e:
    print(f"Error loading Vosk model at startup: {e}")
    sys.exit(1)

voice_clients = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    print(f"DEBUG: Script's Current Working Directory: {os.getcwd()}")


# --- check_and_play_sound to handle probabilistic playback ---
async def check_and_play_sound(recognized_text: str, user: discord.Member):
    """
    Checks the recognized text for multiple keywords and plays the corresponding sound.
    Handles probabilistic playback for specific keywords (e.g., 'pipe').
    """
    recognized_text_lower = recognized_text.lower()
    
    guild = user.guild
    if not guild:
        print(f"Could not determine guild for user {user.display_name}.")
        return

    for keyword, value in SOUND_TRIGGERS.items():
        if keyword in recognized_text_lower:
            selected_filename = None
            
            # Check if this keyword has probabilistic playback (like 'pipe')
            if isinstance(value, tuple) and len(value) == 3:
                # This is our custom probabilistic format: (default_file, rare_file, default_probability)
                default_file, rare_file, default_probability = value
                
                # Perform the probabilistic check
                if random.random() < default_probability: # e.g., 0.95 chance for default
                    selected_filename = default_file
                    print(f"DEBUG: Playing default '{default_file}' for '{keyword}'.")
                else: # The remaining percentage (e.g., 0.05 chance for rare)
                    selected_filename = rare_file
                    print(f"DEBUG: Playing rare '{rare_file}' for '{keyword}'.")
            else:
                # Standard case: keyword maps directly to a single filename string
                selected_filename = value
                print(f"DEBUG: Playing standard '{selected_filename}' for '{keyword}'.")

            if selected_filename: # Ensure a filename was successfully determined
                if guild.voice_client:
                    if not guild.voice_client.is_playing():
                        sound_path = os.path.join(os.path.dirname(__file__), selected_filename)
                        
                        if os.path.exists(sound_path):
                            try:
                                source = discord.FFmpegPCMAudio(sound_path)
                                guild.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
                                print(f"Playing '{selected_filename}' due to '{keyword}' from {user.display_name} in '{guild.name}'!")
                                return # Exit after playing (or attempting to play) the first matched sound
                            except Exception as e:
                                print(f"Error playing sound '{selected_filename}': {e}")
                        else:
                            print(f"Error: Sound file '{selected_filename}' not found at '{sound_path}'. Please ensure all MP3s are present.")
                    else:
                        print(f"Already playing audio, skipping '{selected_filename}' for '{keyword}' in '{guild.name}'.")
                else:
                    print(f"Bot not in a voice channel in '{guild.name}' to play sound for '{keyword}'.")
            return # Exit after finding a match and attempting to play

# --- process_voice_audio ---
def process_voice_audio(recognizer_obj: sr.Recognizer, audio_data: sr.AudioData, user: discord.Member) -> str | None:
    user_id = user.id if user else "Unknown"
    user_display_name = user.display_name if user else "Unknown"
    
    try:
        text = recognizer_obj.recognize_vosk(audio_data) 
        if text:
            parsed_text = json.loads(text).get('text', '')
            if parsed_text:
                print(f"Recognized from {user_display_name} (ID: {user_id}): {parsed_text}")
                return parsed_text
            
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results from Vosk service; {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding Vosk JSON output: {e} - Output: {text}")
    except Exception as e:
        print(f"An unexpected error occurred during synchronous speech recognition: {e}")
    
    return None

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        return await ctx.send("You need to be in a voice channel to make me join!")

    channel = ctx.author.voice.channel
    guild_id = ctx.guild.id

    if guild_id in voice_clients and voice_clients[guild_id].is_connected():
        await voice_clients[guild_id].move_to(channel)
        await ctx.send(f"Moved to {channel.name} and still listening in this server!")
    else:
        try:
            vc = await channel.connect(cls=voice_recv.VoiceRecvClient)
            voice_clients[guild_id] = vc
            print(f"Joined {channel.name} in '{ctx.guild.name}' and started listening!")

            vc.listen(
                voice_recv.extras.speechrecognition.SpeechRecognitionSink(
                    process_cb=process_voice_audio, 
                    text_cb=lambda user_obj, recognized_text: bot.loop.call_soon_threadsafe(
                        asyncio.create_task, 
                        check_and_play_sound(recognized_text, user_obj)
                    ) if recognized_text else None,
                    default_recognizer="vosk",
                )
            )
            await ctx.send(f"Joined {channel.name} and will listen for keywords in this server!")

        except RuntimeError as e:
            if "The SpeechRecognition module is required" in str(e):
                await ctx.send(f"Error: `speech_recognition` module is not properly installed or loaded for `discord-ext-voice-recv` to use `SpeechRecognitionSink`. Please ensure `pip install speech_recognition` was successful.")
                print(f"RuntimeError: {e}")
            else:
                await ctx.send(f"Could not join voice channel: {e}")
                print(f"Error joining voice channel or starting listener: {e}")
        except Exception as e:
            print(f"Error joining voice channel or starting listener: {e}")
            await ctx.send(f"Could not join voice channel: {e}")


@bot.command()
async def leave(ctx):
    guild_id = ctx.guild.id
    if guild_id in voice_clients and voice_clients[guild_id].is_connected():
        vc = voice_clients[guild_id]
        if vc.is_listening():
            vc.stop_listening()
            print(f"Stopped listening in '{ctx.guild.name}'.")
        await vc.disconnect()
        del voice_clients[guild_id]
        print(f"Left voice channel in '{ctx.guild.name}'.")
        await ctx.send("Left the voice channel.")
    else:
        await ctx.send("I'm not in a voice channel in this server.")

# Run the bot
bot.run(TOKEN)
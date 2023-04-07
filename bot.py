from nextcord.ext import commands
import nextcord
import datetime

from gtts import gTTS
import responses
import re, bot_data

import cogs.add_toon as add_toon_cog

import discord_token

const_TOKEN = discord_token.token
const_lang = 'en'
const_tld = 'us'

async def send_message(message, user_message, is_private):
    if len(user_message) == 0:
        print("Empty message")
        return
    
    try:
        response = responses.handle_response(user_message)

        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

def disconnect_DB(mydb):
    mydb.disconnect()

#create a function that accepts a string and cleans it for SQL
def clean_text(string):
    escape_dict = {
        "'": "''", 
        '"': '""', 
        "\\": "\\\\", 
        "%": "\%", 
        "_": "\_", 
        "[": "\[", 
        "]": "\]", 
        "^": "\^", 
        "?": "\?", 
        "*": "\*", 
        "(": "\(", 
        ")": "\)", 
        "{": "\{", 
        "}": "\}", 
        ";": "\;"
        }
    
    for escape_char in escape_dict:
        string = string.replace(escape_char, escape_dict[escape_char])

    return string

def connect_DB():
    ret = bot_data.Database("hearyee.db")
    ret.connect()
    return ret

def create_speech_source(message, guild_id, lang, tld):
    myobj = gTTS(text=message, lang=lang, tld=tld, slow=False, )

    filename = f"{guild_id}-tts-audio.mp3"
    myobj.save(filename)
    
    source = nextcord.PCMVolumeTransformer(nextcord.FFmpegPCMAudio(filename, executable="C:/ffmpg/bin/ffmpeg.exe"))
    return source



def create_voice_state_update_message(member, before, after):

    print(f"[create_voice_state_update_message]guild=={member.guild.name}")
    print(f"[create_voice_state_update_message]before.channel=={before.channel}")
    print(f"[create_voice_state_update_message]after.channel=={after.channel}")
    print(f"[create_voice_state_update_message]member=={member}")
    
    before_channel = before.channel
    after_channel = after.channel

    if before_channel == None: before_channel = "None"
    if after_channel == None: after_channel = "None"

    #if they are joining the channel from being disconnected
    if before_channel == "None":
        display_name = generate_name(member, True) #send it over with fanfare if they are joining the channel
    else:
        display_name = generate_name(member)


    before_channel = f"has left" if before_channel != "None" else ""
        
    after_channel = f"has joined" if after_channel != "None" else ""

    if len(after_channel) > 0 and len(before_channel) > 0: after_channel = f" and {str(after_channel)}"

    
    message = f"{display_name} {before_channel}{after_channel}"
    return message

def generate_name(member, fanfare=False):
    clean_name = re.sub(r'[^\w\s,]', '', member.display_name) #remove all non alphanumeric characters

    if clean_name == "Tricksyhobit Sam": return "The tallest Hobbit"

    if fanfare:
        names=["Druith Dru+", "Tricksyhobit Sam", "0R0", "Lawrence Tom", "Spindrift", "Marquitos Marc", "Chrissy", "Triggered", "MilliV", "TwinBlade", "Grezlok"]
        title=["His Majesty, King Buttercup; Druith", "The tallest Hobbit", "Oar owe", "Law Man", "High Magus Spin of the Detroit Drifts", "Marc of the Washington Wee Toes", "Doctor Chrissy Sky, PHD Candidate", "Tom's side piece, Triggered, esquire", "Professor MilliV of the Middlemost School", "Twin Blade, One man legion", "Hold my beer, Grezlok is here"]

        if str(member.display_name) in names:
            return title[names.index(str(clean_name))]

    return clean_name

async def say_text_in_chat(ctx, text, user):
    if user.voice != None:
        vc = None

        if ctx.voice_client == None:
            vc = await ctx.message.author.voice.channel.connect(reconnect=True)
        else:
            vc = ctx.voice_client

        source = create_speech_source(text, ctx.guild.id, const_lang, const_tld)

        vc.play(source)

        await ctx.send(text)
    else:
        await ctx.send('You need to be in a vc to run this command!')

def run_discord_bot():
    instance_intents = nextcord.Intents.all()
    bot=commands.Bot(command_prefix='$', intents=instance_intents)
    
    @bot.command(name='tts')
    async def tts(ctx, *args):
        text = " ".join(args)
        user = ctx.message.author
        await say_text_in_chat(ctx, text, user)

    @bot.command(name='chrissysays')
    async def chrissysays(ctx, *args):
        text = " ".join(args)
        user = ctx.message.author
        if user.voice != None:
            vc = None

            if ctx.voice_client == None:
                vc = await ctx.message.author.voice.channel.connect(reconnect=True)
            else:
                vc = ctx.voice_client

            source = create_speech_source(text, ctx.guild.id, 'fr', 'ca')

            vc.play(source)
        else:
            await ctx.send('You need to be in a vc to run this command!')

    @bot.command(name='drusays')
    async def chrissysays(ctx, *args):
        text = " ".join(args)
        user = ctx.message.author
        if user.voice != None:
            vc = None

            if ctx.voice_client == None:
                vc = await ctx.message.author.voice.channel.connect(reconnect=True)
            else:
                vc = ctx.voice_client

            source = create_speech_source(text, ctx.guild.id, 'en', 'ie')

            vc.play(source)
        else:
            await ctx.send('You need to be in a vc to run this command!')
    
    @bot.event
    async def on_ready():
        current_time = datetime.datetime.now().strftime("%m/%d/%y, %H:%M:%S %p")
        print(f'[{current_time}] We have logged in as {bot.user} to monitor {len(bot.guilds)} guilds.')
  
    @bot.event
    async def on_voice_state_update(member, before, after, **args):
        if before.channel == after.channel or member == bot.user: #then it is a mute/unmute or deafen/undeafen, ignore for now
            return

        message = create_voice_state_update_message(member, before, after)

        print(f"[on_voice_state_update](message){message}")
        
        voice_client = nextcord.utils.get(bot.voice_clients, guild=member.guild)

        if voice_client is not None:
            source = create_speech_source(message, member.guild.id, const_lang, const_tld)

            try:
                if voice_client.is_connected():
                    voice_client.stop()
                    voice_client.play(source)
            
            except Exception as e:
                print(f"[on_voice_state_update](try){str(e)}")

    @bot.command(name='join', help='This command makes the bot join the voice channel')
    async def join(ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not connected to a voice channel")
        voice_channel = ctx.message.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await say_text_in_chat(ctx, "Hear Yee has connected!", ctx.message.author)
        else:
            if ctx.voice_client.channel != voice_channel:
                await ctx.voice_client.move_to(voice_channel)
                await say_text_in_chat(ctx, "Hear Yee has arrived!", ctx.message.author)
            else:
                await ctx.send("Hear Yee is already in the channel")

    @bot.command(name='leave', help='This command makes the bot leave the voice channel')
    async def leave(ctx):
        if ctx.voice_client is None:
            await ctx.send("Hear Yee is not in the channel")
        else:
            await ctx.voice_client.disconnect()
            await ctx.send("Hear Yee has left!")

    @bot.command(name='E', help='my precious')
    async def sql_execute(ctx):
        if ctx.author.id != 610981657343950886: 
            await ctx.send("You are not authorized to use this command; does Hobit know you are playing with his toys?")
            return
        try:

            mydb = bot_data.Database("hearyee.db")
            mydb.connect()
            mydb.execute(ctx.message.content[3:])
            mydb.disconnect()
            await ctx.send("SQL command executed")
        except Exception as e:
            await ctx.send("SQL command failed... [error={str(e)}]")

    @bot.command(name='Q', help='my precious')
    async def sql_query(ctx):
        if ctx.author.id != 610981657343950886: 
            await ctx.send("You are not authorized to use this command; does Hobit know you are playing with his toys?")
            return
        try:
            args_list = ctx.message.content[3:].split("|")

            if len(args_list) == 3:
                table_name = args_list[0]
                columns = args_list[1]
                condition = args_list[2]
                

                mydb = bot_data.Database("hearyee.db")
                mydb.connect()
                records = mydb.select(table_name, columns, condition)
                mydb.disconnect()
                
                output = f"Results({len(records)}):\n\n"
                for record in records:
                    output += f"{record}\n"


                await ctx.send(output)
        except Exception as e:
            await ctx.send("SQL command failed... [error={str(e)}]")

    @bot.command(name='I', help='my precious')
    async def sql_query(ctx):
        if ctx.author.id != 610981657343950886: 
            await ctx.send("You are not authorized to use this command; does Hobit know you are playing with his toys?")
            return
        try:
            args_list = ctx.message.content[3:].split("|")

            if len(args_list) == 3:
                table_name = args_list[0]
                columns = args_list[1]
                values = args_list[2]

                mydb = bot_data.Database("hearyee.db")
                mydb.connect()
                inserted_id = mydb.insert(table_name, columns, values)
                
                if inserted_id == None: output = "No rows were inserted"
                else: output = f"Inserted({inserted_id})\n\n"
              
                mydb.disconnect()

                await ctx.send(output)
        except Exception as e:
            await ctx.send("SQL command failed... [error={str(e)}]")

    @bot.command(name='register', help='REGISTER WITH HEARYEE')
    async def register_member(ctx):
        # if ctx.author.id != 610981657343950886: 
        #     await ctx.send("You are not authorized to use this command; does Hobit know you are playing with his toys?")
        #     return
        try:
            message = ctx.message
            fanfare = clean_text(message.content[9:].lower())

            table_name = "members"
            columns = "name, discord_id, discord_username, fanfare_title, discord_guild_id"
            values = f"'{message.author.display_name}', '{message.author.id}', '{message.author.name}', '{fanfare}', {message.guild.id}"

            mydb = connect_DB()

            inserted_id = mydb.insert(table_name, columns, values)
            
            if inserted_id == None: output = "No rows were inserted"
            else: output = f"Inserted({inserted_id})\n\n"
            
            disconnect_DB(mydb)

            await ctx.send(output)
        except Exception as e:
            await ctx.send("SQL command failed... [error={str(e)}]")
   
    @bot.command(name='update-title', help='my precious')
    async def register_member(ctx):
        # if ctx.author.id != 610981657343950886: 
        #     await ctx.send("You are not authorized to use this command; does Hobit know you are playing with his toys?")
        #     return
        try:
            message = ctx.message
            fanfare = clean_text(message.content[13:].lower())

            table_name = "members"
            set = f"fanfare_title = '{fanfare}'"
            where = f"discord_id = '{message.author.id}' and discord_guild_id = '{message.guild.id}'"

            mydb = connect_DB()

            mydb.update(table_name, set, where)
            
            output = f"Fanfare updated successfully\n{where}\n"
            
            disconnect_DB(mydb)

            await ctx.send(output)
           
        except Exception as e:
            await ctx.send("SQL command failed... [error={str(e)}]")

    TOWER_DEFENSE_SIGNUP_SUCCESS_MESSAGE = "Your info has been saved to the roster signup! Thank you! You can update the information by simply reposting the updated information to #tower-defense."

    @bot.event
    async def on_message_edit(before, after):
        if after.author.bot:
            return # Return if the message is from a bot
        if isinstance(after.channel, nextcord.DMChannel):
            return # Return if the message is a DM

        LISTENING_CHANNEL = "hobits-hackery"
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        # Check if the message is from a specific text channel
        if after.channel.name == LISTENING_CHANNEL:
            # Check if the message contains comma separated values
            if ',' in after.content and after.content.count(',') >= 5:
                # Split the message content into a list of values
                values = after.content.split(',')
                # Parse the desired values from the list
                name = clean_text(values[0])
                resonance = clean_text(values[1])
                health = clean_text(values[2])
                damage = clean_text(values[3])
                paragon = clean_text(values[4])
                class_ = clean_text(values[5])
                discord_id = str(after.author.id)
                discord_name = clean_text(after.author.display_name)
                updated_on = datetime.datetime.now().strftime(DATE_FORMAT)
                # Save the values to the SQLite database
                table_name = "tower_defense"
                columns = "name, resonance, health, damage, paragon, class, discord_id, discord_name, updated_on"
                values = f"'{name}', '{resonance}', '{health}', '{damage}', '{paragon}', '{class_}', '{discord_id}', '{discord_name}', '{updated_on}'"
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON CONFLICT(discord_id) DO UPDATE SET resonance='{resonance}', health='{health}', damage='{damage}', paragon='{paragon}', class='{class_}', discord_id='{discord_id}', discord_name='{discord_name}', updated_on='{updated_on}'"
                mydb = connect_DB()
                mydb.execute(query)
                disconnect_DB(mydb)

                # Direct message the user who submitted the message
                author = after.author
                dm_message = TOWER_DEFENSE_SIGNUP_SUCCESS_MESSAGE
                await author.send(dm_message)

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return # Return if the message is from a bot
        if isinstance(message.channel, nextcord.DMChannel):
            return # Return if the message is a DM

        LISTENING_CHANNEL = "hobits-hackery"
        DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

        # Check if the message is from a specific text channel
        if message.channel.name == LISTENING_CHANNEL:
            # Check if the message contains comma separated values
            if ',' in message.content and message.content.count(',') >= 5:
                # Split the message content into a list of values
                values = message.content.split(',')
                # Parse the desired values from the list
                name = clean_text(values[0])
                resonance = clean_text(values[1])
                health = clean_text(values[2])
                damage = clean_text(values[3])
                paragon = clean_text(values[4])
                class_ = clean_text(values[5])
                discord_id = str(message.author.id)
                discord_name = clean_text(message.author.display_name)
                updated_on = datetime.datetime.now().strftime(DATE_FORMAT)
                # Save the values to the SQLite database
                table_name = "tower_defense"
                columns = "name, resonance, health, damage, paragon, class, discord_id, discord_name, updated_on"
                values = f"'{name}', '{resonance}', '{health}', '{damage}', '{paragon}', '{class_}', '{discord_id}', '{discord_name}', '{updated_on}'"
                query = f"INSERT INTO {table_name} ({columns}) VALUES ({values}) ON CONFLICT(discord_id) DO UPDATE SET resonance='{resonance}', health='{health}', damage='{damage}', paragon='{paragon}', class='{class_}', discord_id='{discord_id}', discord_name='{discord_name}', updated_on='{updated_on}'"
                mydb = connect_DB()
                mydb.execute(query)
                disconnect_DB(mydb)

                # Direct message the user who submitted the message
                author = message.author
                
                dm_message = TOWER_DEFENSE_SIGNUP_SUCCESS_MESSAGE
                await author.send(dm_message)
        await bot.process_commands(message)


    add_toon_cog.setup(bot)

    bot.run(const_TOKEN)



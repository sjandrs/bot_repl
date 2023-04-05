import nextcord
from nextcord.ext import commands
from util import sanitize
import sqlite3

class ManageToon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('hearyee.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS diablo_toons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            resonance INTEGER NOT NULL,
            health INTEGER NOT NULL,
            damage INTEGER NOT NULL,
            paragon_level INTEGER NOT NULL,
            class TEXT NOT NULL,
            clan_name TEXT NOT NULL,
            shadow_rank TEXT,
            discord_id INTEGER NOT NULL
            )''')
        self.conn.commit()

    @commands.command(name='register-toon')
    async def register_toon(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        await ctx.send("Please enter your character name:")
        name = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character resonance:")
        resonance = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character health:")
        health = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character damage:")
        damage = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character paragon level:")
        paragon_level = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character class:")
        character_class = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character clan name:")
        clan_name = await self.bot.wait_for('message', check=check)
        await ctx.send("Please enter your character shadow rank:")
        shadow_rank = await self.bot.wait_for('message', check=check)

        discord_id = ctx.author.id

        self.cursor.execute("INSERT INTO diablo_toons (name, resonance, health, damage, paragon_level, class, clan_name, shadow_rank, discord_id) \
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                            (sanitize(name.content), 
                             sanitize(resonance.content), 
                             sanitize(health.content), 
                             sanitize(damage.content), 
                             sanitize(paragon_level.content), 
                             sanitize(character_class.content), 
                             sanitize(clan_name.content),
                             sanitize(shadow_rank.content),
                             discord_id))
        self.conn.commit()

        await ctx.send("Your character information has been saved to the database.")

    @commands.command(name='toon-list')
    async def toon_list(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        role = nextcord.utils.get(ctx.guild.roles, name='Clan Member')
        if role not in ctx.author.roles:
            await ctx.send("You must have the Clan Member role to use this command.")
            return

        self.cursor.execute(f"SELECT name, resonance, health, damage, paragon_level, class, clan_name, \
                            shadow_rank FROM diablo_toons WHERE discord_id = {ctx.author.id}")
        toons = self.cursor.fetchall()

        if not toons:
            await ctx.send("There are no registered toons. Would you like to register one? (y/n)")
            register_toon_response = await self.bot.wait_for('message', check=check)
            if register_toon_response.content.lower() == 'y' or register_toon_response.content.lower() == 'yes':
                await self.register_toon(ctx)
            return

        message = "Registered Toons:\n"
        for toon in toons:
            message += f"Name: {toon[0]}\
                \nResonance: {toon[1]}\
                \nHealth: {toon[2]}\
                \nDamage: {toon[3]}\
                \nParagon Level: {toon[4]}\
                \nClass: {toon[5]}\
                \nClan Name: {toon[6]}\
                \nShadow Rank: {toon[7]}\
                \n\n"
        
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ManageToon(bot))

import os, sys, discord, platform, random, aiohttp, json, time, asyncio,traceback
from discord.ext import commands,tasks
from utils.lists import roasts_list
from discord.ext.commands.cooldowns import BucketType
from utils.help import EmbedHelpCommand
import asyncpg
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config



colourlist=[0xCCFF00,0x00C2C7,0x006163,0xE67E22,0xC14DF0,0xEC4451,0xFAED2E,0x2E75FA,0xFA782E,
            0x2EFAD2,0xFF729D,0xA172FF,0x72A3FF,0xFF0000,0x0DAA00,0x171EFF,0x8BD6F9,0x8E44AD,0x9B59B6,]



#bot
intents = discord.Intents.default()
intents.members = True
#intents.presences = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("yeet ","y ","Y ","Yeet "),case_insensitive = True,intents = intents,help_command=EmbedHelpCommand())
#bot = commands.Bot(command_prefix=commands.when_mentioned_or("Beta ","beta "),case_insensitive = True,intents = intents,help_command=EmbedHelpCommand())
#declarations
#TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = "NzUwMjM2MjIwNTk1ODk2Mzcw.X03l7Q.sC1NA7kusFCB778Em5aw0LyNVTo"
#Beta
#TOKEN = "Nzc4NTc0NzU2NjA0NTQzMDI2.X7T-Pw.r4of7QgJV686GLsLutR6lZjHEBU"

for extension in config.STARTUP_COGS:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

class CommandErrorHandler(commands.Cog):
    #https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="<:warn:789487083802460200>  | Missing Argument",description="Oops...You missed an argument.",color = random.choice(colourlist))
            embed.add_field(name="You are missing a required argument.",value="Type \"Yeet help <command-name>\" to learn how to use a command.", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed=discord.Embed(title="<:warn:789487083802460200>  | Invalid User",description="Mention a valid user", color = random.choice(colourlist))
            embed.add_field(name="An incorrect user was mentioned",value="Mention a user or a users user id", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error,commands.CommandNotFound):pass

        elif isinstance(error,commands.errors.BadArgument):
            embed=discord.Embed(title="<:warn:789487083802460200>  | Invalid Argument",color = random.choice(colourlist))
            embed.add_field(name="You passed a incorrect or invalid argument", value=" Please make sure that you are using the correct format.\n Type \"r help command_name\" to learn how to use a command.", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error,TypeError):pass

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            embed=discord.Embed(title="<:warn:789487083802460200>  | Bot doesn't have required permissions",color = random.choice(colourlist))
            embed.add_field(name="Please give me the required permissions and try again.", value=f"{missing_permissions}", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            embed=discord.Embed(title="<:warn:789487083802460200>  | Missing Permissions",color = random.choice(colourlist))
            embed.add_field(name="You don't have the required permissions", value=f"{missing_permissions}", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MaxConcurrencyReached):
            embed=discord.Embed(title="<:warn:789487083802460200>  | Maximimum Concurrency",color = random.choice(colourlist))
            embed.add_field(name="The same command is currently ongoing in this channel.", value=f"Use a different Channel or wait until the current command is completed.", inline=False)
            await ctx.send(embed=embed)
        
        # elif isinstance(error, commands.UserInputError):
        #     await ctx.send("Invalid input.")
        #     await self.send_command_help(ctx)
        #     return

        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in [571957935270395925]:
                await ctx.reinvoke()
            #elif ctx.guild.id in [748786284373475358,748754737695948860,774113408378863666]:
                #await ctx.reinvoke()
            else:
                embed=discord.Embed(title="<:warn:789487083802460200>  | Command on Cooldown",color = random.choice(colourlist))
                embed.add_field(name="Slow down there, Romeo :rose: :race_car:", value=" Please wait before using this command again. You can use this command in {:.2f} s'seconds again.".format(error.retry_after), inline=False)
                await ctx.send(embed=embed)
        else:
            #traceback=traceback.format_exception(type(error), error, error.__traceback__)
            embed=discord.Embed(title="<:warn:789487083802460200>  | Goddamn Karen!",description="I knew I could count on you for screwing this up...",color = random.choice(colourlist))
            #embed.add_field(name='Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #etype, value, tb = sys.exc_info()
            embed.add_field(name="Something went wrong. Try again later",value=f"{error} \n {traceback.format_exc()}", inline=False)

            await ctx.send(embed=embed)

#loop = asyncio.get_event_loop()
#bot.pool = loop.run_until_complete(asyncpg.create_pool(database="Yeet Bot DB",user="postgres",password="Welcome1"))
bot.add_cog(CommandErrorHandler(bot))       
bot.run(TOKEN)

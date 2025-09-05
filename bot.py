import os
import discord
from discord import app_commands

#--------------------------------------------------

TOKEN = os.environ['DISCORD_TOKEN']
OWNER_ID = os.environ['DISCORD_OWNER']
MY_GUILD = discord.Object(id=1376201573520244746)  # replace with your guild id


class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD) # 同步指定伺服器指令 → 測試用（馬上生效）
        
        # 同步全域指令 → 給其他伺服器用（要等一段時間）
        #await self.tree.sync()


intents = discord.Intents.default()
client = MyClient(intents=intents)

# Activity,Streaming,Game
activity = discord.Activity(
    type=discord.ActivityType.streaming, # https://discordpy.readthedocs.io/en/stable/api.html#discord.ActivityType
    name="有趣的東西",
    state="別看了\t沒什麼好看的 (´･ω･`)",
    #url="https://www.twitch.tv/infin21live"  # Twitch URL is required for streaming activity
)

@client.event
async def on_ready():
    print(f'登入為: {client.user} (ID: {client.user.id})')
    await client.change_presence(activity=activity)
    print("機器人狀態已設置!")
    print('------')

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
async def stop(interaction: discord.Interaction):
    """stop bot"""
    if interaction.user.id != OWNER_ID:
        await interaction.response.send_message("You are not the owner of the bot.", ephemeral=True)
        return
    await interaction.response.send_message("Stopping the bot...", ephemeral=True)
    print("Shutting down…")
    await client.close()


client.run(TOKEN)

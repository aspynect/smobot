import discord
from discord import app_commands
import requests
import json

with open('secrets.json', 'r') as file:
    secrets = json.load(file)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="runner",description="Get the 'runner' role")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.describe(username="Your Speedrun.com Username")
async def runner(interaction: discord.Interaction, username: str):
    # embed = discord.Embed(title = f"{user.name}'s PFP", color = myColor)
    response = requests.get(f"https://www.speedrun.com/api/v2/GetUserSummary?url={username}")
    userData = response.json()
    discordData = next((entry for entry in userData["userSocialConnectionList"] if entry.get("networkId") == 5), None)
    if discordData is None:
        await interaction.response.send_message("No discord linked to SR.C account", ephemeral = True)
        return
    if discordData["value"] != interaction.user.name:
        await interaction.response.send_message("Discord name does not match SR.C account", ephemeral = True)
        return
    if discordData["verified"] == False:
        await interaction.response.send_message("Discord account not verified on SR.C", ephemeral = True)
        return
    await interaction.user.add_roles(discord.utils.get(interaction.guild.roles, name="Runner"))
    await interaction.response.send_message("Role granted!", ephemeral = True)



@tree.command(name="sync",description="sync")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
async def sync(interaction: discord.Interaction):
    await tree.sync()
    await interaction.response.send_message("sunk!", ephemeral = True)
    print("Sunk!")

@client.event
async def on_ready():
    print("Ready!")

if __name__ == "__main__":
    client.run(secrets["token"])
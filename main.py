import discord
from discord import app_commands
import json
from api_checks import checkRunnerRole, RunnerResult, runnerResultToErrorString

with open("secrets.json", "r") as file:
    secrets = json.load(file)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="runner", description="Get the 'Runner' role. Removes the role if you already have it.")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.describe(username="Your Speedrun.com Username")
async def runner(interaction: discord.Interaction, username: str):
    runnerRole = discord.utils.get(interaction.guild.roles, name="Runner")

    if runnerRole in interaction.user.roles:
        await interaction.user.remove_roles(runnerRole)
        await interaction.response.send_message(
            "The 'Runner' role has been removed.", ephemeral=True
        )
        return

    result = checkRunnerRole(interaction.user.name, username)  

    if result == RunnerResult.IsEligible:
        await interaction.user.add_roles(runnerRole) 

    await interaction.response.send_message(
        runnerResultToErrorString(result), ephemeral=True
    )


@tree.command(name="role", description="Get or remove a role.")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.describe(role="The role that you want to get or remove.")
@app_commands.choices(role=[
    app_commands.Choice(
        name = secrets["roles"][i], value = secrets["roles"][i]) 
        for i in range(len(secrets["roles"]))
    ]
)
async def role(interaction: discord.Interaction, role: app_commands.Choice[str]):
    desiredRole = discord.utils.get(interaction.guild.roles, name=role.name)
    if desiredRole in interaction.user.roles:
        await interaction.user.remove_roles(desiredRole)
        await interaction.response.send_message(
            f"The '{role.name}' role has been removed.", ephemeral=True
        )
    else:
        await interaction.user.add_roles(desiredRole)
        await interaction.response.send_message(
            f"The '{role.name}' role has been given.", ephemeral=True
        )


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

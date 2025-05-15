import discord
from discord import app_commands
from os import getenv
from api_checks import checkRunnerRole, RunnerResult, runnerResultToErrorString

DISCORD_TOKEN = getenv("DISCORD_TOKEN", "NO TOKEN PROVIDED")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(
    name="runner",
    description="Get the 'Runner' role. Removes the role if you already have it.",
)
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


@tree.command(name="sync", description="sync")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
async def sync(interaction: discord.Interaction):
    await tree.sync()
    await interaction.response.send_message("sunk!", ephemeral=True)
    print("Sunk!")


@client.event
async def on_ready():
    print("Ready!")


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)

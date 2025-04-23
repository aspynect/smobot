import discord
from discord import app_commands
import json
from api_checks import checkRunnerRole, RunnerResult, runnerResultToErrorString

with open("secrets.json", "r") as file:
    secrets = json.load(file)
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@tree.command(name="runner", description="Get the 'Runner' role")
@app_commands.allowed_installs(guilds=True, users=False)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.describe(username="Your Speedrun.com Username")
async def runner(interaction: discord.Interaction, username: str):
    res = checkRunnerRole(interaction.user.name, username)

    if res == RunnerResult.IsEligible:
        await interaction.user.add_roles(
            discord.utils.get(interaction.guild.roles, name="Runner")
        )  # We should change this to be Role ID based. Not that it matters too much, but I would prefer if it was more specific than simply "any role named Runner"

    await interaction.response.send_message(
        runnerResultToErrorString(res), ephemeral=True
    )


if __name__ == "__main__":
    client.run(secrets["token"])

import discord
from discord import app_commands
from os import getenv
from api_checks import checkRunnerRole, RunnerResult, runnerResultToErrorString
from bot_logs import createLogEmbed

DISCORD_TOKEN = getenv("DISCORD_TOKEN", "NO TOKEN PROVIDED")
LOG_CHANNEL_ID = int(getenv("LOG_CHANNEL_ID", "NO LOG CHANNEL ID PROVIDED"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def log_command(interacton: discord.Interaction, command_response: str):
    print("Logging command usage...")
    if type(LOG_CHANNEL_ID) is str:
        print("No log channel ID provided.")
        return
    user = interacton.user
    embed = createLogEmbed(timestamp = interacton.created_at, username=user.name, user_id=user.id, command_name=interacton.command.name, command_response=command_response)
    log_channel = client.get_channel(LOG_CHANNEL_ID)
    await log_channel.send(embed=embed)

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
        await log_command(
            interacton = interaction,
            command_response = "The 'Runner' role has been removed."
        )
        await interaction.response.send_message(
            "The 'Runner' role has been removed.", ephemeral=True
        )
        return

    result = checkRunnerRole(interaction.user.name, username)

    if result == RunnerResult.IsEligible:
        await interaction.user.add_roles(runnerRole)
        
    resultString = runnerResultToErrorString(result)

    await log_command(
        interacton = interaction,
        command_response = resultString
    )

    await interaction.response.send_message(
        resultString, ephemeral=True
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

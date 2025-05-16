import discord
from discord import app_commands
from os import getenv
from api_checks import checkRunnerRole, RunnerResult, runnerResultToErrorString
from bot_logs import UserInfo, createLogEmbed

DISCORD_TOKEN = getenv("DISCORD_TOKEN", "NO TOKEN PROVIDED")
LOG_CHANNEL_ID = int(getenv("LOG_CHANNEL_ID", "NO LOG CHANNEL ID PROVIDED"))

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

    result = RunnerResult.UnknownError

    if runnerRole in interaction.user.roles:
        await interaction.user.remove_roles(runnerRole)
        result = RunnerResult.ObtainedRemoval
    else:
        result = checkRunnerRole(interaction.user.name, username)

        if result == RunnerResult.IsEligible:
            await interaction.user.add_roles(runnerRole)

    print(
        "Runner Role: {0} wrote {1} and got {2}.".format(
            interaction.user.name,
            username,
            result.name,
        )
    )
    if LOG_CHANNEL_ID != "NO LOG CHANNEL ID PROVIDED":
        embed = createLogEmbed(
            UserInfo(
                name=interaction.user.name,
                picture_url=interaction.user.avatar.url,
                discord_id=interaction.user.id,
            ),
            username,
            result,
            UserInfo(
                name=client.user.name,
                picture_url=client.user.avatar.url,
                discord_id=client.user.id,
            ),
        )
        log_channel = client.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(embed=embed)

    resultString = runnerResultToErrorString(result)

    await interaction.response.send_message(resultString, ephemeral=True)


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

from discord import Embed, Color

def createLogEmbed(timestamp: int, username: str, user_id: int, command_name: str, command_response: str) -> Embed:
    embed = Embed(
        title="Command Log",
        description=f"{username} ({user_id}) used /{command_name}\n{command_response}",
        timestamp=timestamp,
        color=Color.red(),
    )
    return embed
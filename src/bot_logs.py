from datetime import datetime
from discord import Embed, Color
from dataclasses import dataclass
from api_checks import RunnerResult


@dataclass
class UserInfo:
    name: str
    discord_id: int
    picture_url: str


def createLogEmbed(
    user: UserInfo, src_name: str, result: RunnerResult, bot: UserInfo
) -> Embed:
    embed = Embed(title="Runner Role", color=Color.red(), timestamp=datetime.now())
    embed.set_author(
        name=f"{user.name} ({user.discord_id})",
        url=user.picture_url,
        icon_url=user.picture_url,
    )
    embed.set_footer(
        text=bot.name,
        icon_url=bot.picture_url,
    )
    embed.add_field(name="SRC Username", value=src_name)
    embed.add_field(name="Result", value=result.name)
    return embed

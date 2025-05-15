import requests
from enum import Enum
import os

RUNNER_THRESHOLD = int(os.environ.get("RUNNER_THRESHOLD", 3600))

ENDPOINT: str = "https://www.speedrun.com/api/v2/"
USER_SUMMARY_ENDPOINT: str = ENDPOINT + "GetUserSummary?url={}"


class RunnerResult(Enum):
    IsEligible = 0
    AccountNotFound = 1
    DiscordNotFound = 2
    DiscordNameNotMatch = 3
    DiscordNotVerified = 4
    NotEnoughOdysseyRuns = 5
    UnknownError = 6


def checkRunnerRole(discord_name: str, src_username: str) -> RunnerResult:
    api_request = requests.get(USER_SUMMARY_ENDPOINT.format(src_username))

    if api_request.status_code == 404:
        return RunnerResult.AccountNotFound
    elif api_request.status_code != 200:
        return RunnerResult.UnknownError

    api_request_json = api_request.json()

    discord_data = next(
        (
            entry
            for entry in api_request_json["userSocialConnectionList"]
            if entry.get("networkId") == 5
        ),
        None,
    )

    if discord_data is None:
        return RunnerResult.DiscordNotFound
    elif not discord_data["verified"]:
        return RunnerResult.DiscordNotVerified
    elif discord_data["value"] != discord_name:
        return RunnerResult.DiscordNameNotMatch

    total_time = sum(
        entry["totalTime"]
        for entry in api_request_json["userGameRunnerStats"]
        if entry["gameId"] in ["76r55vd8", "m1mxxw46"]
    )

    if total_time < RUNNER_THRESHOLD:
        return RunnerResult.NotEnoughOdysseyRuns
    else:
        return RunnerResult.IsEligible


def runnerResultToErrorString(result: RunnerResult) -> str:
    match result:
        case RunnerResult.IsEligible:
            return "The 'Runner' role has been given."
        case RunnerResult.AccountNotFound:
            return "The speedrun.com username could not be found."
        case RunnerResult.DiscordNotFound:
            return "We couldn't find a Discord account attached to this profile. Ensure that it is linked by navigating to https://www.speedrun.com/settings/socials and linking your Discord account."
        case RunnerResult.DiscordNameNotMatch:
            return "A Discord account is linked to this SRC profile, but it doesn't match yours."
        case RunnerResult.DiscordNotVerified:
            return "The Discord account is not verified! Navigate to https://www.speedrun.com/settings/socials, unlink your Discord account, and re-link it to verify it."
        case RunnerResult.NotEnoughOdysseyRuns:
            return "You have not run Super Mario Odyssey enough to be eligible for the 'Runner' role. You must have at least one hour of total time across verified submissions."
        case RunnerResult.UnknownError:
            return "Something went wrong when attempting to look up your information. Speedrun.com may just be having issues. If this happens repeatedly, please message a moderator."

# smobot

## environment variables

### required

- DISCORD_TOKEN: Specifies the token of the discord bot to connect to.
- SMO_CHECKED_GAMES: The list of games to check for the appropriate runner
  threshold. Comma separated string, with each value as the SRC API ID (for
  example: 76r55vd8,m1mxxw46).

### optional

- RUNNER_THRESHOLD: The amount of time necessary to qualify for the role, in
  seconds. Default is 3600 (1hr).

## docker instructions

- docker build -t smobot-image .
- docker run -e DISCORD_TOKEN="<token>" smobot-image

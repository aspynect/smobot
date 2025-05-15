# smobot

## environment variables

### required

- DISCORD_TOKEN="foo"

### optional

- RUNNER_THRESHOLD="3600"
- SMO_CHECKED_GAMES="76r55vd8,m1mxxw46"

## docker instructions

- docker build -t smobot-image .
- docker run -e DISCORD_TOKEN="<token>" smobot-image

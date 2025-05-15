# smobot
## environment variables
### required in .env
DISCORD_TOKEN="foo"
### optional
RUNNER_THRESHOLD="3600"
## docker instructions
docker build -t smobot-image .
docker run --env-file .env smobot-image
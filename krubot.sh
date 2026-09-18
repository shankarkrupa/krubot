export LLM_MODEL=$(cat krubot_config.json | jq '.["LLM_MODEL"]' -r)
export LLM_BASE_URL=$(cat krubot_config.json | jq '.["LLM_BASE_URL"]' -r)
export LLM_API_KEY=$(cat krubot_config.json | jq '.["LLM_API_KEY"]' -r)
echo $LLM_BASE_URL
python krubot.py --no-confirm

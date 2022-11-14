# Encode2Tg [BETA] [![pyLint](https://github.com/Niffy-the-conqueror/Encode2Tg/actions/workflows/pyLint.yml/badge.svg?branch=anime)](https://github.com/Niffy-the-conqueror/Encode2Tg/actions/workflows/pyLint.yml)

## With HandBrakeCLI support

### Variables
---
Compulsory Variables | Explanation
:--------- | :---------------------------------------------
`APP_ID` `API_HASH` `BOT_TOKEN` | get the first two from [Telegram.org](telegram.org) and the third from [@Botfather](t.me/botfather)
`OWNER`    | input id Of allowed users with a space between each

Optional Variables | Explanation
:--------- | :---------------------------------------------
`THUMBNAIL`  | input telegraph link of a picture for use as Thumbnail.
`FFMPEG` | input Your FFMPEG Code or Handbrake-cli code (after installing it)  with """{}""" as input and output. (Eg. __ffmpeg -i """{}""" -preset veryfast -vcodec libx265 -crf 27 """{}"""__) escape the " characters if you're deploying locally 
`LOG_CHANNEL` | Input Log Group/Channel ID (bot must be an admin in target group or channel)
`DATABASE_URL` | input valid Mongodb Database Url
---


### Anime branch 

__Customized To work Specifically For Animes!__

### Commands
---
```
start - Check If Bot Is Awake
restart - ☢️ Restart Bot 
bash - /bash + command 
eval - Evaluate code
peval - same as eval but with pyrogram 
ping - Ping!
queue - List queue
encodequeue - List queue (parsed)
fix - Turn V2 On (With Message) or Off
get - Get Current ffmpeg code
set - Set custom ffmpeg code
reset - Reset default ffmpeg code
filter - Filter & stuff
vfilter - View filter
groupenc - Allow Encoding in Group Toggle 
delfilter - Delete filter
status - 🆕 Get bot's status
showthumb - 🖼️ Show Current Thumbnail
parse - Toggle Parsing with captions 
cancelall - ❌ Clear Cached Downloads & Queued Files
clear - Clear Queued Files
logs - Get Bot Logs
help - Get Detailed Help
```

### Features:
__(Coming Soon)__

### Source 

- **[An Heavily Modified Fork of Danish CompressorQueue](https://github.com/1Danish-00/CompressorQueue)**

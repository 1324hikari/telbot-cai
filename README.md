# Telbot-CAI

Telbot-CAI uses the PyCharacterAI library and the python-telegram-bot library.
This program sends and recieves messages to CharacterAI using Telegram.

Please note that this is still in development and you may face issues.

# Installation

1 - Copy this repository
```bash
git clone https://github.com/1324hikari/cai-telbot.git
```

2 - Navigate to the folder and run 
```bash
pip install -r requirements.txt
```

# Setting up the bot

You will need these to set-up the bot:
>CharacterAI Token

>Character ID (The character in CAi that you want to talk with)

>Telegram bot ID

>Telegram USER ID (So that only you can message the bot)



**1 - Getting the Telegram token and creating the bot**

go to Telegram and using botfather, create a new bot. After the bot is
created, it should give you your bot token. Paste this into ```TELEGRAM_BOT_TOKEN```

**2 - Getting the Telegram USER ID**

Use the ''@userinfo'' bot in Telegram to get your USER ID. Paste it
into ```ALLOWED_USER_ID```

**3 - Getting the Charcter ID**

Search for the character you want in CharacterAI (website, not the mobile app)
it should be like ```https://character.ai/chats2?=ID_HERE``` and paste it into
```CHARACTER_ID```

**4 - Getting the Character AI Token**

You can follow [this guide](https://github.com/realcoloride/node_characterai) on
how to get your CharacterAI token. After getting it, paste it on ```CHARACTER_AI_TOKEN```

## Usage

Simply run the program using 
```bash
python3 telbot13.py
```
And the bot should start and log all messages sent and recieved


After running the bot for the first time, send a ```/start``` message to the bot in Telegram.


>NOTE: ONLY SEND ```/start``` ONCE AS CHAT SESSIONS IS SAVED IN A FILE

## Donate to the Project

**Bitcoin (BTC): 1FCCRMqHhn1uheccUNbQKzPy9xg1WVfwui**

**Ethereum (ETH): 0x6187c2b9484274012e209bfa8c34cd5cbb90364e**

**Dogecoin (DOGE):
DH1M64ATHMgTqwrsokjanny6ML1wP3W6TQ**

## Contributing

Please leave a **Star ⭐** and open an issue if you encounter any problems.


**This schizophrenic project is made with love ♥️ somewhere in the Philippines 🇵🇭**

## License
<a rel="license" href="https://opensource.org/licenses/MIT"><img alt="MIT License" src="https://cloud.githubusercontent.com/assets/5456665/18950087/fbe0681a-865f-11e6-9552-e59d038d5913.png" width="60em" height=auto/></a><br/><a href="https://github.com/1324hikari/cai-telbot">Telbot-CAI</a> is licensed under <a rel="license" href="https://opensource.org/licenses/MIT">MIT License</a>.

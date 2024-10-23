# Pets Finder
## Quick start
Clone this repo:
```shell
git clone https://github.com/vladislav-serdyuk/Pets_Finder
```
Install requirements:
```shell
pip install -r requirements.txt
```
Create .env file:
```
# vk token
user_token = 'vk1.a.blablabla'

tg_token = '1234567890:abcdefghijknlmopqrstuvwxyz'  # telegram bot token

wallet_addr = '1488abracadabra52'  # cripto wallet address
```
or setup environment variable:
```shell
export user_token='vk1.a.blablabla'
export tg_token='1234567890:abcdefghijknlmopqrstuvwxyz'
export wallet_addr='1488abracadabra52'
```

And run:
```shell
python bot.py
```

## Use
### Setup use vk
Open config.py and edit walls_domain:
```python
walls_domain = [
    'gefundendog',              # vk.com/gefundendog
    'poiskzhivotnykh',          # vk.com/poiskzhivotnykh
    'obyavleniyaozhivotnykh',   # vk.com/obyavleniyaozhivotnykh
    'poteryashkamoskva',        # vk.com/poteryashkamoskva
]
```

### Remove cache
```shell
rm -rf cache/vk_walls/*
```

### Clear logs
```shell
echo -n > log.txt
```

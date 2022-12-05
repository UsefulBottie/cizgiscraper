from bs4 import BeautifulSoup
import requests
from pyrogram import Client,filters

api_id = 18009375
api_hash = '1c6b8b0a259aa35affee58377c634eeb'
bot_token = '5617260708:AAG9EeZy1rH5DpxICPVucptLGrSMAojK6Sc'
chatID = -1001716483713

headers = {
'pragma': 'no-cache',
'cache-control': 'no-cache',
'dnt': '1',
'upgrade-insecure-requests': '1',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-dest': 'document',
}


app = Client(
    "Scrape",
api_id = 18009375,
api_hash = "1c6b8b0a259aa35affee58377c634eeb",
bot_token = "5617260708:AAG9EeZy1rH5DpxICPVucptLGrSMAojK6Sc"
)

url = "https://cizgivedizi.fandom.com/tr/wiki/RedaKai_1.Sezon_1.Bölüm_Türkçe_İzle"

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "html.parser")

with open("test.html", "w", encoding="utf-8") as file:
    file.write(soup.prettify())
image = soup.find("a", {"class": "image image-thumbnail"})
image = image.find("img").get("src")
link = soup.find_all("iframe")
name = soup.find("h2", {"class": "pi-item pi-item-spacing pi-title pi-secondary-background"}).text

@app.on_message(filters.command('image') | filters.private)
async def echo(client, message):
    await app.send_photo(message.chat.id, photo=image, caption=name + "\n" + str(link))


app.run()


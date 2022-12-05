# from bs4 import BeautifulSoup
# import request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium import webdriver
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


async def getData(content, season, totalEpisodes, message):
    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    option.add_argument("--headless")
    browser = webdriver.Chrome(executable_path=driver_path, options=option)
    await app.send_message(message.chat.id, text = f"📁 Çekilen İçerik: {content}\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}\n{message.from_user.mention}")
    for episode in range(1,totalEpisodes+1):
        url = f"https://cizgivedizi.fandom.com/tr/wiki/{content}_{season}.Sezon_{episode}.Bölüm_Türkçe_İzle"
        browser.get(url)
        link = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/p[4]/span/iframe').get_attribute('src')
        name = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/h2').text
        await app.send_message(message.chat.id, text = f"```{link} | {content} {season}. Sezon {episode}. Bölüm - {name}```")
    await app.send_message(message.chat.id, text = f"Hey {message.from_user.mention}!\n📁 {content} İçeriği Çekildi!\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}")

app = Client(
    "Scrape",
api_id = 18009375,
api_hash = "1c6b8b0a259aa35affee58377c634eeb",
bot_token = "5617260708:AAG9EeZy1rH5DpxICPVucptLGrSMAojK6Sc"
)

driver_path = "./chromedriver.exe"
brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser\Application/brave.exe'


@app.on_message(filters.command('getlink') | filters.private)
async def echo(client, message):
    content = input("Enter the content name: ")
    totalEpisodes = int(input("Enter the total episode: "))
    season = int(input("Enter the season: "))
    await getData(content, season, totalEpisodes, message)

app.run()


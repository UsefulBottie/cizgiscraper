from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium import webdriver
import selenium.common.exceptions
from pyrogram import Client,filters, enums
import pyromod.listen
import os

html = enums.ParseMode.HTML

# headers = {
# 'pragma': 'no-cache',
# 'cache-control': 'no-cache',
# 'dnt': '1',
# 'upgrade-insecure-requests': '1',
# 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'sec-fetch-site': 'none',
# 'sec-fetch-mode': 'navigate',
# 'sec-fetch-dest': 'document',
# }


async def getData(content, season, totalEpisodes, message):
    missingEpisodes = []
    browser = webdriver.Chrome("/opt/render/project/src/webdriver.exe",options=option)
    url = f"https://cizgivedizi.fandom.com/tr/wiki/{content}_1.Sezon_1.Bölüm_Türkçe_İzle"
    browser.get(url)
    try: 
        pic = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/figure/a/img').get_attribute('src')
    except selenium.common.exceptions.NoSuchElementException:
        pic = "https://telegra.ph/file/18c4a300239fe7a06cd97.jpg"
    await app.send_photo(message.chat.id, photo= pic, caption= f"📁 İçerik: {content}\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}", parse_mode=html)
    await app.pin_chat_message(chat_id=message.chat.id,message_id=message.id + 7, both_sides=True)
    for episode in range(1,totalEpisodes+1):
        url = f"https://cizgivedizi.fandom.com/tr/wiki/{content}_{season}.Sezon_{episode}.Bölüm_Türkçe_İzle"
        browser.get(url)
        try:
            link = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/p[4]/span/iframe').get_attribute('src')
            name = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/h2').text
            await app.send_message(message.chat.id, text = f"<code>{link} | {content} {season}. Sezon {episode}. Bölüm - {name}</code>", parse_mode=html)
        except selenium.common.exceptions.NoSuchElementException:
            await app.send_message(message.chat.id, text = f"{episode}. Bölüm Bulunamadı!")
            missingEpisodes.append(episode)
    await app.send_message(message.chat.id, text = f"Hey {message.from_user.mention}!\n📁 {content} Hazır!\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}\n🤔 Eksik Bölümler: {missingEpisodes}", parse_mode=html)

app = Client(
    "Scrape",
api_id = 18009375,
api_hash = "1c6b8b0a259aa35affee58377c634eeb",
bot_token = "5617260708:AAG9EeZy1rH5DpxICPVucptLGrSMAojK6Sc"
)

option = webdriver.ChromeOptions()
option.add_argument("--headless")



@app.on_message(filters.command('getlink') | filters.private)
async def echo(client, message):
    await app.send_message(-1001716483713,f"Path: {os.getcwd()}")
    await app.send_message(-1001716483713,f"Path: {os.listdir("/opt/render/project/src/")}")
    
    content = await client.ask(message.chat.id, '<em>Enter the content name:</em>', parse_mode=html)
    totalEpisodes = await client.ask(message.chat.id, '<em>Enter the total episode:</em>', parse_mode=html)
    season = await client.ask(message.chat.id, '<em>Enter the season:</em>', parse_mode=html)
    await getData(content.text, int(season.text), int(totalEpisodes.text), message)

app.run()

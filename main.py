from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium import webdriver
import selenium.common.exceptions
from pyrogram import Client,filters, enums
import pyromod.listen
import sys, time, os

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
async def progress(current, total):
    print(f"Yüklenen: {current * 100 / total:.1f}%")

async def getData(content, season, totalEpisodes, thumb, startIndex, message, client):
    missingEpisodes = []
    browser = webdriver.Chrome(options=options)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
    url = f"https://cizgivedizi.fandom.com/tr/wiki/{content}_1.Sezon_1.Bölüm_Türkçe_İzle"
    browser.get(url)
    try: 
        pic = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/figure/a/img').get_attribute('src')
    except selenium.common.exceptions.NoSuchElementException:
        pic = "https://telegra.ph/file/18c4a300239fe7a06cd97.jpg"
    await app.send_photo(message.chat.id, photo= pic, caption= f"📁 İçerik: {content}\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}", parse_mode=html)
    await app.pin_chat_message(chat_id=message.chat.id,message_id=message.id + 11, both_sides=True)
    for episode in range(startIndex,totalEpisodes+1):
        url = f"https://cizgivedizi.fandom.com/tr/wiki/{content}_{season}.Sezon_{episode}.Bölüm_Türkçe_İzle"
        browser.get(url)
        try:
            link = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/p[4]/span/iframe').get_attribute('src')
            name = browser.find_element(By.XPATH, '//*[@id="mw-content-text"]/div/aside/h2').text          
            # await app.send_message(message.chat.id, text = f"<code>{link} | {content} {season}. Sezon {episode}. Bölüm - {name}</code>", parse_mode=html)
            b = await app.send_message(message.chat.id, text = f"Downloading Episode: {episode}...")
            filename = f"{content} S{season}E{episode} - {name}"+ ".mp4"
            
            os.system(f'yt-dlp "{link.replace("share=0","")}" -v -o "{filename}"')
            q = await app.send_message(message.chat.id, text = f"Uploading...")
            await app.send_video(message.chat.id,progress= progress,video= filename,caption= f"{content} {season}. Sezon {episode}. Bölüm - {name}", supports_streaming = "True", thumb=thumb)
            await app.delete_messages(message.chat.id, q.id)
            await app.delete_messages(message.chat.id, b.id)
        except selenium.common.exceptions.NoSuchElementException:
            await app.send_message(message.chat.id, text = f"{episode}. Bölüm Bulunamadı!")
            missingEpisodes.append(episode)
    await app.send_message(message.chat.id, text = f"Hey {message.from_user.mention}!\n📁 {content} Hazır!\n📹 Sezon: {season}\n📼 Toplam Bölüm: {totalEpisodes}\n🤔 Eksik Bölümler: {missingEpisodes}", parse_mode=html)
    
    # selection = await client.ask(message.chat.id, '<em>Do you want to download? (Y/N)</em>', parse_mode=html)
    # if selection.text == "Y" or selection.text == "y":
    #     for episodee in range(1,totalEpisodes+1):
    #         que = await app.send_message(message.chat.id, text = f"Downloading Episode: {episodee}...")
    #         filename = f"{content} S{season}E{episodee} - {name}"+ ".mp4"
    #         # ydlp_opts = {'output': "./filename.mp4", 'outtpml': './' + "filename.mp4"}
    #         # yt_dlp.YoutubeDL(ydlp_opts).download({link.replace('share=0','')})
    #         os.system(f'yt-dlp "{link.replace("share=0","")}" -v -o "{filename}"')
    #         await app.edit_message_text(message.chat.id, message_id= que.id, text = f"Uploading...")
    #         await app.send_video(message.chat.id,progress= progress, duration=get_length("./"+filename),video= filename, caption= f"{content} {season}. Sezon {episodee}. Bölüm - {name}", supports_streaming = "True", thumb="./redakai.jpg")
    #     await client.send_message(message.chat.id, text = "Downloaded!")
    # else:
    #     await client.send_message(message.chat.id, text = "Bye!")

app = Client(
    "Scrape",
api_id = 18009375,
api_hash = "1c6b8b0a259aa35affee58377c634eeb",
bot_token = "5655890908:AAHd9UwlPRCdiERPkwH7e0aI3vlVoB8oYys"
)

driver_path = "./chromedriver.exe"
brave_path = 'C:/Program Files/BraveSoftware/Brave-Browser\Application/brave.exe'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
#overcome limited resource problems
options.add_argument('--disable-dev-shm-usage')
options.add_argument("lang=en")
#open Browser in maximized mode
#disable infobars
options.add_argument("disable-infobars")
#disable extension
options.add_argument("--disable-extensions")
options.add_argument("--disable-blink-features=AutomationControlled")

@app.on_message(filters.command('getcontent') | filters.private)
async def echo(client, message):
    thumbLink = await client.ask(message.chat.id, '<em>Thumb:</em>', parse_mode=html)
    from pySmartDL import SmartDL
    obj = SmartDL(thumbLink.text, progress_bar=True, dest="./")
    obj.start()
    thumb = obj.get_dest()
    content = await client.ask(message.chat.id, '<em>Enter the content name:</em>', parse_mode=html)
    startIndex = await client.ask(message.chat.id, '<em>Starting Episode:</em>', parse_mode=html)
    totalEpisodes = await client.ask(message.chat.id, '<em>Enter the total episode:</em>', parse_mode=html)
    season = await client.ask(message.chat.id, '<em>Enter the season:</em>', parse_mode=html)
    await getData(content.text, int(season.text), int(totalEpisodes.text),thumb, int(startIndex.text), message, client)

app.run()

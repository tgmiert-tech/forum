import asyncio
import os
from telethon import TelegramClient, events

API_ID = 2040
API_HASH = 'b18441a1ff607e10a989891a5462e627'

spamming = False
spam_chat = None

def load_text():
    file_path = os.path.join(os.path.dirname(__file__), 'text.txt')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(" text.txt не найден!")
        return []
    
    sentences = [line.strip() for line in lines if line.strip()]
    
    if sentences:
        print(f" Загружено {len(sentences)} фраз")
    
    return sentences

client = TelegramClient('my_session', API_ID, API_HASH)
sentences = load_text()

@client.on(events.NewMessage(pattern=r'^\.spam$'))
async def start_spam(event):
    global spamming, spam_chat
    
    await event.delete()
    
    if spamming:
        return
    
    if not sentences:
        return
    
    spamming = True
    spam_chat = event.chat_id
    
    print(f"\n Спам запущен в чате {spam_chat}")
    
    while spamming:
        for sentence in sentences:
            if not spamming:
                break
            try:
                await client.send_message(spam_chat, sentence)
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                spamming = False
                break

@client.on(events.NewMessage(pattern=r'^\.stop$'))
async def stop_spam(event):
    global spamming
    
    await event.delete()
    
    if not spamming:
        return
    
    spamming = False
    print("\n⏹ Спам остановлен")

async def main():
    await client.start()
    print("Вход выполнен!")
    print(f" {await client.get_me()}")
    print("\n Управление:")
    print("   .spam - начать")
    print("   .stop - остановить")
    print("="*40)
    print(" Ожидание команд...\n")
    
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n Пока!")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        input("Нажми Enter...")

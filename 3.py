from telethon import TelegramClient, events
from elasticsearch import Elasticsearch
import socks

es = Elasticsearch('http://localhost:9200')

api_id = 20404256
api_hash = '7ca51ccca81f9973bd2e0adbbd45d88a'
client = TelegramClient('milad', api_id, api_hash, proxy=(socks.SOCKS5, '127.0.0.1', 1080))

@client.on(events.NewMessage('ina_hw2_test'))
async def my_event_handler(event):
    print(event.text, event.id)

    doc = {
        'ID': event.id,
        'DATE': event.date,
        'TEXT': event.text,

    }
    resp = es.index(index="q4", id=event.id, document=doc)
    print(resp['result'])

    if resp['result'] == "created" or resp['result'] == "updated":
        await client.send_message('ina_hw2_test', 'your message successfully saved in database', reply_to=event.id)


client.start()
client.run_until_disconnected()

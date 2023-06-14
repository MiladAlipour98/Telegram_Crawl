from telethon import TelegramClient
from elasticsearch import Elasticsearch
import socks



es = Elasticsearch('http://localhost:9200')

api_id = 20404256
api_hash = '7ca51ccca81f9973bd2e0adbbd45d88a'
client = TelegramClient('milad', api_id, api_hash, proxy=(socks.SOCKS5, '127.0.0.1', 1080))


async def main():
    me = await client.get_me()
    print(me.stringify())
    username = me.username
    print(username)
    print(me.phone)

    num = 0
    async for dialog in client.iter_dialogs():
        print(dialog.id, dialog.name, dialog.date, dialog.title)
        num = num + 1
        print(num)
        strq = str(dialog.message.from_id)
        doc = {
            'ID': dialog.id,
            'NAME': dialog.name,
            'DATE': dialog.date,
            'TITLE': dialog.title,
            'TEXT': dialog.message.text,
            'FROM': strq,
        }

        resp = es.index(index='q2', id=num, document=doc)

        print(resp['result'])

    rec = es.get(index='q2', id=num)
    print(rec['_source'])


with client:
    client.loop.run_until_complete(main())

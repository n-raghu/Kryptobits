import random
import asyncio as aio

from fastapi import FastAPI
from pydantic import BaseModel


get_id = '/api/v1/getid'
get_pass = '/api/v1/getpass'
app = FastAPI()
key_pass_list = [
    {
        'uid': 'uid1',
        'pass': 'pass1'
    },
    {
        'uid': 'uid2',
        'pass': 'pass2'
    },
    {
        'uid': 'uid3',
        'pass': 'pass3'
    },
]
id_list = [_['uid'] for _ in key_pass_list]


class KeyDoc(BaseModel):
    uid: str


async def key_pass(uid):
    for keypair in key_pass_list:
        if keypair['uid'] == uid:
            return keypair
    return {uid: 'Key not Found'}


@app.get(get_pass)
async def get_pvt(key_doc: KeyDoc):
    uid = key_doc.uid
    print('uid :' + uid)
    done = set()
    try:
        done, pending = await aio.wait([key_pass(uid)])
    except Exception as err:
        print(err)

    if done:
        for task in done:
            return task.result()
    return None


@app.get(get_id)
async def get_pub():
    return random.choice(id_list)


@app.get("/")
async def root():
    return {"message": "Test-AIO"}

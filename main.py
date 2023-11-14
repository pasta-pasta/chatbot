
from group_setup import Group
import panopticon
import asyncio
import atexit


panopt = panopticon.Panopticon("vk1.a.SH1U4eNrwujUpiy9ladVCNeJDh3uatKYdhHAMknEk4pyEZrYUIqPwXhYgBZF79F-tbNhSnYt2XP_lxBUz4BFo9E02mPrVNRNTeFxSdAdU-E0ytZizpXexd4j0mvJLkoKKnallKTDogOy_95qp-5S0EHa4aOHZlZKQevDcjqyCR4ApXDkXlX3JEkS5GZDAY420cDqwqEv7fqwKUWKJ1uwyg"
)
asyncio.run(panopt.init())


def handle(data):
    asyncio.run(panopt.listener.handle_update(data))

def Shutdown(module):
    asyncio.run(module.shutdown())


atexit.register(Shutdown, panopt)

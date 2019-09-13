import asyncio
import time


async def myfun(i):
    print('start {}th'.format(i))
    await asyncio.sleep(1)
    print('finish {}th'.format(i))

    loop = asyncio.get_event_loop()
    myfun_list = (myfun(i) for i in range(10))
    loop.run_until_complete(asyncio.gather(*myfun_list))

def agt(*test):
    print(test)
    for item in test:
        print(item)

if __name__ == "__main__":
    a = [1, 2, 3, 4, 5]
    agt(10, "20", 30)

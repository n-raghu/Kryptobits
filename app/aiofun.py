import asyncio as aio

async def find_divisibles(inrange, div_by):
    print("finding nums in range {} divisible by {}".format(inrange, div_by))
    located = 0
    for i in range(inrange):
        if i % div_by == 0:
            located += 1
            await aio.sleep(0.000000001)
    print("Done w/ nums in range {} divisible by {}".format(inrange, div_by))
    return located

async def main(loop):
    divs1 = loop.create_task(find_divisibles(508000, 9))
    divs2 = loop.create_task(find_divisibles(100052, 4))
    divs3 = loop.create_task(find_divisibles(500, 31))
    return await aio.wait([divs1, divs2, divs3])

'''
loop = aio.get_event_loop()
loop.run_until_complete(main())
loop.close()
'''
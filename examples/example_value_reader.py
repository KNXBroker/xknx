import asyncio
from xknx import XKNX, ValueReader
from xknx.knx import Address


async def main():
    xknx = XKNX()
    await xknx.start()

    value_reader = ValueReader(xknx, Address('6/2/1'))
    telegram = await value_reader.read()
    if telegram is not None:
        print(telegram)

    await xknx.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
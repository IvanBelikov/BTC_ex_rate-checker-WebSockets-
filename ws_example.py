import websockets
import asyncio
import json
from datetime import datetime

import matplotlib.pyplot as plt

x_data = []
y_data = []

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()


def update_graph(tm, current_value):
    x_data.append(tm)
    y_data.append(current_value)
    ax.plot(x_data, y_data)

    fig.canvas.draw()
    plt.pause(0.05)


async def main():
    url = "wss://stream.binance.com/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client:
        while True:
            data = json.loads(await client.recv())['data']
            current_value = round(float(data['c']), 2)
            tm = datetime.fromtimestamp(data['E'] // 1000)
            update_graph(tm, current_value)

            print(f"{tm} -> {round(float(data['c']), 2)}$")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


from collections import deque
import aioredis
import asyncio
import atexit
import os
import logging
import json

class RedisClient():
    def __init__(self, queue_size=20):
        self.queue_size = deque(maxlen=queue_size)
        self.redis = None
        self.sub_topics = []
        self.logger = logging.getLogger()

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.init_client())

    async def init_client(self):
        self.redis = await aioredis.create_redis_pool(os.environ.get("REDIS_URI"))
        while True:
            await self.send_message()
            await asyncio.sleep(1)

    def publish(self, key, message):
        self.queue_size.append([key, message])

    async def send_message(self):
        try:
            key, msg = self.queue_size.pop()
            await self.redis.rpush(key, msg)
        except IndexError:
            self.logger.info("[REDIS] Empty messaging queue, ignoring it....")

    async def _get_message(self, key):
        msg = await self.redis.lpop(key)
        return json.loads(msg)

    async def subscribe(self, topic, callback):
        res = await self.redis.subscribe(topic)
        self.sub_topics.append(topic)
        ch = res[0]
        while (await ch.wait_message()):
            msg = await ch.get_json()
            callback(msg)

    def get(self, key):
        value = self.redis.get(key)
        return value

    async def set_key(self, key, value):
        await self.redis.set(key, value)

    @atexit.register
    async def close(self):
        self.logger.info("[REDIS] Unsubscribing channels...")
        for topic in self.sub_topics:
            await self.redis.unsubscribe(topic)
        self.logger.info("[REDIS] Closing connection...")
        # gracefully closing underlying connection
        self.redis.close()
        await self.redis.wait_closed()
        self.logger.info("[REDIS] Connection closed!")

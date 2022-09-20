import aiosqlite

class DB:

    async def initialize(self):
        self.db = await aiosqlite.connect("./database.db")

    async def execute(self, sql: str):
        await self.db.execute(sql)
        await self.db.commit()
        return self.db.total_changes

    async def fetch_one(self, sql: str):
        try:
            cursor = await self.db.execute(sql)
            return await cursor.fetchone()
        finally:
            await cursor.close()

    async def fetch_all(self, sql: str):
        try:
            async with self.db.execute(sql) as cursor:
                async for row in cursor:
                    yield row
        finally:
            await cursor.close()

    async def close(self):
        await self.db.close()

    @staticmethod    
    async def prepare_database():
        db = DB()
        await db.initialize()
        await db.execute("CREATE TABLE IF NOT EXISTS logs (consumer_id VARCHAR(255), service_name VARCHAR(255), service_id VARCHAR(255), request_time INTEGER, proxy_time INTEGER, gateway_time INTEGER)")
        await db.close()
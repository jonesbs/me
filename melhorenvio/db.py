import aiosqlite

class DB:

    async def initialize(self):
        self.db = await aiosqlite.connect("./database.db")

    async def execute(self, sql: str, parameters=None):
        await self.db.execute(sql, parameters)
        await self.db.commit()
        return self.db.total_changes

    async def fetch_all(self, sql: str):
        async with self.db.execute(sql) as cursor:
            async for row in cursor:
                yield row

    async def close(self):
        await self.db.close()

    @staticmethod    
    async def prepare_database():
        db = DB()
        await db.initialize()
        await db.execute("CREATE TABLE IF NOT EXISTS logs (consumer_id VARCHAR(255), service_name VARCHAR(255), service_id VARCHAR(255), request_time INTEGER, proxy_time INTEGER, gateway_time INTEGER)")
        await db.close()
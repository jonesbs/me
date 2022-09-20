import asyncio
import csv
from db import DB

class Report:

    def __init__(self, filename) -> None:
        self.filename = filename

    async def create_report(self, prefix, header, sql):
        with open(f"{prefix}-{self.filename}", "w") as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow(header)
            async for line in self.db.fetch_all(sql):
                writer.writerow(line)


    async def process(self):
        self.db = DB()
        await self.db.initialize()
        map_report = [
            ("consumer", ["Consumidor ID", "Total de requisições"], "SELECT consumer_id, COUNT(*) as total FROM logs GROUP BY consumer_id ORDER BY total ASC"),
            ("service", ["Serviço ID", "Serviço Nome", "Total de requisições"], "SELECT service_id, service_name, COUNT(*) FROM logs GROUP BY service_id ORDER BY service_name ASC"),
            ("average", ["Serviço ID", "Serviço Nome", "Tempo médio request (ms)", "Tempo médio proxy (ms)", "Tempo médio gateway (ms)"], "SELECT service_id, service_name, AVG(request_time), AVG(proxy_time), AVG(gateway_time) FROM logs GROUP BY service_id ORDER BY service_name ASC")
        ]

        await asyncio.gather(*[self.create_report(prefix, header, sql) for prefix, header, sql in map_report])
        await self.db.close()
        return True
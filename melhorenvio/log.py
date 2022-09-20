import asyncio
import json
from progress.bar import ChargingBar
from db import DB

class Log:
    

    def get_total_lines_file(self, file_path):
        return sum(1 for i in open(file_path, 'r'))

    def read_log(self, filename):
        with open (filename, mode="r") as reader:
            while reader:
                line = reader.readline().strip()
                if not line:
                    break

                yield json.loads(line)

    async def save_log_line(self, request, db):
        consumer_id = request['authenticated_entity']['consumer_id']['uuid']
        service_id = request['service']['id']
        service_name = request['service']['name']
        request_time = request['latencies']['request']
        proxy_time =request['latencies']['proxy']
        gateway_time =request['latencies']['kong']
        await db.execute("INSERT INTO logs (consumer_id, service_id, service_name, request_time, proxy_time, gateway_time) VALUES (?, ?, ?, ?, ? ,?)", parameters=(consumer_id, service_id, service_name, request_time, proxy_time, gateway_time))
        return True

    def chunk_generator(self, line_generator, size):
        out_list = []
        i = 0
        for item in line_generator:
            out_list.append(item)
            i += 1
            if i == size:
                yield out_list
                out_list = []
                i = 0

        yield out_list

    async def process(self, file_path):
        db = DB()
        await db.initialize()
        chunk_size = 30

        
        total_lines = self.get_total_lines_file(file_path)
        with ChargingBar('Importing', max=total_lines) as bar:
            for list_items in self.chunk_generator(self.read_log(file_path), chunk_size):
                await asyncio.gather(*[self.save_log_line(item, db) for item in list_items])
                bar.next(chunk_size)

        await db.close()   
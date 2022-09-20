import asyncio
import argparse

from db import DB
from log import Log
from report import Report

async def parse_cli():

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help="Path to log JSON informations")
    parser.add_argument("-r", help="Report output name file")
    parser.add_argument("-p", help="Initialize database schema", action='store_true')
    response = vars(parser.parse_args())
    
    if "l" in response and response["l"]:
        l = Log()
        await l.process(response["l"])
        print("Insert process completed")

    if "r" in response and response["r"]:
        r = Report(response["r"])
        await r.process()
        print("Report generated")

    if "p" in response and response["p"]:
        await DB.prepare_database()
        print("Database ready")
    
    return None

if __name__ == "__main__":
    asyncio.run(parse_cli())
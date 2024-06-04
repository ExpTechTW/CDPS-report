import json
import random
import time

import requests
import urllib3

from cdps.plugin.manager import Manager
from cdps.plugin.thread import new_thread
from cdps.utils.logger import Log
from plugins.report.src.events import onReport

urllib3.disable_warnings()


@new_thread
def get_report():
    reports = []
    with open("./config/report.json", 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    url = f"https://api-{random.randint(1,2)}.exptech.dev/api/v2/eq/report?limit={config['limit']}"
    while True:
        data = []
        try:
            data = requests.get(url, timeout=5)
        except Exception as e:
            log.logger.warning(f"取得地震資料發生錯誤\n{e}")
            time.sleep(config["timeout"])
            continue
        try:
            data = (json.loads(data.text))
        except Exception as e:
            log.logger.warning(f"解析地震資料發生錯誤\n{e}")
            time.sleep(config["timeout"])
            continue

        if data != []:
            if reports == []:
                reports = data
                event_manager.call_event(onReport(reports, True))
            elif data != reports:
                if data[0]["time"] > reports[0]["time"]:
                    reports = data
                    event_manager.call_event(onReport(reports, False))
        time.sleep(config["timeout"])


log = Log()
event_manager = Manager()
get_report()
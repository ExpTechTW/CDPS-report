from cdps.plugin.manager import Manager, Listener
from cdps.plugin.events import onServerStartEvent
from cdps.utils.logger import Log
from plugins.report.src.events import onReport
import json
import random
import requests
import time
import threading
import urllib3

urllib3.disable_warnings()


class onServerStartListener(Listener):
    event = onServerStartEvent

    def on_event(self, event):
        print(event.pid)


def get_report(stop_event):
    reports = []
    url = f"https://api-{random.randint(1,2)}.exptech.dev/api/v2/eq/report?limit={time.sleep(config["limit"])}"
    with open("./config/report.json", 'r', encoding='utf-8') as f:
        config = json.loads(f.read())
    while not stop_event.is_set():
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


def task(stop_event):
    task_thread_1 = threading.Thread(target=get_report, args=(stop_event,))
    task_thread_1.start()


log = Log()
event_manager = Manager()
event_manager.register_listener(onServerStartListener())

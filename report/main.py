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
    url = f"https://api-{random.randint(1,2)}.exptech.dev/api/v2/eq/report?limit=50"
    while not stop_event.is_set():
        time.sleep(2)
        data = []
        try:
            data = requests.get(url, timeout=5)
        except Exception as e:
            log.logger.warning(f"取得地震資料發生錯誤\n{e}")
            continue
        try:
            data = (json.loads(data.text))
        except Exception as e:
            log.logger.warning(f"解析地震資料發生錯誤\n{e}")
            continue

        if data != []:
            if reports == []:
                reports = data
                event_manager.call_event(onReport(reports, True))
            elif data != reports:
                if data[0]["time"] > reports[0]["time"]:
                    reports = data
                    event_manager.call_event(onReport(reports, False))


def task(stop_event):
    task_thread_1 = threading.Thread(target=get_report, args=(stop_event,))
    task_thread_1.start()


log = Log()
event_manager = Manager()
event_manager.register_listener(onServerStartListener())
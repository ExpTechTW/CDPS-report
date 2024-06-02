from cdps.plugin.manager import Manager
from plugins.report.src.events import onReport

event_manager = Manager()

event_manager.call_event(onReport("report",True))
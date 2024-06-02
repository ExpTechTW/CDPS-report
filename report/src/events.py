from cdps.plugin.events import Event


class onReport(Event):
    """ 當 伺服器 啟動 """

    def __init__(self, data:list, init:bool):
        self.report = data #地震報告資料
        self.init = init #是否為初次啟動

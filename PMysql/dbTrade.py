from PMysql.dbTable import DB_table

class DB_trade(DB_table):

    def __init__(self, dataList):           # the parameter could be a tuple
        super().__init__()
        self.setData(list(dataList))

    def defineNames(self):
        self.tname = "Trade"
        ar = ['id','acct', 'description', 'symbol', 'long_short','open_closed', 'dt_open', 'dt_close',
             'risk', 'net', 'spread', 'strategy', 'outcome', 'verdict']
        self.setNames(ar)

    def updateList(self):
        sql = "acct = " + '"' + self.data[1] + '", '
        sql += "description = " + '"' + self.data[2] + '", '
        sql += "symbol = " + '"' + self.data[3] + '", '
        sql += "long_short = " + '"' + self.data[4] + '", '
        sql += "open_closed = " + '"' + self.data[5] + '", '
        sql += "dt_open = " + '"' + self.data[6] + '", '
        sql += "dt_close = " + '"' + self.data[7] + '", '
        sql += "risk = " + self.data[8] + ', '
        sql += "net = " + self.data[9] + ', '
        sql += "spread = " + '"' + self.data[10] + '", '
        sql += "strategy = " + '"' + self.data[11] + '", '
        sql += "outcome = " + '"' + self.data[12] + '", '
        sql += "verdict = " + '"' + self.data[13] + '" '
        return sql
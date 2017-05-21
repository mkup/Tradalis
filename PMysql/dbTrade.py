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

from PMysql.dbTable import DB_table

class DB_transaction(DB_table):
    """ Class to hold a Transaction table row """

    def __init__(self, dataList):           # the parameter could be a tuple
        super().__init__()
        self.setData(list(dataList))

    def defineNames(self):
        self.tname = "Transaction"
        ar = ['id', 'dt', 'vendorId', 'description', 'quantity', 'symbol', 'price', 'commission', 'net_cash',
                      'instrument', 'expiration', 'strike', 'trade', 'acct']
        self.setNames(ar)

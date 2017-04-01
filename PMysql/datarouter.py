from PMysql.dbTable import DB_table
from PMysql.dbTransaction import DB_transaction
from env.Persistence import Persistence


class Getter(object):

    def getTrades(self, fr=None, to=None):
        """Queries database for Trades, converts it to trade object, returns trade collections
            Staggering, if necessary, should be implemented here"""
        # construct sql
        sql = "select * from trades"
        tdCol = DB_table.select(sql)
        tradeCol = [Persistence.P.mapper.unmarshallTrades(t) for t in tdCol]
        return tradeCol

    def getTransactions(self, trade=0):
        """Queries database for Transactions, converts it to positions, returns position collections
            Staggering, if necessary, should be implemented here"""
        # construct sql
        sql = "select * from Transactions where trade = " + trade
        data = DB_table.select(sql)
        posCol = [Persistence.P.mapper.unmarshallTransaction(DB_transaction(t)) for t in data]
        return posCol

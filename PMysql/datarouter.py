from PMysql.dbTable import DB_table
from PMysql.dbTransaction import DB_transaction
from env.Persistence import Persistence


class Getter(object):

    def __init__(self):
        self.map = None

    def getMap(self):
        if not self.map:
            self.map = Persistence.P.mapper
        return self.map

    def getTrades(self, account, state=None, fr=None, to=None, order=None):
        """Queries database for Trades, converts it to trade object, returns trade collections
            Staggering, if necessary, should be implemented here"""
        # construct sql
        sql = "select * from Trade where acct = " + account
        if state:
            sql += " open_close = " + state
        if fr:
            sql += " and dt_open >= " + fr
        if to:
            sql += " and dt_close <= " + to
        if order:
            sql += " order by " + order
        tdCol = DB_table.select(sql)
        tradeCol = [self.getMap().unmarshalTrades(t) for t in tdCol]
        return tradeCol

    def getTransactions(self, account, trade, order):
        """Queries database for Transactions, converts it to positions, returns position collections
            Staggering, if necessary, should be implemented here"""
        # construct sql
        sql = "select * from Transaction where"
        sql += " acct = " + account
        sql += " and trade = " + str(trade)
        if order:
            sql += " order by " + order
        data = DB_table.select(sql)
        tranCol = [self.getMap().unmarshallTransaction(DB_transaction(t)) for t in data]
        return tranCol

    def getUnattachedTransactions(self, account):
        return self.getTransactions(account, 0,"symbol, dt, instrument, expiration, strike")

    def getOpenTrades(self, account):
        trades = self.getTrades(account, "OPEN",None,None,order="dt_open")
        for tr in trades:
            tr.tranCol = self.getTransactions(tr.account, tr.id, "symbol, dt, instrument, expiration, strike")
            tr.addTrans(self.tranCol)
        return trades
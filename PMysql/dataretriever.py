from PMysql.dbTable import DB_table
from PMysql.dbTransaction import DB_transaction
from PMysql.dbTrade import DB_trade
from PMysql.dbDic import DB_dic
from env.Persistence import Persistence

dicNames = ['Strategy', 'Outcome']

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
        sql = 'select * from Trade where acct = "' + account + '"'
        if state:
            sql += ' and open_closed = "' + state + '"'
        if fr:
            sql += ' and dt_open >= "' + fr + '"'
        if to:
            sql += ' and dt_close <= "' + to + '"'
        if order:
            sql += ' order by ' + order
        tdCol = DB_table.select(sql)
        tradeCol = [self.getMap().unmarshalTrade(DB_trade(tr)) for tr in tdCol]
        return tradeCol

    def getTransactions(self, account, tradeId, order):
        """Queries database for Transactions, converts it to positions, returns position collections
            Staggering, if necessary, should be implemented here"""
        # construct sql
        sql = "select * from Transaction where"
        sql += ' acct = "' + account + '"'
        if tradeId:
            sql += ' and trade = ' + str(tradeId)
        if order:
            sql += ' order by ' + order
        data = DB_table.select(sql)
        tranCol = [self.getMap().unmarshalTransaction(DB_transaction(t)) for t in data]
        return tranCol

    def getUnattachedTransactions(self, account):
        return self.getTransactions(account, 0, "symbol, dt, instrument, expiration, strike")

    def getOpenTrades(self, account):
        trades = self.getTrades(account, "OPEN",None,None,order="dt_open")
        for tr in trades:
            trans = self.getTransactions(tr.account, tr.id, "symbol, dt, instrument, expiration, strike")
            tr.addTrans(trans)
        return trades

    def insertTrade(self, tr):
        dbTr = self.getMap().marshalTrade(tr)
        i = dbTr.insert()
        tr.id = i
        for tran in [t for t in Persistence.P.changes['tran'] if t.trade == tr]:
            self.updateTransaction(tran, i)
            del Persistence.P.changes['tran'][tran]
        return i

    def updateTransaction(self,tran, i):
        sql = "update Transaction set trade = " + str(tran.id) + " where id = " + str(i)
        DB_table.execute(sql)

    def deleteTrade(self, trade):
        sql = "delete from Trade where id = " + str(trade.id)
        DB_table.execute(sql)

    def updateTrade(self, trade):
        dbTr = self.getMap().marshalTrade(trade)
        dbTr.update()

    def insertDic(self, dic):
        dbDic = self.getMap().marshalDic(dic)
        return dbDic.insert()

    def updateDic(self, dic):
        dbDic = self.getMap().marshalDic(dic)
        return dbDic.update()

    def deleteDic(self, dic):
        dic.active = 0
        dbDic = self.getMap().marshalDic(dic)
        return dbDic.update()

    def getDic(self, nm):
        if nm in dicNames:
            sql = "select * from " + nm
            data = DB_table.select(sql)
            col = [self.getMap().unmarshalDic(DB_dic(d)) for d in data]
            return col
        else:
            return None

    def populateDic(self):
        d = {}
        for nm in dicNames:
            col = self.getDic(nm)
            d[nm] = col
        return d

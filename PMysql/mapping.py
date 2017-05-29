# todo: code and reorganize marshal/un-marshal for Trades and Dictionaries

from coreapp.positions import Position, Option
from coreapp.trade import Trade
from coreapp.dict import Dict
from env.Persistence import Persistence
from PMysql.dbTrade import DB_trade
from PMysql.dbDic import DB_dic


# noinspection PyMethodMayBeStatic
class Map(object):
    def unmarshalTransaction(self, tran):
        """" Translate DB_transaction record to either Position or Option object"""

        if tran.get('instrument') in ('call', 'put'):
            o = Option()
            o.removal = tran.get('description').startswith("Removal")
            o.expiration = tran.get('expiration')
            o.strike = tran.get('strike')
        else:
            o = Position()
        o.id = tran.get('id')
        o.vendorId = tran.get('vendorId')
        o.dt = tran.get('dt')
        o.quantity = tran.get('quantity')
        o.origQty = tran.get('quantity')
        o.symbol = tran.get('symbol')
        o.price = tran.get('price')
        o.comm = tran.get('commission')
        o.net = tran.get('net_cash') + o.comm
        o.instrument = tran.get('instrument')
        o.trade = tran.get('trade')
        o.account = tran.get('acct')
        return o

    def unmarshalTrade(self, dbTr):
        """" Translate DB_trade record to Trade object """
        trade = Trade()
        trade.id = dbTr.getData()[0]
        trade.account = dbTr.getData()[1]
        trade.strategy = dbTr.getData()[11]
        # addTran() populates all the derived attributes
        trade.addTrans(Persistence.P.retriever.getTransactions(trade.account, trade.id, 'dt, instrument, expiration, strike'))
        return trade

    def marshalTrade(self, trade):
        """convert Trade to DB_trade"""
        # todo:  use in the data - trade.spread.display() in place of Spread
        data = [trade.id, trade.account, trade.description, trade.symbol, trade.long_short, trade.open_closed,
                str(trade.dateOpen), str(trade.dateClose), str(trade.risk), str(trade.net), 'Spread', '', '', '']
        dbTr = DB_trade(data)
        return dbTr

    def marshalDic(self, d):
        data = [d.id, d.cde, d.description, d.valid]
        dbD = DB_dic()
        dbD.tname = d.name
        return dbD

    def unmarshalDic(self, dbD):
        d = Dict()
        d.id = dbD[0]
        d.name = dbD.tname
        d.cde = dbD[1]
        d.description = dbD[2]
        d.active = dbD[3]
        return d
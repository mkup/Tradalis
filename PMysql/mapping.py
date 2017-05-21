# todo: code and reorganize marshal/un-marshal for Trades and Dictionaries

from coreapp.positions import Position, Option
from coreapp.trade import Trade
from env.Persistence import Persistence
from PMysql.dbTrade import DB_trade


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

    def unmarshalTrade(self, tr):
        """" Translate DB_trade record to Trade object """
        trade = Trade()
        trade.id = tr.id
        trade.acct = tr.acct
        trade.addTrans(Persistence.P.getter.getTransactions(tr.acct, tr.id, 'dt, instrument, expiration, strike'))
        return trade

    def marshalTrade(self, trade):
        """convert Trade to DB_trade"""

        data = [trade.id, trade.acct, trade.description, trade.symbol, trade.long_short, trade.open_close,
                trade.dateOpen, trade.dateClose, trade.risk, trade.net, trade.spread.display()]
        dbTr = DB_trade(data)
        return dbTr

from env.Env import Env
from apps.proposal import Proposal
from coreapp.trade import Trade


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,
# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class TradeGroup(object):
    @staticmethod
    def tranBelong(tr, lst, t):
        """Determine if the transaction(t) belongs to trade(tr) without altering the tr"""
        if tr.isReal():
            cp = Trade()
            cp.state = tr.state
            cp.addTrans(tr.tranCol+lst, False)
        else:
            cp = tr
        return cp.belong(t)

    def __init__(self, acct):
        self.getter = Env.E.getP().retriever
        self.account = acct

    def getOpenTrades(self, sym):
        return self.getter.getOpenTrades(self.account, sym)

    def unAttachedTrans(self, sym):
        return self.getter.getUnattachedTransactions(self.account, sym)

    # noinspection PyRedundantParentheses
    def groupSingles(self):
        #todo: last transaction is lost
        """Go through un-attached transactions and propose how to attach them to existing and new trades.
           Each proposal can add transactions to an Open trade, or open a new trade"""
        group = []
        singles = self.unAttachedTrans(None)
        propTrade = self.proposeTrade(group)
        propTrade.symbol = singles[0].symbol
        itr = 0
        openTrades = self.getOpenTrades(None)
        if openTrades:
            openTrade = openTrades[itr]
            trend = False
        else:
            trend = True

        for t in singles:
            if propTrade.isReal():
                if TradeGroup.tranBelong(propTrade, group, t):
                    group.append(t)
                else:
                    self.addProposal(propTrade, group)
                    group = []
                    propTrade = self.proposeTrade(group)
            else:
                if not trend and TradeGroup.tranBelong(openTrade, [], t):
                    self.addProposal(propTrade, group)
                    group = [t]
                    propTrade = openTrade
                else:
                    itr += 1
                    if itr < len(openTrades):
                        openTrade = openTrades[itr]
                    else:
                        trend = True
                    if TradeGroup.tranBelong(propTrade, group, t):
                        group.append(t)
                        propTrade.addTransaction(t, False)
                        propTrade.setPlan()
                    else:
                        self.addProposal(propTrade, group)
                        group = [t]
                        propTrade = self.proposeTrade(group)
        self.addProposal(propTrade, group)
    # end of groupSingles()

    def proposeTrade(self, trans):
        trade = Trade()
        trade.account = self.account
        if trans:
            trade.addTrans(trans, False)
            trade.setPlan()
        return trade

    def addProposal(self, trade, trans):
        if trade.tranCol:
            Proposal.addProp(trade, trans)

    def groupSymbol(self, sym, fr, to):
        """Collect all existing trades and transactions for the Symbol within a the time period"""

        trades = self.getter.getTrades(self.account, sym, state=None, fr=fr, to=to, order='dt_open')
        trans = self.unAttachedTrans(sym)
        return trades, trans
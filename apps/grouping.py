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
        self.openTrades = self.getOpenTrades()
        self.singles = self.unAttachedTrans()  # collection of un-attached transactions


    def getOpenTrades(self):
        return self.getter.getOpenTrades(self.account)

    def unAttachedTrans(self):
        return self.getter.getUnattachedTransactions(self.account)

    # noinspection PyRedundantParentheses
    def groupSingles(self):
        """Go through un-attached transactions and propose how to attach them to existing and new trades.
           Each proposal can add transactions to an Open trade, or open a new trade"""
        group = []
        propTrade = self.proposeTrade(group)
        propTrade.symbol = self.singles[0].symbol
        itr = 0
        if self.openTrades:
            openTrade = self.openTrades[itr]
            trend = False
        else:
            trend = True

        for t in self.singles:
            if propTrade.isReal():
                if TradeGroup.tranBelong(propTrade, group, t):
                    group.append(t)
                else:
                    self.addProposal(propTrade, group)
                    group = [t]
                    propTrade = self.proposeTrade(group)
            else:
                if not trend and TradeGroup.tranBelong(openTrade, group, t):
                    self.addProposal(propTrade, group)
                    group = [t]
                    propTrade = openTrade
                else:
                    itr += 1
                    if itr < len(self.openTrades):
                        openTrade = self.openTrades[itr]
                    else:
                        trend = True
                    if TradeGroup.tranBelong(propTrade, group, t):
                        group.append(t)
                        propTrade.addTransaction(t, False)
                    else:
                        self.addProposal(propTrade, group)
                        group = [t]
                        propTrade = self.proposeTrade(group)
    # end of groupSingles()

    def proposeTrade(self, trans):
        trade = Trade()
        trade.account = self.account
        trade.state = "PLAN"
        if trans:
            trade.addTrans(trans, False)
        return trade

    def addProposal(self, trade, trans):
        if trade.tranCol:
            Proposal.addProp(trade, trans)

    def groupSymbol(self, sym, fr, to):
        """Collect all existing trades and transactions for the Symbol within a the time period"""

        trades = self.getter.getTrades(self.account, state=None, fr=fr, to=to, order='dt_open')
        trans = self.unAttachedTrans()
        return trades, trans
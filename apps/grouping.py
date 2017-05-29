from env.Env import Env
from apps.proposal import Proposal
from coreapp.trade import Trade


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,
# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class TradeGroup(object):
    @staticmethod
    def tranBelong(tr, t):
        """Determine if the transaction(t) belongs to trade(tr) without altering the tr"""
        if tr.isReal():
            cp = Trade()
            cp.open_close = tr.open_close
            cp.addTrans(tr.tranCol)
        else:
            cp = tr
        return cp.belong(t)

    def __init__(self, acct):
        self.getter = Env.E.getP().retriever
        self.account = acct
        self.openTrades = self.getOpenTrades()
        self.singles = self.unAttachedTrans()  # collection of un-attached transactions
        self.props = []

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
        itr = 0
        if self.openTrades:
            openTrade = self.openTrades[itr]
            trend = False
        else:
            trend = True

        for t in self.singles:
            if TradeGroup.tranBelong(propTrade, t):
                group.append(t)
                if not propTrade.isReal():
                    propTrade.addTransaction(t)
            else:
                self.addProposal(propTrade, group)
                group = [t]
                propTrade = self.proposeTrade(group)
                if not trend:
                    while not trend and t.symbol > openTrade.symbol:
                        itr += 1
                        if itr < len(self.openTrades):
                            openTrade = self.openTrades[itr]
                        else:
                            trend = True
                    # end-while
                    if propTrade.isReal() or not TradeGroup.tranBelong(openTrade, t):
                        self.addProposal(propTrade, group)
                        group = [t]
                        propTrade = self.proposeTrade(group)
                    else:
                        propTrade = openTrade
                        itr += 1
                        openTrade = self.openTrades[itr]
        # end of loop trough singles
        if propTrade and group:
            self.addProposal(propTrade, group)

    # end of groupSingles()

    def proposeTrade(self, trans):
        trade = Trade()
        trade.account = self.account
        trade.open_closed = "PLAN"
        if trans:
            trade.addTrans(trans)
        return trade

    def addProposal(self, trade, trans):
        prop = Proposal(trade, trans)
        self.props.append(prop)

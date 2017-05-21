from env.Env import Env
from apps.proposal import Proposal
from coreapp.trade import Trade


# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,
# noinspection PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming,PyPep8Naming
class TradeGroup(object):
    @staticmethod
    def proposeTrade(trans):
        trade = Trade()
        trade.open_closed = "PLAN"
        trade.tranCol = trans
        return trade

    @staticmethod
    def tradeBelong(tr, t):
        """Determine if the transaction(t) belongs to trade(tr) without altering the tr"""
        if tr.isReal():
            cp = Trade()
            cp.open_close = tr.open_close
            cp.addTrans(tr.tranCol)
        else:
            cp = tr
        return cp.belong(t)

    def __init__(self, acct):
        self.getter = Env.E.getP().getter
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
        trend = False
        group = []
        propTrade = TradeGroup.proposeTrade(group)
        itr = 0
        openTrade = self.openTrades[itr]
        for t in self.singles:
            if TradeGroup.tradeBelong(propTrade, t):
                group.append(t)
            else:
                self.addProposal(propTrade, group)
                group = [t]
                propTrade = TradeGroup.proposeTrade(group)
                while (not trend and t.symbol > openTrade.symbol):
                    itr += 1
                    if itr < len(self.openTrades):
                        openTrade = self.openTrades[itr]
                    else:
                        trend = True
                # end-while
                if propTrade.isReal() or not TradeGroup.tradeBelong(openTrade, t):
                    self.addProposal(propTrade, group)
                    group = [t]
                    propTrade = TradeGroup.proposeTrade(group)
                else:
                    propTrade = openTrade
                    itr += 1
                    openTrade = self.openTrades[itr]
        # end of loop trough singles
        if propTrade and group:
            self.addProposal(propTrade, group)

    # end of groupSingles()

    def addProposal(self, trade, trans):
        prop = Proposal(trade)
        prop.trans = trans
        self.props.append(prop)

import copy
from decimal import Decimal
from coreapp.spread import Spread
from env.Persistence import Persistence


class Trade(object):
    def __init__(self):
        self.id = 0
        self.account = ''  # account nick (for now)
        self.tranCol = []  # Collection of transactions, uncompressed
        self.posCol = []  # Compressed collection of transaction COPIES
        self.description = ''
        self.symbol = ''  # Derived from the first added transaction
        self.long_short = ''  # ('LONG', 'SHORT') - derived from Spread
        self.state = 'PLAN'  # ('OPEN', 'CLOSED', 'PLAN')
        self.dateOpen = None  # Derived from Spread
        self.dateClose = None  # Derived from Spread
        self.risk = Decimal(0.00)  # Trade initial exposure, derived from Spread
        self.net = Decimal(0.00)  # Derived from Spread
        self.spread = None
        self.strategy = ''
        self.mgmt = None

    def getDescription(self):
        sep = ' '
        ar = [type(self).__name__, str(self.id), self.state, repr(self.spread)]
        self.description = sep.join(ar)
        return self.description

    def __repr__(self):
        return '(' + str(self.id) + ') ' + self.getDescription()

    #   Structural methods
    def getStrategy(self):
        return self.strategy

    def getVerdict(self):
        return self.mgmt.getVerdict()

    def getOutcome(self):
        return self.mgmt.getOutcome()

    #   Application methods
    def belong(self, tran):
        if not tran or not self.matchAccount(tran) or not self.matchSymbol(tran):
            ret = False
        elif not self.tranCol:
            ret = True
        else:
            ret = self.matchPos(tran) is not None or tran.matchDate(self.dateOpen) or \
                    (self.spread and self.spread.isComplement(tran))
        return ret

    def matchAccount(self, t):
        return t and self.account == t.account

    def matchSymbol(self, t):
        return (self.symbol == '') or (self.symbol == t.symbol)

    def matchPos(self, tran):
        """ Determine if a similar transaction exists in the spread.
            Basically, the transaction must be of exact match to one of the spread positions, 
            except for date and quantity"""
        match = None
        if tran:
            for i in range(len(self.posCol)):
                if self.posCol[i].quantity !=0 and self.posCol[i].baseEquals(tran):
                    match = i
                    break
        return match

    def addTransaction(self, t, update=True):
        """update=False, means that it's proposed assignment"""
        new = False  # new position indicator
        self.appendTran(t)
        t.setTrade(self)
        if update:
            Persistence.P.update(t)
        i = self.matchPos(t)
        if i is None:
            self.posCol.append(copy.copy(t))  # add a COPY of tran to the posCol
            new = True
        else:
            self.posCol[i].addQty(t)
        self.net += t.getNet()
        if new:
            self.calculateSpread()

    def addTrans(self, trans, update=True):
        if trans:
            for t in trans:
                self.addTransaction(t, update)

    def rmTrans(self, trans):
        """"""
        recalc = False
        for t in trans:
            l = [it for it in self.tranCol if t.id == it.id]  # find tran to remove
            if l:
                self.tranCol.remove(l[0])  # remove transaction
                t.setTrade(None)
                Persistence.P.cancel(t)
                if not self.tranCol:
                    self.clear()  # if tranCol became empty, clear the trade and exit
                    return
                else:
                    i = self.matchPos(t)
                    self.posCol[i].subtractQty(t)
                    self.net += t.getNet()
                    if self.posCol[i].quantity == 0:
                        # if removing an opening transaction, signal to recalculate the spread
                        del self.posCol[i]
                        recalc = True
        if recalc:
            # positions were removed - reconstruct the spread
            self.calculateSpread()

    def isReal(self):
        return not self.state == "PLAN"

    def setPlan(self):
        self.state = 'PLAN'

    def appendTran(self, t):
        if not self.tranCol or t.dt < self.tranCol[0].dt:
            self.tranCol.insert(0, t)
            self.account = t.account
            self.dateOpen = t.dt
            self.symbol = t.symbol
        else:
            self.tranCol.append(t)

    def clear(self):
        self.account = ''
        self.symbol = ''
        self.spread = None
        self.tranCol[:] = []
        self.posCol[:] = []

    def open(self):
        if self.dateOpen:
            self.state = 'OPEN'

    def close(self):
        if self.dateClose:
            self.state = 'CLOSED'

    def isOpen(self):
        return self.state == 'OPEN'

    def calculateSpread(self):
        self.spread = Spread.construct(self)


# todo code TradeManagement class
class TradeMgmt(object):
    def __init__(self, tr):
        self.trade = tr
        self.symbol = tr.getSymbol()  # Derived from positions
        self.verdict = ''  # notes on trade outcome
        self.outcome = ''  # Formal outcome for analysis
        self.underPriceOpen = 0.0  # Open underlying price
        self.underPriceClose = 0.0  # Close underlying price
        self.dateOpen = tr.getDateOpen()  # Cached from Trade
        self.dateClose = tr.getDateCLose()  # Cached from Trade


#            ret = (self.matchPos(tran) is not None) or \
#                    tran.matchDate(self.dateOpen) or \
#                        (self.spread and self.spread.isComplement(tran))

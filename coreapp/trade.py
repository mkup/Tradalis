import copy


class Trade(object):
    def __init__(self):
        self.id = 0
        self.acct = ''  # account nick (for now)
        self.tranCol = []  # Collection of transactions, uncompressed
        self.posCol = []  # Compressed collection of transaction COPIES
        self.description = ''
        self.symbol = ''  # Derived from the first added transaction
        self.long_short = ''  # ('LONG', 'SHORT') - derived from Spread
        self.open_close = 'PLAN'  # ('OPEN', 'CLOSED', 'PLAN')
        self.dateOpen = None  # Derived from Spread
        self.dateClose = None  # Derived from Spread
        self.risk = 0.0  # Trade initial exposure, derived from Spread
        self.net = 0.0  # Derived from Spread
        self.spread = None
        self.mgmt = None

    #   Structural methods
    def getRisk(self):
        return self.spread.getRisk()

    def getStrategy(self):
        return self.mgmt.getStrategy()

    def getVerdict(self):
        return self.mgmt.getVerdict()

    def getOutcome(self):
        return self.mgmt.getOutcome()

    #   Application methods
    def belong(self, tran):
        if (not tran) or not self.acct == tran.account or not self.matchSymbol(tran):
            ret = False
        else:
            ret = self.matchPos(tran) or self.isComplement(tran)
        return ret

    def matchPos(self, tran):
        """ Determine if a similar transaction exists in the spread.
            Basically, the transaction must be of exact match to one of the spread positions, 
            except for date and quantity"""
        match = None
        if tran:
            for i in range(len(self.posCol)):
                if self.posCol[i].baseEquals(tran):
                    match = i
                    break
        return match

    def isComplement(self, t):
        """See if the transaction belongs to the spread or the covered call pair"""
        # todo: it should be spread's responsibility to answer this question, but later...
        return t and t.matchDate(self.dateOpen)

    def addTrans(self, trans):
        """"""
        new = False  # new position indicator
        for t in trans:
            self.appendTran(t)
            t.setTrade(self)
            i = self.matchPos(t)
            if i:
                self.posCol[i].addQty(t)
            else:
                self.posCol.append(copy.copy(t))  # add a COPY of tran to the posCol
                new = True
            self.net += t.getNet()
        if new:
            # todo: invoke Spread logic for NEW positions
            pass
        else:
            # todo: invoke Spread logic for EXISTING position
            pass
            # mark for update

    def rmTrans(self, trans):
        """"""
        recalc = False
        for t in trans:
            l = [it for it in self.tranCol if t.id == it.id]  # find tran to remove
            if l:
                self.tranCol.remove(l[0])  # remove transaction
                t.setTrade(None)
                if not self.tranCol:
                    self.clear()  # if tranCol became empty, clear the trade and exit
                    return
                else:
                    i = self.matchPos(t)
                    self.posCol[i].subtractQty(t)
                    self.net -= t.getNet()
                    if self.posCol[i].quantity == 0:
                        # if removing an opening transaction, signal to recalculate the spread
                        del self.posCol[i]
                        recalc = True
        if recalc:
            # todo: recalculate the spread
            pass

    def matchSymbol(self, tran):
        if (self.symbol == '') or (self.symbol == tran.symbol):
            return True
        else:
            return False

    def isReal(self):
        return not self.open_close == "PLAN"

    def appendTran(self, t):
        if not self.tranCol or t.dt < self.tranCol[0].dt:
            self.tranCol.insert(0, t)
            self.acct = t.acct
            self.dateOpen = t.dt
            self.symbol = t.symbol
        else:
            self.tranCol.append(t)

    def clear(self):
        self.acct = ''
        self.symbol = ''
        self.spread = None
        self.tranCol[:] = []
        self.posCol[:] = []
        # todo: mark for Delete

# todo code Spread class
class Spread(object):
    """"""
    def __init__(self):
        pass

# todo code TradeManagement class
class TradeMgmt(object):
    def __init__(self, tr):
        self.trade = tr
        self.symbol = tr.getSymbol()  # Derived from positions
        self.strategy = ''
        self.verdict = ''  # notes on trade outcome
        self.outcome = ''  # Formal outcome for analysis
        self.underPriceOpen = 0.0  # Open underlying price
        self.underPriceClose = 0.0  # Close underlying price
        self.dateOpen = tr.getDateOpen()  # Cached from Trade
        self.dateClose = tr.getDateCLose()  # Cached from Trade

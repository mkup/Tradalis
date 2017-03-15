import copy

class Trade(object):

    def __init__(self):
        self.id = 0
        self.acct = ''          # account nick (for now)
        self.tranCol = []       # Collection of transactions, uncompressed
        self.posCol = []               # Compressed collection of transaction COPIES
        self.description = ''
        self.symbol = ''               # Derived from positions
        self.long_short = ''           # ('LONG', 'SHORT') - derived from positions
        self.open_closed = 'PLAN'      # ('OPEN', 'CLOSED', 'PLAN')
        self.dateOpen = None           # Derived from positions
        self.dateClose = None          # Derived from positions
        self.risk = 0.0                # trade initial exposure, derived from positions
        self.net = 0.0                 # Derived from positions
        self.spread = None
        self.mngmt = None

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
    def matchTran(self, tran):
        if (tran is None) or (not self.account == tran.account) or \
            (not self.matchSymbol(tran)) or (self.matchPos(tran) is None):
            return None
        else:
            return self

    def matchPos(self, tran):
        """ Determine if a transaction belongs to the spread.
            Basicaly, the transaction must be of exact match to one of the spread positions, except for date and quantity"""
        match = None
        if not tran is None:
            str = tran.baseString()
            for i in range(self.posCol.len()) :
                if str == self.posCol[i].baseString():
                    match = i
                    break
        return match

    def addTrans(self, trans):
        """"""
        new = False                 # new position indicator
        for t in trans:
            self.tranCol.append(t)
            t.setTrade(self)
            i = self.matchPos(t)
            if i :
                self.posCol[i].addQty(t)
            else:
                if not self.posCol:                     # set trade symbol with the first Transaction
                    self.symbol = t.symbol
                self.posCol.append(copy.copy(t))        # add a COPY of tran to the posCol
                new = True
            self.net += t.getNet()
        if new:
            # todo: invoke Spread logic for NEW positions
            pass
        else:
            # todo: invoke Spread logic for EXISTING position
            pass
        # mark for update

    def remTrans(self, trans):
        """"""
        all = False
        for t in trans:
            l = [it for it in self.tranCol if t.id == it.id]        # find tran to remove
            if l:
                self.tranCol.remove(l[0])                           # remove transaction
                t.setTrade(0)
            else:
                continue                                            # skip

            if not self.tranCol:
                self.clear()                # if tranCol became empty, clear the trade and exit
                return
            else:
                i = self.matchPos(t)
                self.posCol[i].subtractQty(t)
                self.net += t.getNet()
                if self.posCol[i].addQty(t) == 0:                  #  if removing an opening transaction, signal to recalc the spread
                    del self.posCol[i]
                    all = True
        if all:
            # todo: recalculate the spread
            pass

    def matchSymbol(self,tran):
        if (self.symbol == '') or (self.symbol == tran.symbol):
            return True
        else:
            return False


# todo code Spread class
class Spread():
    """"""

    def __init__(self):
        """"""

class TradeMgmt():

    def __init__(self, trade):
        #self.trade = trade         # I hope this var would not be neccessary
        self.symbol = trade.getSymbol()        # Derived from positions
        self.strategy = ''
        self.verdict = ''                           # notes on trade outcome
        self.outcome = ''                           # Formal outcome for analysis
        self.underPriceOpen = 0.0                   # Open underlying price
        self.underPriceClose = 0.0                  # Close underlying price
        self.dateOpen = trade.getDateOpen()          # Cached from Trade
        self.dateClose = trade.getDateCLose()        # Cached from Trade

from decimal import Decimal
from env.Persistence import Persistence

class Position(object):

    def __init__(self):
        self.id = None
        self.dt = None
        self.vendorId = ''
        self.quantity = 0              # Sign defines the action: Sold '-', Bought '+'
        self.origQty = 0              # Same as quantity
        self.symbol = ''
        self.price = Decimal(0.00)
        self.comm = Decimal(0.00)
        self.net = Decimal(0.00)
        self.instrument = ''            # ('stock', 'call', 'put')
        self.trade = 0
        self.account = ''
        self.baseString = None

    def __repr__(self):
        return type(self).__name__ + ' '+ str(self.quantity) + '@' + \
               self.dt.strftime('%m/%d/%Y') + ': ' + self.getBaseString()

    def getBaseString(self):
        if not self.baseString:
            self.baseString = self.symbol
        return self.baseString

    def baseEquals(self, pos):
        """ Compares self to an other position, except for date and quantity"""
        return self.getBaseString() == pos.getBaseString()

    def addQty(self, pos):
        self.quantity += pos.quantity
        if self.origQty * pos.quantity > 0:         # multiple fills - aggergation
            self.origQty += pos.quantity

    def subtractQty(self, pos):
        self.quantity -= pos.quantity

    def getNet(self):
        return self.net

    def setTrade(self,tr):
        if self.trade != tr:
            self.trade = tr
            Persistence.P.update(self)

    def matchDate(self,date):
        return self.dt == date

    def getFullString(self):
        return ':'.join([self.symbol, self.dt.strftime('%Y/%m/%d'), self.instrument])

    def isStock(self):
        return self.instrument == 'stock'

    def isCall(self):
        return self.instrument == 'call'

    def isPut(self):
        return self.instrument == 'put'

    def isLong(self):
        return self.quantity >= 0

    def getOrigNet(self):
        return self.getNet()

class Option(Position):
    """ """
    def __init__(self):
        super().__init__()
        self.removal = False        #True/False
        self.expiration = None
        self.strike = 0.0

    def getBaseString(self):
        if not self.baseString:
            self.baseString = ':'.join([self.symbol, self.instrument, self.expiration.strftime('%Y/%m/%d'), str(self.strike)])
        return self.baseString

    def getFullString(self):
        return ':'.join([self.symbol, self.dt.strftime('%Y/%m/%d'), self.expiration.strftime('%Y/%m/%d'), self.instrument, str(self.strike)])

    def getOrigNet(self):
        return self.origQty * self.price * (-100)

    def isRemoval(self):
        return self.removal

    def addQty(self, pos):
        if pos.isRemoval():
            self.quantity = 0
        else:
            super().addQty(pos)
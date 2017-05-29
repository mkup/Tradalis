from decimal import Decimal
from env.Persistence import Persistence

class Position(object):

    def __init__(self):
        self.id = None
        self.dt = None
        self.vendorId = ''
        self.quantity = 0              # Sign either here or in price
        self.origQty = 0              # Sign either here or in price
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

class Option(Position):
    """ """
    def __init__(self):
        super().__init__()
        self.removal = False        #True/False
        self.expiration = None
        self.strike = 0.0

    def getBaseString(self):
        if not self.baseString:
            self.baseString = self.symbol + self.instrument + self.expiration.strftime('%m/%d/%Y') + str(self.strike)
        return self.baseString

class Position():

    def __init__(self):
        self.id = None
        self.dt = None
        self.vendorId = ''
        self.quantity = 0              # Sign either here or in price
        self.origQty = 0              # Sign either here or in price
        self.symbol = ''
        self.price = 0.0
        self.comm = 0.0
        self.net = 0.0
        self.instrument = ''            # ('stock', 'call', 'put')
        self.trade = 0
        self.account = ''

    def baseString(self):
        """ Return identity string, except for date and quantity"""
        return self.symbol  # construct self identity

    def addQty(self, pos):
        self.quantity += pos.quantity

    def subtractQty(self, pos):
        self.quantity -= pos.quantity

    def getNet(self):
        return self.net

    def setTrade(self,tr):
        self.trade = tr
        # mark for update

class Option(Position):
    """ """
    def __init__(self):
        super(self).__init__()
        self.removal = False        #True/False
        self.expiration = None
        self.strike = 0.0

    def baseString(self):
        """ Return identity string, except for date and quantity"""
        str = self.super().baseString()
        if self.removal:
            str += " removal"
        else:
            str += " " + self.instrument + " $" + self.strike + " @" + self.expiration
        return str

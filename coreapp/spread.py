# todo code Triple subclass
# todo code Quad subclass
# todo: display Spread qty
import datetime
import copy


class Spread(object):
    """This is an abstract class"""

    @staticmethod
    def construct(trade):
        """"""
        trade.posCol.sort(key=lambda x: x.getFullString())
        l = len(trade.posCol)
        if l == 1 or [t for t in trade.posCol if t.isStock()]:
            spr = Single(trade)
        elif l == 2:
            spr = Twos.determine(trade)
        elif l == 3:
            spr = Triple(trade)
        elif l == 4:
            spr = Quad.determine(trade)
        else:
            spr = Other(trade)
        spr.calculate()
        return spr

    def __init__(self, tr):
        self.trade = tr
        if tr.posCol:
            self.col = tr.posCol
        else:
            self.col = None
        self.tp = ''

    def __repr__(self):
        return self._display()

    def getOpen(self):
        return self.col[0].dt

    def isClosed(self):
        return bool(not [t for t in self.trade.posCol if t.quantity != 0])

    def getClose(self):
        if self.isClosed():
            return self.trade.tranCol[-1].dt
        else:
            return None

    def getNet(self):
        return sum([t.net for t in self.trade.tranCol])

    def getOpenNet(self):
        return sum([t.getOrigNet() for t in self.col])

    def getRisk(self):
        return None

    def getInstrument(self):
        return 'Both'

    def longShort(self):
        if self.isLong():
            return 'Long'
        else:
            return 'Short'

    def calculate(self):
        self.trade.net = self.getNet()
        self.trade.long_short = self.longShort()
        self.trade.dateOpen = self.getOpen()
        if self.isClosed():
            self.trade.dateClose = self.getClose()
            self.trade.close()
        else:
            self.trade.dateClose = None
        self.trade.risk = self.getRisk()

    def isLong(self):
        pass

    def getType(self):
        pass

    def _display(self):
        """Calendar 10 AAPL June 16(17)/July 18(17) @150"""
        expStr = ''
        prevExp = datetime.date(year=1970, month=1, day=1)
        strikeStr = '@'
        prevStrike = 0
        qtyStr = ''
        prevQty = 0
        sep = ''
        for p in self.col:
            if p.expiration != prevExp:
                expStr += sep + p.expiration.strftime('%m-%d-%y')
                prevExp = p.expiration
            if p.strike != prevStrike:
                strikeStr += sep + str(p.strike)
                prevStrike = p.strike
            if abs(p.origQty) != prevQty:
                qtyStr += sep + str(abs(p.origQty))
                prevQty = abs(p.origQty)
            sep = '/'
        return ' '.join(
            [self.getType(), qtyStr, self.trade.symbol, self.getInstrument(), expStr, strikeStr, self.longShort()])


# noinspection PyMethodMayBeStatic
class Single(Spread):
    """Stock (possibly with covered calls) or Single Option"""

    def getType(self):
        return 'Single'

    def _display(self):
        return ' '.join([self.col[0].symbol, str(self.col[0].origQty), self.longShort()])

    def getInstrument(self):
        s = self.col[0].instrument
        if len(self.col) > 1 and [p for p in self.col if p.isCall()]:  # that makes it Stock plus covered call
            s += " + Covered Call"
        return s

    def getRisk(self):
        if self.col[0].isLong():
            r = 0 - self.getOpenNet()
        elif not self.col[0].isPut():  # short Stock or Call
            r = None  # it actually means infinite
        else:  # short Put
            r = self.col[0].origQty * self.col[0].strike * (-100) + self.getOpenNet()
        return r

    def isLong(self):
        return self.col[0].isLong()


class Twos(Spread):
    """ Twos covers vertical, ratio, calendar, straddle and strangle spreads"""

    @classmethod
    def determine(cls, tr):
        one = tr.posCol[0]
        two = tr.posCol[1]
        q = one.origQty + two.origQty
        if q != 0:
            spr = VertRatio(tr)
            if q > 0:
                spr.tp = 'Back Ratio'
            else:
                spr.tp = 'Ratio'
        elif one.expiration != two.expiration:
            spr = Calen(tr)
            spr.tp = 'Calendar'
        elif one.instrument == two.instrument:  # same instrument
            spr = VertRatio(tr)
            spr.tp = 'Vertical'
        else:
            spr = Strle(tr)
            if two.strike - one.strike > .50:
                spr.tp = 'Strangle'
            else:
                spr.tp = 'Straddle'
        return spr

    def __init__(self, tr):
        super().__init__(tr)
        # convenience vars
        self.one = self.col[0]
        self.two = self.col[1]

    def getType(self):
        return self.tp

    def getRisk(self):
        """ Strle should override """
        if self.isLong():
            r = 0 - self.getOpenNet()
        else:
            r = abs(self.one.strike - self.two.strike)
            if self.two.isLong():  # use short leg quantity
                r *= self.one.origQty
            else:
                r *= self.two.origQty
            r += self.getOpenNet()
        return r

    def getInstrument(self):
        """Strle should override"""
        return self.one.instrument


class Calen(Twos):
    def isLong(self):
        return self.two.isLong()


class VertRatio(Twos):
    def isLong(self):
        return (self.one.instrument == 'call' and self.one.isLong()) or \
               (self.one.instrument == 'put' and self.two.isLong())


class Strle(Twos):
    """Straddle and Strangle"""

    def getInstrument(self):
        return 'Both'

    def isLong(self):
        return self.one.islong()

    def getRisk(self):
        if self.isLong():
            return 0 - self.getOpenNet()
        else:
            return None


class Triple(Spread):
    """Butterfly"""

    def __init__(self, tr):
        super().__init__(tr)
        self.tp = ''
        # convenience vars
        self.one = self.col[0]
        self.two = self.col[1]
        self.three = self.col[2]

    def getType(self):
        if not self.tp:
            if self.getInstrument() == 'Both' or \
                    not (self.one.expiration == self.two.expiration and self.one.expiration == self.three.expiration) or \
                    not (self.one.isLong() == self.three.isLong() and self.one.isLong() != self.two.isLong()):
                self.tp = 'Other'
            elif self.one.origQty == self.three.origQty:
                self.tp = 'Butterfly'
            else:
                self.tp = 'Broken Wing Butterfly'
        return self.tp

    def getInstrument(self):
        if self.one.instrument == self.two.instrument and self.one.instrument == self.three.instrument:
            return self.one.instrument
        else:
            return 'Both'

    def isLong(self):
        return self.two.isLong()

    def getRisk(self):
        if self.getType() != 'Other' and self.isLong():
            if self.getInstrument() == 'Call':
                mid = self.two
                last = self.three
            else:
                mid = self.two
                last = self.one
            return (last.strike - mid.strike) * (mid.origQty + last.orig.Qty) * 100
        else:
            return None


class Quad(Spread):
    """"""

    # noinspection PyUnusedLocal
    @classmethod
    def determine(cls, tr):
        tr1 = copy.copy(tr)
        tr1.posCol = tr.posCol[:2]
        spr1 = Twos.determine(tr1)
        tr2 = copy.copy(tr)
        tr2.posCol = tr.posCol[:-2]
        spr2 = Twos.determine(tr1)
        return Quad(tr, spr1, spr2)

    def __init__(self, trade, spr1, spr2):
        super().__init__(trade)
        self.spr1 = spr1
        self.spr2 = spr2
        self.getType()

    def getType(self):
        if not self.tp:
            if (
                                self.spr1.getType() == 'Vertical' and not self.spr1.isLong() and self.spr1.getInstrument() == 'call') and \
                    (
                                        self.spr2.getType() == 'Vertical' and not self.spr2.isLong() and self.spr2.getInstrument() == 'put'):
                self.tp = 'Iron Condor'
            elif (self.spr1.getType() == 'Strangle' and not self.spr1.isLong()) and \
                    (self.spr2.getType() == 'Strangle' and self.spr2.isLong()) and \
                            self.spr1.one.expiration < self.spr2.one.expiration:
                self.tp = 'Strangle Swap'
            else:
                self.tp = 'Other'
        return self.tp

    def isLong(self):
        return self.spr1.isLong()

    def getRisk(self):
        if self.getType() == 'Iron Condor':
            return max(self.spr1.getRisk(), self.spr2.getRisk())
        else:
            return None

    def getInstrument(self):
        return 'Both'


class Other(Spread):
    """"""
    def getType(self):
        return 'Other'

    def isLong(self):
        return False


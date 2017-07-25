import datetime
from env.Persistence import Persistence


class Proposal(object):
    Props = []

    @classmethod
    def addProp(cls,trade, trans):
        state = trade.isReal()
        trade.calculateSpread()
        if not state:
            trade.setPlan()
        cls.Props.append(Proposal(trade, trans))

    def __init__(self, tr, trans):
        self.trade = tr
        self.trans = trans
        self.dt = datetime.datetime.now()

    def accept(self):
        if self.trade.isReal():
            self.trade.addTrans(self.trans, True)
        else:
            self.trade.open()
        self.trade.calculateSpread()
        Persistence.P.update(self.trade)
        [Persistence.P.update(t) for t in self.trans]

    def reject(self):
        if not self.trade.isReal():
            self.trade.clear()

    def __repr__(self):
        s = repr(self.trade) + '\n'
        if self.trade.isReal():
            for t in self.trans:
                s += repr(t) + '\n'
        s += "--- Add ---" + '\n'
        for t in self.trans:
            s += repr(t) + '\n'
        return s


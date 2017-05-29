import datetime


class Proposal(object):
    def __init__(self, tr, trans):
        self.trade = tr
        self.trans = trans
        self.dt = datetime.datetime.now()

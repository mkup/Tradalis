import datetime


class Proposal(object):
    def __init__(self, trans):
        self.trade = None
        self.trans = trans
        self.dt = datetime.datetime.now()

from env.Persistence import Persistence

class TestData(object):

    @staticmethod
    def startup():
        trades = Persistence.P.retriever.getTransactions(1)
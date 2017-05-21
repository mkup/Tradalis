from env.Persistence import Persistence

class TestData(object):

    def startup(self):
        posCol = Persistence.P.retriever.getTransactions(1)
        print(posCol)
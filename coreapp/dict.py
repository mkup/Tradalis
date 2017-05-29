from env.Persistence import Persistence


class Dict(object):
    all = None

    @staticmethod
    def getAll():
        if not Dict.all:
            Dict.all = Persistence.P.retriever.populateDic()
        return Dict.all

    def __init__(self, nm):
        self.id = 0
        if not nm in list(Dict.getAll().keys()):
            exit(2)
        self.name = nm
        self.cde = ''
        self.description = ''
        self.valid = 1
        Dict.getAll()[nm].append(self)


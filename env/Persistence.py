# todo: Implement CommitTransaction, CancelTransaction logic
import importlib

class Persistence(object):
    """ Parent for specific storage handlers """
    # Singleton
    P = None
    
    @staticmethod
    def startup(conf):
        mlName = conf.get("Persistence", "module")
        clName = conf.get("Persistence", "class")
        module = importlib.import_module(mlName)
        cls = getattr(module, clName)
        Persistence.P = cls(conf)
        return Persistence.P
            
    @staticmethod
    def shutdown():
        Persistence.P.close()
        Persistence.P = None

    def __init__(self):
        self.retriever = None                         # Data Retriever - needs to be implemented by subclasses
        self.mapper = None                            # Data Mapper  - needs to be implemented by subclasses
        self.completeInit()                           # subclass functionality

    def commit(self):
        pass



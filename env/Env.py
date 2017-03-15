from Persistence import Persistence

class Env(object):
    E = None
    
    def __init__(self, conf):
        self.config = conf
        self.cache = None
        self.persistence = None
        self.app = None
        self.log = None
        self.start()
        
    def start(self):
        if Env.E :
            raise Exception("Environment already exists")
        else:
            Env.E = self
        self.cache = []
        self.persistence = Persistence.startup(self.config)
        #todo self.log = new log and init
        self.appStart()

    def stop(self):
        self.persistence.shutdown()
        # close log
        # stop coreapp?
        Env.E = None

    def getP(self):
        return self.persistence

    def getLog(self):
        return self.log

    def appStart(self):
        if self.config.has_option("Application", "class") :
            nm = self.config.get("Application", "class")
            obj = globals()[nm]
            self.app = obj.start


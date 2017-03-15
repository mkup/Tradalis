# asdfasdf
from PMysql.dbTable import DB_table

class DB_instrument(DB_table):
    inst = None
    
    @staticmethod
    def single():
        if not DB_instrument.inst:
            DB_instrument.inst = DB_instrument()
        return DB_instrument.inst
        
    def defineNames(self):
        self.tname = "Instrument"
        self.names = ["id", "cde", "description"]
        self.data = [[0,"stock","Stock"], [1,"call", "Call Option"], [2,"put","Put option"]]
        
    def getId(self, code):
        c = code.lower()
        for l in self.data :
            if l[1] == c : 
                return l[0]
        
    
    
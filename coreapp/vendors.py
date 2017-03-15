from PMysql.dbTransaction import DB_transaction
import calendar
from datetime import date, datetime

class Vendor(object):

    col = {}

    @staticmethod
    def loadVendors():
        v = TDA()
        Vendor.col[v.nick] = v

    @staticmethod
    def getVendor(nm):
        return Vendor.col[nm]

    def __init__(self):
        self.nick = ''
        self.contact = " "
        self.populate()

    def populate(self):
        pass

    def fromFile(self, act, fn):
        #        import sys, os
        #        sys.path.append("/Users/mark2/Documents/MyDev/git/Tradalis")
        #        os.chdir("/Users/mark2/Documents/MyDev/git/Tradalis")
        #        print os.getcwd()

        # act is account Nickname
        s = open( fn )
        self.load(act, s)
        s.close( )

class TDA(Vendor):
    """" This class handles loading Transaction data from a file system
        It's aware of the input file structure and the destination DB object.
        I'm taking a lot of shortcuts here for now - (1)TDA only, (2) straight to mysql """

    exp = {v.lower(): k for k, v in enumerate( calendar.month_abbr )}
    oper = ('sold', 'bought', 'removal')

    def populate(self):
        self.nick = "TDA"
        self.contact = " "  # to be filled out later

    def load(self, act, stream):
        "Loads transactions from the source opened as a 'Stream' - either file or URL request"

        inst = DB_transaction([])
        for line in stream:  # loop until the EOF
            data = line.split( ',' )  # parse CSV
            if self.needsLoad(data):  # check if the line is 'loadable'
                self.fixLine(data)
                data.append(act)
                data.insert(0,0)        # id placeholder, it will be skipped by DB_table.insert()
                inst.setData(data)
                inst.insert( )
        inst.db.commit( )

    def needsLoad(self, data):
        r = False
        if not data[0].startswith("***END"):            # the last line of the transactions download
            s = data[2].split( ' ', 1 )
            r = (s[0].lower( ) in TDA.oper)
        return r

    def fixLine(self, data):
        # todo: code the 'removal' transaction
        d = data[0].split('/')
        data[0] = datetime(int( d[2] ), int(d[0]), int(d[1])).strftime("%Y-%m-%d %H:%M:%S")  # Transaction date
        s = data[4].split(' ')
        if len(s) > 1:
            data[4] = s[0]  # Symbol
            if data[2].startswith("Bought"):
                data[5] = '-' + data[5]
            data[8] = s[5].lower()  # Instrument
            data[9] = date(int( s[3] ), TDA.exp[s[1].lower()], int(s[2])).strftime("%Y-%m-%d")  # Expiration
            data[10] = s[4]  # Strike
        else:
            data[8] = 'stock'       # Instrument
            data[9] = ''
            data[10] = 0.0
            data[11] = 0  # Trade id
        del data[12]



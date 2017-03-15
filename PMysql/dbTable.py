#todo duplicate Transactions
from env.Persistence import Persistence

class DB_table(object):
    """ 'Abstract' class, that implements the most of SQL methods """

    def __init__(self):
        self.db = Persistence.P
        self.tname = 'Needs Name'
        self.names = []
        self.data = []
        self.defineNames()

    def defineNames(self):
        pass

    def getNames(self):
        return self.names

    def getData(self):
        return self.data

    def setNames(self, lst):
        self.names = lst

    def get(self,name):
        i = self.names.index(name)
        return self.data[i]

    def setData(self, lst):
        self.data = lst

    def getOneRow(self, sql):
        data = self.select(sql, True)
        self.setData(data)

    @staticmethod
    def select(sql, all=True):
        #todo sql error handling
        cursor = Persistence.P.connection.cursor()
        cursor.execute(sql)
        col = cursor.fetchall()
        cursor.close()
        return col


    def insert(self):
        comma = ', '
        nm = self.getNames()
        dt = self.getData()
        if "id" in self.names:  # skip `id` - auto-increment field
            nm = nm[1:]
            dt = dt[1:]
        sql = "Insert into " + self.tname + " (" + \
              comma.join(nm) + ") VALUES(" + \
              str(dt).strip('[]') + ")"
        cursor = self.db.connection.cursor()
        cursor.execute(sql)
        i = cursor.lastrowid
        cursor.close()
        return i

    def update(self, sql):
        pass






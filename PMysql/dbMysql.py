from mysql import connector
from env.Persistence import Persistence
from mysql.connector import errorcode
from PMysql.dataretriever import Getter
from PMysql.mapping import Map

class DB_Mysql(Persistence):
    """ This class performs all the Mysql operations """

    def __init__(self, conf):
        super(DB_Mysql, self).__init__()
        self.conf = conf
        self.connection = self.connect()
        self.changes = {'trade':{'i':[],'d':[],'u':[]}, 'tran':[]}    # only Update for Transactions, for now

    def completeInit(self):
        self.retriever = Getter()
        self.mapper = Map()

    def connect(self):
        try:
            return connector.connect(db=self.conf.get('mysql','db'), user=self.conf.get('mysql','user'), passwd=self.conf.get('mysql','passwd'))
        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Bad user name and password combination")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(2)

    def close(self):
        self.commit()
        self.connection.close()
        
    def commit(self):
        # insert Trade
        for tr in self.changes['trade']['i']:
            self.retriever.insertTrade(tr)
        self.changes['trade']['i'] = []

        # update Trade
        for tr in self.changes['trade']['u']:
            self.retriever.updateTrade(tr)
        self.changes['trade']['u'] = []

        # delete Trade
        for tr in self.changes['trade']['d']:
            self.retriever.deleteTrade(tr)
        self.changes['trade']['d'] = []

        # update Transaction
        for t in self.changes['tran']:
            self.retriever.updateTranasaction(t)
        self.changes['tran'] = []

        self.connection.commit()

    def update(self, obj):
        if not obj:
            pass
        elif type(obj).__name__ == 'Trade':
            self.changes['trade']['u'].append(obj)
        elif type(obj).__name__ in ('Position', 'Option'):
            self.changes['tran'].append(obj)

    def insert(self, obj):
        if not obj:
            pass
        elif type(obj).__name__ == 'Trade':
            self.changes['trade']['i'].append(obj)

    def delete(self, obj):
        if not obj:
            pass
        elif type(obj).__name__ == 'Trade':
            self.changes['trade']['d'].append(obj)


from mysql import connector
from env.Persistence import Persistence
from mysql.connector import errorcode
from PMysql.datarouter import Getter
from PMysql.mapping import Map

class DB_Mysql(Persistence):
    """ This class performs all the Mysql operations """

    def __init__(self, conf):
        super(DB_Mysql, self).__init__()
        self.conf = conf
        self.connection = self.connect()

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
        self.connection.commit()


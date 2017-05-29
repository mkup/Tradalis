from PMysql.dbTable import DB_table


class DB_dic(DB_table):
    def __init__(self, dataList):  # the parameter could be a tuple
        super().__init__()
        self.setData(list(dataList))

    def defineNames(self):
        ar = ['id', 'cde', 'description', 'active']
        self.setNames(ar)

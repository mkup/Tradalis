# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import unittest

import dbMysql


class  DBTestCase(unittest.TestCase):
    def setUp(self):
        dbMysql.DB_Mysql.connect()
    
    def tearDown(self):
        self.dbCon = dbMysql.DB_Mysql.close()

    def test__connect(self):
        crs = dbMysql.DB_Mysql().connection.cursor()
        self.assertIsNotNone(crs)
        crs.execute("select * from Transactions")
        self.assertEqual(0, crs.rowcount)
        crs.close()

def main():
    unittest.main()
    
if __name__ == '__main__':
    unittest.main()
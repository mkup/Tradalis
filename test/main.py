from mysql import connector

cnx = connector.connect(db="tradalis", user='root', passwd='123')
# Using the cursor as iterator
crs = cnx.cursor()
crs.execute("SELECT * FROM Transaction")
row = crs.fetchone()
print(type(row[1]), type(row[2]), type(row[6]))
crs.fetchall()
crs.close()
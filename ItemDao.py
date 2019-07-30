import cx_Oracle

class ItemDao:

    def __init__(self):
        ip = 'stonehillcsc325.cjjvanphib99.us-west-2.rds.amazonaws.com'
        port = 1521
        SID = 'ORCL'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        self.db = cx_Oracle.connect('jpenaflorida', 'csrocks55', dsn_tns)
        self.cur = self.db.cursor()

    def add(self, item):
        n = "'" + item.name+ "'"
        d = "'" + item.description + "'"
        q = "'" + item.quantity + "'"
        u = "'" + item.unit + "'"
        num = str(item.item_number)
        s = "'" + item.storage_area + "'"
        self.cur.execute("insert into items values("
                         + n + ','
                         + d + ','
                         + q + ','
                         + u + ','
                         + num + ','
                         + s + ')')
        self.db.commit()

    def edit(self, name, desc, quantity, unit, item_number, storage_area):
        name = "'" + name + "'"
        desc = "'" + desc + "'"
        unit = "'" + unit + "'"
        storage_area = "'" + storage_area + "'"

        self.cur.execute("update items set name = " + name +
                         ", description = " + desc
                         + ", quantity = " + str(quantity)
                         + ", unit = " + unit
                         + ", storage_area = " + storage_area
                         + " where item_number = " + str(item_number))
        self.db.commit()

    def delete(self, number):
        self.cur.execute("delete from items where item_number =" + str(number))
        self.db.commit()

    def get_all(self):
        self.cur.execute("select * from items")
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def get_infodesk(self):
        self.cur.execute("select * from items where storage_area = 'Info Desk'")
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def get_gac(self):
        self.cur.execute("select * from items where storage_area = 'Group Activities Center'")
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def print(self):
        self.cur.execute("select * from items")
        result = self.cur.fetchall()
        for row in result:
            print(row[0] + " | " + row[1] + " | " + str(row[2]) + " | " + row[3] + " | " + str(row[4]) + " | " + str(row[5]))




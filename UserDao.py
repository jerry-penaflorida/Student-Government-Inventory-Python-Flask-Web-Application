import cx_Oracle
from User import User

class UserDao:

    def __init__(self):
        ip = 'stonehillcsc325.cjjvanphib99.us-west-2.rds.amazonaws.com'
        port = 1521
        SID = 'ORCL'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        self.db = cx_Oracle.connect('jpenaflorida', 'csrocks55', dsn_tns)
        self.cur = self.db.cursor()

    def add(self, user):
        e = "'" + user.email + "'"
        p = "'" + user.password + "'"
        f = "'" + user.fname + "'"
        l = "'" + user.lname + "'"
        self.cur.execute("insert into inventory_users values("
                         + e + ','
                         + p + ','
                         + f + ','
                         + l + ')')
        self.db.commit()

    def delete(self, email):
        email = "'" + email + "'"
        self.cur.execute("delete from inventory_users where email =" + email)
        self.db.commit()

    def print(self):
        self.cur.execute("select * from inventory_users")
        result = self.cur.fetchall()
        for row in result:
            print(row[0] + " | " + row[1] + " | " + row[2] + " | " + row[3])

    def check(self, email, password):
        e = "'" + email + "'"
        p = "'" + password + "'"

        self.cur.execute("select * from inventory_users where email = " + e + " and password = " + p)

        result = self.cur.fetchall()

        if len(result) == 0:
            return False
        else:
            return True



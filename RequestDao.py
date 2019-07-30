import cx_Oracle

class RequestDao:

    def __init__(self):
        ip = 'stonehillcsc325.cjjvanphib99.us-west-2.rds.amazonaws.com'
        port = 1521
        SID = 'ORCL'
        dsn_tns = cx_Oracle.makedsn(ip, port, SID)
        self.db = cx_Oracle.connect('jpenaflorida', 'csrocks55', dsn_tns)
        self.cur = self.db.cursor()

    def add(self, request):
        n = "'" + request.name + "'"
        d = "'" + request.description + "'"
        q = "'" + request.quantity + "'"
        u = "'" + request.unit + "'"
        e = "'" + request.email + "'"
        s = "'" + request.status + "'"
        r = str(request.request_number)
        self.cur.execute("insert into requests values("
                         + n + ','
                         + d + ','
                         + q + ','
                         + u + ','
                         + e + ','
                         + s + ','
                         + r + ')')
        self.db.commit()

    def delete(self, number):
        self.cur.execute("delete from requests where request_number =" + str(number))
        self.db.commit()

    def get_all(self):
        self.cur.execute("select * from requests")
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def get_specific(self, email):
        email = "'" + email + "'"
        self.cur.execute("select * from requests where email = " + email)
        result = self.cur.fetchall()
        self.db.commit()
        return result

    def print(self):
        self.cur.execute("select * from items")
        result = self.cur.fetchall()
        for row in result:
            print(row[0] + " | " + row[1] + " | " + str(row[2]) + " | " + row[3] + " | " + str(row[4]))




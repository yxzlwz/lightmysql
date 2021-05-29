import pymysql


def try_int(s):
    if type(s).__name__ == "int":
        return s
    else:
        if ((s.startswith("'") and s.endswith("'"))
                or (s.startswith("\"") and s.endswith("\""))):
            return s
        else:
            return "'%s'" % s


def format_into_mysql(s: dict, name=""):
    if not s:
        return ""
    result = ""
    for i, j in s.items():
        result += "%s=%s," % (i, try_int(j))
    return name + " " + result[:-1]


class Connect:
    def __init__(self,
                 host,
                 user,
                 password,
                 database,
                 port=3306,
                 charset="utf8"):
        self.connect = pymysql.connect(host=host,
                                       user=user,
                                       password=password,
                                       database=database,
                                       port=port,
                                       charset=charset)
        print("连接到 %s / %s 成功！当前用户为：%s" % (host, database, user))
        self.cursor = self.connect.cursor()

    def run_code(self, code, return_result=True):
        self.cursor.execute(code)
        self.connect.commit()
        if not return_result:
            return
        results = []
        result = self.cursor.fetchone()
        while result:
            results.append(result)
            result = self.cursor.fetchone()
        return results

    def get_all(self, table):
        self.cursor.execute("select * from %s;" % table)
        results = []
        result = self.cursor.fetchone()
        while result:
            results.append(result)
            result = self.cursor.fetchone()
        return results

    def get(self, table, target: list or str = [], condition: dict = {}):
        if str(target) == target:
            target = [target]
        self.cursor.execute("select %s from %s %s;" %
                            ((target and ", ".join(target)) or "*", table,
                             format_into_mysql(condition, "where")))
        results = []
        result = self.cursor.fetchone()
        while result:
            results.append(result)
            result = self.cursor.fetchone()
        return results

    def update(self, table, changes: dict = {}, condition: dict = {}):
        changes = format_into_mysql(changes)
        condition = format_into_mysql(condition, "where")
        self.run_code("update %s set %s %s;" % (table, changes, condition))

    def insert(self, table: str, data: dict):
        keys = str(tuple(data.keys())).replace("\"", "").replace("'", "")
        values = str(tuple(data.values()))
        self.run_code("insert into %s %s values %s;" % (table, keys, values))

    def delete(self, table, condition: dict):
        condition = format_into_mysql(condition, "where")
        self.run_code("delete from %s %s;" % (table, condition))


if __name__ == "__main__":
    conn = Connect(host="yxzlownserveraddress.yxzl.top",
                   user="root",
                   password="@yixiangzhilv",
                   database="yxzl")


    from icecream import ic

    ic(conn.get("test", condition={"name": "Python-Auto-Test"}))

    conn.insert("test", {"name": "Python-Auto-Test", "age": 15})
    ic(conn.get("test", condition={"name": "Python-Auto-Test"}))

    conn.update("test",
                changes={"age": "20"},
                condition={"name": "Python-Auto-Test"})
    ic(conn.get("test", condition={"name": "Python-Auto-Test"}))

    conn.delete("test", {"name": "Python-Auto-Test"})
    ic(conn.get("test", condition={"name": "Python-Auto-Test"}))

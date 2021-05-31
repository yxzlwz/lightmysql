import pymysql


VERSION = "1.0.2"


def try_type(s):
    # 若传入value（j）的类型为str，则在字符串内容两侧加入表示内容的引号
    if type(s).__name__ != "str":
        return s
    else:
        if ((s.startswith("'") and s.endswith("'"))
                or (s.startswith("\"") and s.endswith("\""))):
            return s
        else:
            return "'%s'" % s


def format_condition_into_mysql(s: dict, sp="and", prefix="where"):
    """
    格式化MySQL子句
    name: MySQL子句的前缀（也就是转换后的任意前缀）
    sp: MySQL条件之间的分隔符，可取"and"或"or"
    """
    if not s:
        # 传入字典为空，则无需设置查询条件
        return ""
    result = ""
    for i, j in s.items():
        t = try_type(j)
        if type(t).__name__ in ["str", "int", "float"]:
            # 这些类型无需处理即可直接传入
            result += "%s=%s %s" % (i, t, sp)
        elif type(t).__name__ == "list":
            # 若字典当前项value为列表，则数据库的table中当前列（i）可对应当前value（j）列表中的任意一项
            text = "("
            for k in t:
                text += "%s=%s or " % (i, try_type(k))
            result += "%s) %s " % (text[:-len(" or ")], sp)
        else:
            raise TypeError
    return prefix + " " + result[:-(len(sp) + 2)]


class Connect:
    def __init__(self,
                 host,
                 user,
                 password,
                 database,
                 port=3306,
                 charset="utf8"):
        # 连接和游标的初始化
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connect = pymysql.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       database=self.database,
                                       port=self.port,
                                       charset=self.charset)
        print("连接到 %s / %s 成功！当前用户为：%s" % (self.host, self.database, self.user))
        self.cursor = self.connect.cursor()

    def run_code(self, code, return_result=True):
        # 提交MySQL语句，并将返回结果存入list中
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

    def insert(self, table: str, data: dict):
        # 分别将字典的key和value格式化为SQL语句
        keys = str(tuple(data.keys())).replace("\"", "").replace("'", "")
        values = str(tuple(data.values()))
        return self.run_code("INSERT INTO %s %s VALUES %s;" %
                             (table, keys, values))

    def get(self,
            table,
            target: list or str = [],
            condition: dict = {},
            condition_sp="and"):
        # 若只传入table，则语句等价于SELECT * FROM table;
        if type(target).__name__ == "str":
            target = [target]
        condition = format_condition_into_mysql(condition, condition_sp)
        return self.run_code(
            "SELECT %s FROM %s %s;" %
            ((target and ",".join(target)) or "*", table, condition))

    def update(self,
               table,
               changes: dict = {},
               condition: dict = {},
               condition_sp="and"):
        changes = format_condition_into_mysql(changes, sp=",", prefix="")
        condition = format_condition_into_mysql(condition, condition_sp)
        return self.run_code("UPDATE %s SET %s %s;" %
                             (table, changes, condition))

    def delete(self, table, condition: dict, condition_sp=" and "):
        condition = format_condition_into_mysql(condition, condition_sp)
        return self.run_code("DELETE FROM %s %s;" % (table, condition))

    def restart(self):
        # MySQL默认8小时清空一次session，所以请确认你在每八小时进行了一次restart
        self.cursor.close()
        self.connect.close()
        self.connect = pymysql.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       database=self.database,
                                       port=self.port,
                                       charset=self.charset)
        print("连接到 %s / %s 成功！当前用户为：%s" % (self.host, self.database, self.user))
        self.cursor = self.connect.cursor()

    def close(self):
        self.cursor.close()
        self.connect.close()
        del(self)

import pymysql
import pymysqlpool
import time


def try_type(s):
    # 若传入value（j）的类型为str，则在字符串内容两侧加入表示内容的引号
    if type(s) != str:
        return s
    else:
        return "\"%s\"" % pymysql.converters.escape_string(s)


def format_condition_into_mysql(s: dict, sp="and", prefix="WHERE BINARY"):
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
        if type(t) in [str, int, float]:
            # 这些类型无需处理即可直接传入
            result += "`%s`=%s %s " % (i, t, sp)
        elif type(t) == list:
            # 若字典当前项value为列表，则数据库的table中当前列（i）可对应当前value（j）列表中的任意一项
            text = "("
            for k in t:
                text += "`%s`=%s or " % (i, try_type(k))
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
                 charset="utf8",
                 pool_size=10):
        # 连接和游标的初始化
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.pool_size = pool_size
        self.pool = pymysqlpool.ConnectionPool(size=self.pool_size,
                                               name="pool",
                                               host=self.host,
                                               user=self.user,
                                               password=self.password,
                                               database=self.database,
                                               port=self.port,
                                               charset=self.charset)
        print("连接到 %s / %s 成功！当前用户为：%s" %
              (self.host, self.database, self.user))
        self.connected_time = time.time()

    def run_code(self, code, return_result=True, twice=False):
        # 提交MySQL语句，并将返回结果存入list中
        try:
            self.check_time()
            connect = self.pool.get_connection()
            cursor = connect.cursor()
            cursor.execute(code)
            connect.commit()
            if not return_result:
                return None
            results = []
            result = cursor.fetchone()
            while result:
                results.append(result)
                result = cursor.fetchone()
            connect.close()
            return results
        except pymysql.err.ProgrammingError:
            return ["You have an error in your SQL syntax.", "您的SQL语法有错误。"]
        except:
            connect.close()
            if twice:
                return []
            self.restart()
            return self.run_code(code, return_result=return_result, twice=True)

    def insert(self, table: str, data: dict):
        # 分别将字典的key和value格式化为SQL语句
        keys = "(" + ", ".join("`%s`" % t for t in data.keys()) + ")"
        values = "(" + ", ".join([str(try_type(t))
                                  for t in data.values()]) + ")"
        return self.run_code(f"INSERT INTO {table} {keys} VALUES {values};")

    def select(self,
               table,
               target: list or str = [],
               condition: dict = {},
               condition_sp="and",
               limit="",
               order_by="",
               order_sort=""):
        # 若只传入table，则语句等价于SELECT * FROM table;
        if type(target).__name__ == "str":
            target = [target]
        condition = format_condition_into_mysql(condition, condition_sp)
        if limit:
            limit = "LIMIT " + str(limit)
        order = ""
        if order_by and order_sort:
            order = f"ORDER BY `{order_by}` {order_sort}"
        return self.run_code(
            f"SELECT {target and '`' + '`,`'.join(target) + '`' or '*'} FROM {table} {condition} {order} {limit};"
        )

    def update(self,
               table,
               changes: dict = {},
               condition: dict = {},
               condition_sp="and"):
        changes = format_condition_into_mysql(changes, sp=",", prefix="")
        condition = format_condition_into_mysql(condition, condition_sp)
        return self.run_code(f"UPDATE {table} SET {changes} {condition};")

    def delete(self, table, condition: dict, condition_sp="and"):
        condition = format_condition_into_mysql(condition, condition_sp)
        return self.run_code(f"DELETE FROM {table} {condition};")

    def check_time(self):
        if time.time() - self.connected_time > 7200:
            self.restart()
            self.connected_time = time.time()

    def restart(self):
        # MySQL默认8小时清空一次session，所以请确认你在每8小时进行了一次restart
        self.pool = pymysqlpool.ConnectionPool(size=self.pool_size,
                                               name="pool",
                                               host=self.host,
                                               user=self.user,
                                               password=self.password,
                                               database=self.database,
                                               port=self.port,
                                               charset=self.charset)
        print("连接到 %s / %s 成功！当前用户为：%s" %
              (self.host, self.database, self.user))

    def close(self):
        del (self)

    get = select

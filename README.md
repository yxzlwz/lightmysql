# Light-MySQL

The improved-package of pymysql, made by Yixiangzhilv.

## Install

`pip3 install lightmysql`

## Example

```Python
>>> import lightmysql
>>> conn = lightmysql.Connect(host="127.0.0.1", user="root", password="", database="yxzl")
连接到 127.0.0.1 / yxzl 成功！当前用户为：root
>>> conn.insert("test", {"name": "Python-Test", "age": 15})
>>> conn.get("test")
[('Python-Test', 15)]
>>> conn.update("test", changes={"age": "20"}, condition={"name": "Python-Test"})
>>> conn.delete("test", condition={"name": "Python-Test"})
```

For more details, please check example.py

Sorry, but in this version, you couldn't create a table with lightmysql.

## Contact

[mail@yixiangzhilv.com](mailto:mail@yixiangzhilv.com)

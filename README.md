# Bilnn-Python-SDK

这是基于比邻云盘官方API的一份Python打包版，拥有Webdav账号和密码后可方便登录使用。

安装：
`pip3 install bilnn`

示例代码：
```Python

import bilnn
pan = bilnn.Bilnn("abc@example.com", "PASSWORD")  # Bilnn("你的WebDav账号", "你的WebDav密码")
print(pan.upload("D:/1.txt", "/1.txt"))  # pan.upload("本地文件路径", "云端保存路径"))
print(pan.get_url("/1.txt"))  # pan.get_url("云端文件路径")
print(pan.list_dir("/"))  # pan.list_dir("云端目录路径")
print(pan.move("/1.txt", "/2.txt"))  # pan.move("云端原始文件或文件夹名", "云端更改后的文件或文件夹名")
print(pan.delete("/2.txt"))  # pan.delete("云端文件路径")
```

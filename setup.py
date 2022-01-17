from setuptools import setup, find_packages

setup(
    name="lightmysql",
    version="1.1.5",
    description="The improved-package of pymysql.",
    py_modules=["lightmysql"],
    long_description="The improved-package of pymysql, made by Yixiangzhilv.",
    url="https://github.com/Danny-Yxzl/lightmysql",
    author="Yixiangzhilv",
    author_email="mail@yixiangzhilv.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10"
    ],
    keywords="sql mysql pymysql database",
    install_requires=["pymysql==1.0.2", "pymysql-pool==0.3.4"],
    project_urls={
        "Bug Reports": "https://github.com/Danny-Yxzl/lightmysql/issues",
        "Say Thanks!": "https://www.yixiangzhilv.com/",
        "Source": "https://github.com/Danny-Yxzl/lightmysql",
    })

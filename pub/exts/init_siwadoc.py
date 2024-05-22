from flask import Flask
from flask_siwadoc import SiwaDoc

# siwa = SiwaDoc(app, title="siwadocapi", description="一个自动生成openapi文档的库")


# 或者使用工厂模式
siwa = SiwaDoc(title="siwadocapi", description="一个自动生成openapi文档的库")


# siwa.init_app(app)


def init_siwadoc(app: Flask):
    siwa.init_app(app)

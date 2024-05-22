from gevent import monkey

# 将python标准的io方法，都替换成gevent中同名的方法，遇到io阻塞gevent自动进行协程切换
monkey.patch_all()

from apps.front import create_app
from apps.front.config import Website
from pub.models.models_business import WebsiteInfo

app = create_app()


# 上下文应用处理器
@app.context_processor
def app_info():
    website_info = WebsiteInfo.query.first()
    website = dict(
        name=Website.name,
        domain=Website.domain,
        keyword=Website.keyword,
        description=Website.description,
        qq=Website.qq,
        logo=website_info.logo,
        logoDark=website_info.logo_dark
    )
    return dict(website=website)


if __name__ == '__main__':
    app.run(port=8080)

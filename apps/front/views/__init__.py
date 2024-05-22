from apps.front.views.author import register_author_views
from apps.front.views.book import register_book_views
from apps.front.views.file import register_file_views
from apps.front.views.friendlink import register_friend_link_views
from apps.front.views.index import register_index_views
from apps.front.views.news import register_news_views
from apps.front.views.passport import register_passport_views
from apps.front.views.pay import register_alipay_views
from apps.front.views.user import register_user_views


def init_view(app):
    register_index_views(app)
    register_book_views(app)
    register_friend_link_views(app)
    register_user_views(app)
    register_passport_views(app)
    register_file_views(app)
    register_author_views(app)
    register_news_views(app)
    register_alipay_views(app)

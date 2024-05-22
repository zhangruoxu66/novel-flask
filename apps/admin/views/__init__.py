from apps.admin.views.admin import register_admin_views
from apps.admin.views.author import register_author_views
from apps.admin.views.book import register_book_views
from apps.admin.views.booksetting import register_book_setting_views
from apps.admin.views.department import register_dept_views
from apps.admin.views.index import register_index_views
from apps.admin.views.member import register_member_views
from apps.admin.views.news import register_news_views
from apps.admin.views.order import register_order_views
from apps.admin.views.passport import register_passport_views
from apps.admin.views.plugin import register_plugin_views
from apps.admin.views.reports import register_reports_views
from apps.admin.views.rights import register_rights_view
from apps.admin.views.website import register_website_views


def init_view(app):
    register_admin_views(app)
    register_index_views(app)
    register_rights_view(app)
    register_passport_views(app)
    register_dept_views(app)
    register_plugin_views(app)
    register_member_views(app)
    register_website_views(app)
    register_book_setting_views(app)
    register_book_views(app)
    register_news_views(app)
    register_order_views(app)
    register_author_views(app)
    register_reports_views(app)

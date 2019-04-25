import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from xadmin.layout import Fieldset, Main, Side, Row

from .models import UserProfile, EmailVerifyRecord, Banner

# class UserProfileAdmin(UserAdmin):
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
#                 Main(
#                     Fieldset('',
#                              'username', 'password',
#                              css_class='unsort no_title'
#                              ),
#                     Fieldset(('Personal info'),
#                              Row('first_name', 'last_name'),
#                              'email'
#                              ),
#                     Fieldset(('Permissions'),
#                              'groups', 'user_permissions'
#                              ),
#                     Fieldset(('Important dates'),
#                              'last_login', 'date_joined'
#                              ),
#                 ),
#                 Side(
#                     Fieldset(('Status'),
#                              'is_active', 'is_staff', 'is_superuser',
#                              ),
#                 )
#             )
#         return super(UserAdmin, self).get_form_layout()

class BaseSetting(object):#修改主题
    enable_themes = True   #使用主题功能
    use_bootswatch = True


class GlobalSettings(object): #修改界面
    site_title = "学习的管理系统"
    site_footer = "学习在线网"
    menu_style = "accordion"# 页标收纳


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']#展示字段
    search_fields = ['code', 'email', 'send_type']#搜索字段
    list_filter = ['code', 'email', 'send_type', 'send_time']#筛选字段
    model_icon = 'fa fa fa-address-book-o'


class BannerAdmin(object):#继承object
    list_display = ['title', 'image', 'url', 'index', 'add_time']  # 展示字段
    search_fields = ['title', 'image', 'url', 'index']  # 搜索字段
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 筛选字段
    model_icon = 'fa fa-window-restore'


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)#注册xadmin
xadmin.site.register(views.CommAdminView, GlobalSettings)#修改界面
# coding:utf-8

import xadmin
from xadmin.views import BaseAdminPlugin, ListAdminView
from django.template import loader


#excel 导入
class ListImportExcelPlugin(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)


    #重置该函数可以将标签放入Xadmin上部
    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toolbar.import.html'))


xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
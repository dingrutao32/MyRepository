import xadmin

from .models import Course, Lesson, Video, CourseResource, BannerCourse
from organization.models import CourseOrg

class LessonInline(object):
    model = Lesson
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'is_banner', 'degree', 'learntime', 'students','fav_nums', 'image', 'click_nums', 'add_time', 'get_zj_nums', 'go_to']  # 展示字段
    search_fields = ['name', 'desc', 'detail', 'is_banner',  'degree', 'learntime', 'students']  # 搜索字段
    list_filter = ['name', 'desc', 'detail', 'degree', 'learntime', 'students','fav_nums', 'image', 'click_nums', 'add_time']  # 筛选字段
    ordering = ['click_nums']
    reasonly_fields = ['click_nums']
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    #指明某字段采用何种样式
    style_fields = {'detail':'ueditor'}
    import_excel = True
    #refresh_times = [3, 5]  设置刷新时间

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs


    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)

    def save_models(self):
        #保持课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org)
            course_org.save()

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learntime', 'students','fav_nums', 'image', 'click_nums', 'add_time']  # 展示字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'learntime', 'students']  # 搜索字段
    list_filter = ['name', 'desc', 'detail', 'degree', 'learntime', 'students','fav_nums', 'image', 'click_nums', 'add_time']  # 筛选字段
    ordering = ['click_nums']
    reasonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs

class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']  # 展示字段
    search_fields = ['course', 'name']  # 搜索字段
    list_filter = ['course__name', 'name', 'add_time'] #__外键COURSE字段


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']  # 展示字段
    search_fields = ['lesson', 'name']  # 搜索字段
    list_filter = ['lesson', 'name', 'add_time']  # __外键COURSE字段


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']  # 展示字段
    search_fields = ['course', 'name', 'download']  # 搜索字段
    list_filter = ['course', 'name', 'download', 'add_time']  # __外键COURSE字段


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
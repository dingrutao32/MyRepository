import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q#进行多重输入验证
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password #对明文进行加密
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifypwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequireMixin
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course
from .models import Banner


class CustomBackend(ModelBackend):
    """
    判断登录用户是否已经注册并合法,
    自定义后台登录验证，现在用到了Q查询，登录时可以通过手机号码登录，django自带的只可以用户名登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveUserVier(View):#客户验证激活
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_file.html")
        return render(request, "login.html")

class RegisterView(View):#注册views
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)#传入后台参数初始化form
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):#查询用户是否注册
                return render(request, "register.html", {"register_form":register_form, "mag":"用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = "欢迎注册学习在线网"
            user_message.save()

            send_register_email(user_name,"register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))



class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST) #先前验证，减轻数据库负担
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户名或密码错误!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误!", "login_form":login_form})
class ForgetPwdView(View):#密码找回视图
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form":forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)#验证form是否合法
        if forget_form.is_valid():#如果合法，发送邮件
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


class ResetView(View):#客户验证激活
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email":email})
        else:
            return render(request, "active_file.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifypwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {"email":email, "modify_form":modify_form})
# Create your views here.
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg":"用户名或密码错误!"})
#     elif request.method == "GET":
#         return render(request, "login.html", {})

class UserInfoView(LoginRequireMixin,View):
    """
    用户个人信息
    """
    def get(self, reuqest):
        return render(reuqest, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                "{'status':'success'}",
                content_type='application/json')
        else:
            return HttpResponse(json.dump(user_info_form.errors),
                                content_type='application/json')

class UploadImageView(LoginRequireMixin, View):
    """
    用户修改头像
    """
    @method_decorator(csrf_exempt)
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # 这里不用拿它的字段了，定义了modelForm，只要验证成功了，可以直接保存
            # print(image,'image')
            image_form.save()
            # return HttpResponse('ok')
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status':'fail'}", content_type='application/json')


class UpdatePwdView(View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifypwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse("{'status':'fail', 'msg':'密码不一致'}", content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse(json.dump(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequireMixin, View):
    """
    发送邮箱验证码
    """
    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse("{'email':'邮箱已经存在'}", content_type='application/json')
        send_register_email(email, "update_email")

        return HttpResponse("{'status':'success'}", content_type='application/json')

class UpdateEmailView(LoginRequireMixin, View):
    """
    修改个人邮箱
    """
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse("{'status':'success'}", content_type='application/json')
        else:
            return HttpResponse("{'email':'验证码出错'}", content_type='application/json')


class MyCourseView(LoginRequireMixin, View):
    """
    我的课程
    """
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {
            'user_courses':user_courses

        })


class MyFavOrgView(LoginRequireMixin, View):
    """
    我收藏的课程机构
    """
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {
            'org_list':org_list

        })


class MyFavTeacherView(LoginRequireMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list':teacher_list

        })


class MyFavCourseView(LoginRequireMixin, View):
    """
    我收藏的授课讲师
    """
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html', {
            'course_list':course_list

        })


class MymessageView(LoginRequireMixin, View):
    """
    我的消息
    """
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        #用户进入个人消息后清空未读提醒
        all_unread_messages = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        # 对我的消息分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_message, 1, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            "messages":messages

        })


class IndexView(View):
    #慕学在线网首页
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:5]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs

        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response

def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
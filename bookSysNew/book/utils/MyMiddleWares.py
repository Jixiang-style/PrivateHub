from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class M1(MiddlewareMixin):
    def process_request(self, request):
        # print("M1 process_request")
        # 拦截,原路返回
        # return HttpResponse("Forbidden!")
        pass

    def process_response(self, request, response):
        # print("M1 process_response")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # print("Md1view")
        # print("Md1 callback", callback)
        # print("Md1 callback_args", callback_args)
        res = callback(request, *callback_args)
        return res


class M2(MiddlewareMixin):
    def process_request(self, request):
        # print("M2 process_request")
        pass

    def process_response(self, request, response):
        # print("M2 process_response")
        return response

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # print("Md2view")
        # print("Md2 callback", callback)
        # print("Md3 callback_args", callback_args)
        pass


class LoginAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("访问路径", request.path)
        if request.path in ["/login_auth/", "/find/", "/books/", "/", "/register/", "/admin/"]:
            return None

        if not request.user.id:
            print("验证userid")
            return redirect("/login_auth/")

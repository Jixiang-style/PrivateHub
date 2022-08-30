import json
import time

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

from book.models import Publish, Author, Book, AuthorDetail, User

from django.contrib import auth


def zhuang(func):
    def newfunc(request, *args, **kwargs):
        if not request.session.get('is_login') == 'true':
            return redirect('/login/')
        else:
            return func(request, *args, **kwargs)

    return newfunc


# todo 待完善
def findBook(request):
    """
    查询书籍

    :param request:
    :type request:
    :return:
    :rtype:
    """
    title = request.POST.get("keyword")
    print("搜索内容:", title)
    if len(title) > 32 or len(title) < 1:
        msg = "书名不合法！！"
        print(msg)
        return render(request, "books.html", locals())
    book_list = Book.objects.filter(title__regex="{}.*".format(title)).all()
    print(book_list.values())
    return render(request, "findbooks.html", locals())


def addBook(request):
    if request.method == "GET":

        publish_list = Publish.objects.all()
        author_list = Author.objects.all()
        return render(request, "addbook.html", {"publish_list": publish_list, "author_list": author_list})
    else:
        # 取数据
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pubdate")
        publish_id = request.POST.get("publish")
        authors_id = request.POST.getlist("authors")
        print(publish_id)
        print(authors_id)

        book = Book.objects.create(title=title, price=price, pub_date=pub_date, publisher_id=publish_id)
        book.authors.add(*authors_id)

        return redirect("/books/")


def books(request):
    # 取cookie判断
    # print (request.COOKIES)
    # if not request.COOKIES.get("is_login") == 'True':
    #     return redirect("/login/")
    # else:
    # 取session判断
    # if not request.session.get("is_login")=="true":
    #     '''
    #     request.session["is_login"]
    #     1 sessionid=request.COOKIES.get("sessionid")
    #     2 在django-session表中筛选记录
    #       django-session
    #              session-key             session-data
    #              1234asd234cvsxz234      {"is_login":"true","username":"alex"}
    #     3 查询出的session-data["is_login"]
    #
    #     '''
    #     return redirect("/login/")
    # 根据用户认证组件语法判断是否登陆
    # if 1:
    #     pass
    # else:
    # if not request.user.id:
    # if not request.user.is_authenticated:
    #     print (request.user)
    #     print (request.user.id)
    #     print (request.user.username)
    #     print (type(request.user))
    #     return redirect("/login/")
    # else:
    # import time
    # time.sleep(20)
    books = Book.objects.all()  # 分页数据
    current_page = int(request.GET.get("page", 1))
    paginator = Paginator(books, 5)
    if paginator.num_pages < 11:
        # 分页数小于11
        page_range = paginator.page_range
    else:
        if current_page - 5 <= 0:
            page_range = range(1, 12)
        elif current_page + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            page_range = range(current_page - 5, current_page + 6)

    page = paginator.get_page(current_page)
    book_list = page
    # book_list = Book.objects.all()
    # username=request.COOKIES.get("username")
    # username=request.session.get("username")
    # username=request.user.username
    return render(request, "books.html", locals())


def deleteBooks(request, pk):
    Book.objects.filter(id=pk).delete()
    return redirect("/books/")


def editBooks(request, pk):
    if request.method == "GET":
        publish_list = Publish.objects.all()
        author_list = Author.objects.all()

        edit_book = Book.objects.get(id=pk)
        return render(request, "editbook.html", locals())
    else:
        # 取数据
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pubdate")
        publish_id = request.POST.get("publish")
        authors_id = request.POST.getlist("authors")

        Book.objects.filter(id=pk).update(title=title, price=price, pub_date=pub_date, publisher_id=publish_id)
        book = Book.objects.get(id=pk)
        book.authors.set(authors_id)

        return redirect("/books/")


def get_publishes(request):
    data = list(Publish.objects.all().values("name", "email"))
    print("data", data)
    return HttpResponse(json.dumps(data, ensure_ascii=False))


def ajax_del(request):
    res = {"flag": True}
    try:
        pk = request.GET.get("pk")
        Book.objects.filter(id=pk).delete()
    except Exception as e:
        res["flag"] = False
    return HttpResponse(json.dumps(res))


def cal_add(request):
    num1 = request.POST.get("num1")  # "1"
    num2 = request.POST.get("num2")  # "2"
    print(num1, num2)
    ret = float(num1) + float(num2)
    res = {"ret": ret}
    return JsonResponse(res)


def register(request):
    """
    注册（admin站点注册）
    :param request:
    :type request:
    :return:
    :rtype:
    """
    if request.method == "GET":
        print("register")
        request.session.cycle_key()
        return redirect("/admin/")


def login(request):
    if request.method == "GET":
        print("get方法")
        return render(request, "login.html")
    else:
        # 取数据判断用户是否登录
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        user = User.objects.filter(name=name, pwd=pwd).first()
        if user:
            msg = '登录成功，欢迎 %s！' % name
            print(msg)
            # 登录成功
            # res_obj=HttpResponse("登录成功!")
            # res_obj=redirect("/")
            # 写cookie
            # res_obj.set_cookie("is_login",True,max_age=20)
            # res_obj.set_cookie("username",user.name)
            # 写session
            request.session["is_login"] = "true"
            request.session["username"] = user.name
            '''
            request.session["is_login"]="true"
            1 创建随机字符串  1234asd234cvsxz234
            2 在django-session表中添加记录
                django-session
                session-key             session-data
                1234asd234cvsxz234      {"is_login":"true","username":"alex"}
            3 res.set_cookie("sessionid","1234asd234cvsxz234")                    
            '''
            return redirect('/books/')
        else:
            err_msg = "用户名或者密码错误"
            return render(request, "login.html", {"err_msg": err_msg})


def logout(request):
    request.session.flush()
    '''
    1  取钥匙
    2  筛选django-session记录
    3  删除记录
    '''
    return redirect("/login/")


###################
# 用户认证组件
###################

def login_auth(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # 取数据判断用户是否登录(默认：alex/123 )
        name = request.POST.get("username")
        pwd = request.POST.get("password")
        user = auth.authenticate(username=name, password=pwd)
        if user:
            msg = '登录成功，欢迎 %s！' % name
            print(msg)
            # request.session["user_id"]=user.id
            auth.login(request, user)
            return redirect('/books/')
        else:
            err_msg = "用户名或者密码错误"
            print(err_msg)
            return render(request, "login.html", {"err_msg": err_msg})


def logout_auth(request):
    auth.logout(request)
    return redirect("/login/")

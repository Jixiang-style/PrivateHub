from django.shortcuts import render, HttpResponse

# Create your views here.
from .models import Book
from django.core.paginator import Paginator


def books(request):
    '''
     # 批量插入数据
     # for i in range(1,101):
     #     Book.objects.create(name="book_%s"%i,price=2*i+100)

     # book_list=[]
     # for i in range(1,101):
     #     book=Book(name="book_%s"%i,price=2*i+100)
     #     book_list.append(book)
     #
     # Book.objects.bulk_create(book_list)



        paginator=Paginator(books,10)
        print (paginator.count) # 分页数据的总数
        print (paginator.num_pages) # 10
        print (paginator.page_range) # range(1,11)
        page_1=paginator.get_page(1)
        print (page_1.has_next())
        print (page_1.has_previous())
        print (page_1.next_page_number())
        # print (page_1.previous_page_number())
        # print (page_1.object_list)

        # for i in page_1:
        #     i

    :param request:
    :return:
    '''

    books = Book.objects.all()  # 分页数据
    current_page = int(request.GET.get("page", 1))
    paginator = Paginator(books, 2)
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

    return render(request, "app02/books.html", locals())

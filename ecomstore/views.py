from django.shortcuts import render
# from django.http import HttpResponseNotFound
# why its 500 error expected 404


def file_not_found_404(request):
    page_title = 'Page Not Found'
    # return HttpResponseNotFound()
    return render(request, '404.html', context=locals())

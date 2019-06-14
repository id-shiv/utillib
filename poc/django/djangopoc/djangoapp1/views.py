from django.shortcuts import render
# from django.http import HttpResponse


def greet(request):
    return render(request, template_name='djangoapp1/index.html')

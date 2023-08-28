from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.translation import activate
from urllib.parse import urlparse, urlunparse


def home(request):
    return render(request, 'home/home_page.html')


def about(request):
    return render(request, 'home/about.html')


def lang_switcher(request, user_language):
    activate(user_language)
    # Redirect the user back to the previous page
    parsed_url = list(urlparse(request.META.get('HTTP_REFERER')))
    path_parts = parsed_url[2].split('/')
    path_parts[1] = user_language
    parsed_url[2] = '/'.join(path_parts)
    return redirect(urlunparse(parsed_url))  # redirect(urlunparse(parsed_url))



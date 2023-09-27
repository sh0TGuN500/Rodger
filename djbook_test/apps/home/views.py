from os import getenv
from urllib.parse import urlparse, urlunparse

import ipinfo
from django.shortcuts import render, redirect
from django.utils.translation import activate
from .models import GuestData


def user_checker(address):
    access_token = getenv('ADDR_CHECK_API')
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(address)
    return details.all


def get_address(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        address = request.META['HTTP_X_FORWARDED_FOR']
        return address
    else:
        return request.META['REMOTE_ADDR']


def home(request):
    user = request.user
    device_data = request.META
    address = get_address(request)
    address_data = user_checker(address)
    new = GuestData(user=user, device=device_data, address=address_data)
    new.save()
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
    response = redirect(urlunparse(parsed_url))
    response.set_cookie('django_language', user_language)
    return response  # redirect(urlunparse(parsed_url))



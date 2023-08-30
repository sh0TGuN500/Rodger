from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import activate

from .settings import LANGUAGES


class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.COOKIES.get('django_language', None)
        if not language:
            user_language = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0]
            lang_list = [lang[0] for lang in LANGUAGES]
            if user_language in lang_list:
                language = user_language
            else:
                language = 'en'
            response = redirect(reverse('home:home'))
            response.set_cookie('django_language', language)
            activate(language)
        else:
            response = self.get_response(request)
        return response


'''
else:
    current_language = request.path_info.strip('/').split('/')[0]
    if current_language == language:
        response = self.get_response(request)
    else:
        activate(language)
        response = redirect(reverse('home:home'))
return response
'''

# -*- encoding: utf-8 -*-


from front.urls import front_urls
from api.urls import child_urls

urls = []
urls.extend(front_urls)
urls.extend(child_urls)
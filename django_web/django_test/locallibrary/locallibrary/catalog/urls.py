from django.urls import path
from . import views


urlpatterns = [
    # path("templates/catalog/",views.button_click_view,name='button_click'),
	path("templates/catalog/test.html",views.my_view),
	path("templates/catalog/show_stocks.html",views.show_stocks),
	path("templates/catalog/show_stocks.html",views.show_stocks,name='return_date'),
	path("templates/catalog/test2.html",views.test2),
]

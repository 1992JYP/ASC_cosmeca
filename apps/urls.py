from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from apps.main import views
from apps.main.views import ModelCreateView 

urlpatterns = [
    
    path('', include('apps.users.urls')),
    path('item_search/', include('crawling.urls')),
    path('django_task/', include('django_task.urls', namespace='django_task')),
    # path('test/',views.get_post, name='test'),
    # path('btntest/', views.responsetest),
    # path('', views.login, name='home'),
    # path('', views.login, name='login'),
    ### jyp url test 210614
    # path('test/',views.dbtest, name='btntest'),
    ###
    # # path('btntest/', views.responsetest, name='btntest2')
    # path('btntest/', views.btntest, name='btntest'),
    # path('btntest2/',views.btntest, name='btntest2' )

    path('dbtest/',views.dbtest, name = 'dbset'),
    path('test/',views.dbtest, name='dbtest'),
    path('admin/', admin.site.urls),
    path('keyword/', views.keyword, name='keyword'),
    path('review/', views.review, name='review'),
    path('Dashboard/',views.Dashboard, name = 'Dashboard'),
    path('Dashboard/',views.Dashboard, name = 'chart'),
    path('main/',views.main, name = 'main'),
    path('create/', ModelCreateView.as_view() ,name='create'),
    # path('main',views.main, name = 'main'),
    path('review_Dashboard/', views.review_Dashboard ,name='review_Dashboard'),
    


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns


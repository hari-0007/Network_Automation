from django.contrib.auth import views
from django.urls import path
from basicapp import views

# SET THE NAMESPACE!
app_name = 'basicapp'


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home,name='home'),
    path('scan/', views.scan,name='scan'),
    path('nmapscan/', views.nmapscan,name='nmapscan'),
    path('nmapview/',views.view_nmap,name='nmapview'),
    path('pcapview/',views.view_pcap,name='pcapview'),
    path('downloadpage/',views.download_cap,name='form_download'),
    path('scandownload/',views.scan_download_pcap,name='form_scan'),
    path('nmapdownload/',views.download_nmap,name='form_nmap'),
    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('download/', views.download_pcap,name='download'),
    path('userform/', views.showform,name='newform'),
    path('client_home/',views.client_home,name='client_home'),
    path('client/',views.client,name='client'),
    path('client_show/',views.client_show,name='client_show'),
    path('edit/<int:id>',views.client_edit,name='client_edit'),
    path('update/<int:id>',views.client_update,name='client_update'),
    path('delete/<int:id>',views.client_delete,name='client_delete'),

]

from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url

app_name = "articles"

urlpatterns = [
path('schedule/', ScheduleView.as_view()),

path('getmaster/', GetMasterView.as_view()),
path('updatemaster/', UpdateMasterView.as_view()),
path('master/', MasterView.as_view()),
path('masterlist/', MasterlistView.as_view()),
path('addemployee/', AddmasterView.as_view()),
path('delempl/', DelemployeeView.as_view()),

path('client/', ClientView.as_view()),
path('clientall/', ClientAllView.as_view()),
path('updateclientcard/', UpdateClientCartView.as_view()),
path('editclient/', EditClientView.as_view()),
path('addclientcard/', AddClientCartView.as_view()),
path('newclient/', NewclientView.as_view()),
path('changestatus/', ChangeStatusView.as_view()),
path('deletezapis/', DeletezapisView.as_view()),
path('notcome/', NotComezapisView.as_view()),
path('updateclient/', UpdateclientView.as_view()),
path('delcli/', DelClientView.as_view()),


path('serviceall/', ServiceAllView.as_view()),
path('editservice/', EditServiceView.as_view()),
path('updateservice/', UpdateServiceCartView.as_view()),
path('addservice/', AddServiceView.as_view()),
path('delservice/', DelServiceView.as_view()),


path('allzapis/', ZapisAllView.as_view()),


path('allspec/', AllSpecView.as_view()),

path('workcalendar/', WorkcalendarPostView.as_view()),
path('getworkcalendar/', GetWorkcalendarView.as_view()),

path('smspost/', SmsPostView.as_view()),
path('getsms/', GetSMSView.as_view()),

path('allstatus/', StatAllView.as_view()),
path('clientcount/', ClientCountView.as_view()),
path('uslugi/', UslugiChartView.as_view()),
path('masterchart/', MasterChartView.as_view()),

path('companyall/', CompanyAllView.as_view()),
path('getcompany/', GetCompanyView.as_view()),
path('savecompany/', SaveCompanyView.as_view()),
path('addcompany/', AddCompanyView.as_view()),

path('usersall/', UsersAllView.as_view()),
path('getuser/', GetUserView.as_view()),
path('saveuser/', SaveUserView.as_view()),
path('adduser/', AddUserView.as_view()),
path('loadfirm/', LoadfirmView.as_view()),
path('loadpayments/', LoadpaymentsView.as_view()),
path('addtarif/', AddpaymentsView.as_view()),
path('addsms/', AddSMSView.as_view()),

path('getstatus/', GetStatusFirmView.as_view()),

path('logs/', LogsView.as_view()),

path('yandex/', YandexView.as_view()),
path('yandexsucess/', YandexsuccessView.as_view()),
path('yandexcheck/', YandexcheckView.as_view()),
path('yandexaviso/', YandexavisoView.as_view()),
path('yandexerror/', YandexfailView.as_view()),

]
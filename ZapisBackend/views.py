from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import requests

import datetime
from datetime import timedelta

from zapis.models import *

# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
def sendemail(request):
    # def post(self, request, *args, **kwargs):
        username = request.data['username']
        email = request.data['email']
        phone = request.data['phone']

        text="Заявка на визитер"
        body="Имя %s   Email: %s    Телефон: %s" %(username, email, phone)

        # send_email_meesage(text, body)


        # send_mail(text,
        #           body,
        #           'info@sitealert.ru',
        #           ['kairo@list.ru', 'akoibagaroff@gmail.com'], fail_silently=False, )

        return Response({'ok': 1},
                    status=HTTP_200_OK)


def sendtelegrammmes(username,email,phone):
    # def post(self, request, *args, **kwargs):
        print("Sendemail!")

        text="Заявка на визитер"
        body="Имя %s   Email: %s    Телефон: %s" %(username, email, phone)

        # send_email_meesage(text, body)

        try:
            send_mail(text,
                      body,
                      'info@sitealert.ru',
                      ['kairo@list.ru', 'akoibagaroff@gmail.com'], fail_silently=False, )
        except:
            pass

        try:
            cont = "425750182"
            urlsms = "https://api.telegram.org/bot874312188:AAF4sZqc1rzs49qA5TfyY_hWE-_uN8eURaA/sendMessage?chat_id={0}&text={1}".format(
                cont, text+ ' '+body)
            response = requests.post(urlsms, headers={'Content-Type': 'application/xml; charset=UTF-8'})
            cont = "407110866"
            urlsms = "https://api.telegram.org/bot874312188:AAF4sZqc1rzs49qA5TfyY_hWE-_uN8eURaA/sendMessage?chat_id={0}&text={1}".format(
                cont, text + ' ' + body)
            response = requests.post(urlsms, headers={'Content-Type': 'application/xml; charset=UTF-8'})
        except:
            pass


        return Response({'ok': 1},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
    except:
        pass

    if username is None:
        username = request.data['user']
        email = request.data['email']
        phone = request.data['phone']
        print(username,email, phone)
        sendtelegrammmes(username, email, phone)
        return Response({'ok': 1},
                    status=HTTP_200_OK)

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    firma = user.userprofile.firma.name        #user.firma_set.all()[0].name
    idfirma = user.userprofile.firma.id      #user.firma_set.all()[0].id
    login = user.username
    token, _ = Token.objects.get_or_create(user=user)
    try:
        role = user.groups.all()[0].name
    except:
        role= 'guest'
    return Response({'token': token.key, 'firma': firma, 'login': login, 'idfirma':idfirma, 'role':role},
                    status=HTTP_200_OK)



#-----------------------------------------------------------------------------------------------------------------

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newbooking(request):
    try:
        idfirma = request.data.get("idfirma")

    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)

    today = datetime.datetime.today().date()
    nomday = today.weekday() + 1
    spiswork=[]
    num=0
    for i in range(0,30):
        op={}

        dat = today+timedelta(i)
        nomday = dat.weekday() + 1
        master = Master.objects.filter(firma_id=idfirma, id=1)
        for mst in master:
            num += 1
            wkday = Workday.objects.filter(firma_id=idfirma,  master=mst, nomday=nomday)
            if len(wkday) > 0:
                op['time'] = dat
                op['id'] = num
                op['busy'] = 0
                op['idmaster'] = mst.id
            else:
                op['time'] = dat
                op['id'] = num
                op['busy'] = 1
                op['idmaster'] = mst.id
            spiswork.append(op)


    Company= Firma.objects.get(id=idfirma).name

    specall = Spec.objects.filter(firma_id=idfirma)
    spisspec=[]
    for spec in specall:
        op={}
        op['id'] = spec.id
        op['name'] = spec.name
        op['price'] = spec.price
        spisspec.append(op)

    mast = Master.objects.filter(firma_id=idfirma)
    spismaster = []
    for mst in mast:
        op = {}
        op['id'] = mst.id
        op['name'] = mst.fio
        # op['idspec'] = mst.spec.id
        try:
            op['img'] = "https://apivisiter.ru" + mst.photo.url  # "
        except:
            op['img'] = "img/avatars/nobody.jpg"
        spismaster.append(op)

    return Response({'company': Company, 'services':spisspec, 'masters':spismaster, 'dates': spiswork},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newmasters(request):
    try:
        idfirma = request.data.get("idfirma")
        idservice = request.data.get("idservice")
    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)


    mast = Master.objects.filter(firma_id=idfirma, spec__id=idservice)
    spismaster = []
    for mst in mast:
        op = {}
        op['id'] = mst.id
        op['name'] = mst.fio
        # op['idspec'] = mst.spec.id
        try:
            op['img'] = "https://apivisiter.ru" + mst.photo.url  # "
        except:
            op['img'] = "img/avatars/nobody.jpg"
        spismaster.append(op)

    return Response({ 'masters':spismaster},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newgetcompany(request):
    try:
        idfirma = request.data.get("idfirma")

    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)



    nameCompany = Firma.objects.filter(id=idfirma)[0].name


    return Response({ 'company':nameCompany},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newservice(request):
    try:
        idfirma = request.data.get("idfirma")

    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)



    specall = Spec.objects.filter(firma_id=idfirma)
    spisspec=[]
    for spec in specall:
        op={}
        op['id'] = spec.id
        op['name'] = spec.name
        op['price'] = spec.price
        spisspec.append(op)



    return Response({ 'services':spisspec},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newdate(request):
    try:
        idfirma = request.data.get("idfirma")
        id_newmaster = request.data.get("id_newmaster")

    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)

    today = datetime.datetime.today().date()
    nomday = today.weekday() + 1
    spiswork = []
    num = 0
    mst = Master.objects.filter(firma_id=idfirma, id=id_newmaster)[0]
    wkday = [x.nomday for x in Workday.objects.filter(firma_id=idfirma, master=mst)]        #Workday.objects.filter(firma_id=idfirma, master=mst)
    vacation = Vacation.objects.filter(firma_id=idfirma, master=mst)
    vacstart = ''
    vacend = ''
    if len(vacation)>0:
        vacstart= vacation[0].datestart
        vacend=vacation[0].dateend
    for i in range(0, 30):
        op = {}

        dat = today + timedelta(i)
        nomday = dat.weekday() + 1

        # for mst in master:
        num += 1


        # wkday = Workday.objects.filter(firma_id=idfirma, master=mst, nomday=nomday)
        if nomday in wkday :  # len(wkday) > 0
            op['time'] = dat
            op['id'] = num
            op['busy'] = 0
            op['idmaster'] = mst.id
        else:
            op['time'] = dat
            op['id'] = num
            op['busy'] = 1
            op['idmaster'] = mst.id

            # Vacation
        if len(str(vacstart)) > 0:
            if dat >= vacstart and dat <= vacend:
                op['busy'] = 1
        spiswork.append(op)



    return Response({ 'dates':spiswork},
                    status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newtime(request):
    try:
        idfirma = request.data.get("idfirma")
        newdate = request.data.get("newdate")
        idmaster = request.data.get("idmaster")
    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)


    zapis = [x for x in Zapis.objects.filter(firma_id=idfirma, master_id = idmaster, datezapis = newdate)]

    work = Workcalendar.objects.filter(firma_id=idfirma)
    ok = 1
    begin = work[0].start  # work[0].start
    endtime = work[0].end  # work[0].end
    # client = Client.objects.all()
    start = int(begin.split(':')[0])
    end = int(endtime.split(':')[0])
    worktime = []
    num=1
    for i in range(start, end):
        op = {}
        st = str(i) + ':00'
        ok=0
        op['busy'] = 0
        for zp in zapis:
           if  int(st.split(':')[0]) >= int(zp.begin.split(':')[0]) and int(st.split(':')[0]) <= int(
                zp.end.split(':')[0]):
               ok=1
               op['busy'] = 1
               break
        # if ok ==0:
        op['time'] = st
        op['id'] = num

        worktime.append(op)
        num+=1
        # worktime.append(st)
        # st2 = str(i) + ':30'
        # worktime.append(st2)
    # st = str(i + 1) + ':00'
    # worktime.append(st)



    return Response({ 'times':worktime},
                    status=HTTP_200_OK)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Newzapis(request):
    try:
        fio = request.data['fio'].strip()
        phone = request.data['phone'].strip()
        time_begin = request.data['time_begin'].strip()
        time_end = request.data['time_end'].strip()
        master = request.data['master']
        spec = request.data['spec']
        idfirma = request.data['idfirma']

    except:
        return Response({'error': 1},
                        status=HTTP_400_BAD_REQUEST)


    date_srez = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()

    if Client.objects.filter(fio=fio, firma_id=idfirma, phone=phone).count() == 0:
        cl = Client(fio=fio, phone=phone, firma_id=idfirma)
        cl.save()
    else:
        cl = Client.objects.get(fio=fio, firma_id=idfirma, phone=phone)

    mast = Master.objects.get(id=master, firma_id=idfirma)
    #  Check time master
    result = check_time(mast, date_srez, time_begin, time_end, idfirma)
    if result == 1:
        return Response({'ok': False})

    if Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis=date_srez,
                            status__lt=2).count() == 0:
        a = Zapis(client=cl, master=mast, firma_id=idfirma, begin=time_begin, end=time_end, datezapis=date_srez,
                  usluga_id=spec)
        a.save()
    else:
        return Response({'ok': False},
                    status=HTTP_200_OK)

    return Response({'ok': True},
                    status=HTTP_200_OK)


def check_time(master, datezapis,time_begin,time_end, idfirma):
    ok=0
    if int(time_begin.split(':')[0]) < 10:
        time_begin = '0'+time_begin.split(':')[0]+':'+time_begin.split(':')[1]
    if int(time_end.split(':')[0]) < 10:
        time_end = '0'+time_end.split(':')[0]+':'+time_end.split(':')[1]
    if Zapis.objects.filter(master=master, firma_id=idfirma, begin__range=(time_begin, time_end), datezapis=datezapis, status__lt=2).count()>0:
        ok=1
        return ok
    if Zapis.objects.filter(master=master, firma_id=idfirma, end__range=(time_begin, time_end), datezapis=datezapis, status__lt=2).count()>0:
        ok=1
        return ok

    return ok

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import *
from .serializers import MasterSerializer
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib.auth.models import User, Group

from yandex_checkout import Configuration, Payment
import requests

from rest_framework import permissions


from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)




class ClientView(APIView):
    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']
        client = Client.objects.filter(firma_id=idfirma).order_by('fio')
        spisok = []
        for mst in client:
            op = {}
            op['fio'] = mst.fio
            op['phone'] = mst.phone
            spisok.append(op)

        return Response({'headers': spisok})

class EditClientView(APIView):
    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']
        id = request.data['id']

        mast = Client.objects.get(id=id, firma_id=idfirma)
        spisok = []
        op = {}
        op['fio'] = mast.fio
        op['phone'] = mast.phone

        return Response({'headers': op})


class UpdateClientCartView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['id']
        fio = request.data['fio']
        phone = request.data['phone']
        idfirma = request.data['idfirma']
        Client.objects.filter(id=id, firma_id=idfirma).update(fio=fio, phone=phone)

        return Response({'ok': True})

class AddClientCartView(APIView):
    def post(self, request, *args, **kwargs):

        fio = request.data['fio']
        phone = request.data['phone']
        idfirma = request.data['idfirma']
        a = Client(fio=fio, firma_id=idfirma, phone=phone)
        a.save()

        return Response({'ok': True})



class ClientAllView(APIView):
    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']

        client = Client.objects.filter(firma_id=idfirma)
        spisok = []
        idb=0
        count=0
        for mst in client:
            op = {}
            id = mst.id
            fio = mst.fio
            phone = mst.phone
            count = Zapis.objects.filter(client=mst,firma_id=idfirma).count()
            op['username'] = fio
            op['tel'] = phone
            op['visitnumber'] = count
            op['note'] = ''
            op['action'] = '/editclient/' + str(id)
            op['id'] = mst.id
            spisok.append(op)



        return Response({'headers': spisok})

class ClientAllView2(APIView):
    def get(self, request):
        client = Zapis.objects.all().order_by('client_id')
        spisok = []
        idb=0
        count=0
        for mst in client:
            op = {}
            id = mst.client.id
            if idb == id or idb==0:
               count+=1
               idb = id
               fio= mst.client.fio
               phone=mst.client.phone

            else:
                op['username'] = fio
                op['tel'] = phone
                op['visitnumber'] = count
                op['note'] = ''
                op['action'] = '/editclient/'+str(idb)
                spisok.append(op)
                count=1
                idb=id
                fio = mst.client.fio
                phone = mst.client.phone


        return Response({'headers': spisok})


class DelClientView(APIView):
    def post(self, request, *args, **kwargs):
        idcli = request.data['idcli']
        name = request.data['name']
        Client.objects.filter(id=idcli).delete()

        ok=1
        return Response({'ok': 1})


#--------------------------------------------------------------------------

class ServiceAllView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        spec = Spec.objects.filter(firma_id=idfirma)
        spisok = []
        idb=0
        count=0
        for mst in spec:
            op = {}
            id = mst.id
            name = mst.name
            time = mst.time
            price = mst.price
            count = Master.objects.filter(spec=mst,firma_id=idfirma).count()
            op['servicename'] = name
            op['term'] = time
            op['cost'] = price
            op['masternumber'] = count
            op['href'] = '/editservice/' + str(id)
            op['id'] = mst.id
            spisok.append(op)



        return Response({'headers': spisok})

class EditServiceView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        id = request.data['id']

        mast = Spec.objects.get(id=id , firma_id=idfirma)
        spisok = []
        op = {}
        op['name'] = mast.name
        op['time'] = mast.time
        op['price'] = mast.price

        return Response({'headers': op})

class UpdateServiceCartView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        id = request.data['id']
        price = request.data['price']
        time = request.data['time']
        name = request.data['name']
        idfirma = request.data['idfirma']

        Spec.objects.filter(id=id, firma_id=idfirma).update(name=name, price=price, time=time)

        return Response({'ok': True})

class AddServiceView(APIView):
    def post(self, request, *args, **kwargs):

        name = request.data['name']
        time = request.data['time']
        price = request.data['price']
        idfirma = request.data['idfirma']
        a = Spec(name=name,firma_id=idfirma, time=time, price=price)
        a.save()

        return Response({'ok': True})

class DelServiceView(APIView):
    def post(self, request, *args, **kwargs):
        idcli = request.data['idcli']
        name = request.data['name']

        Spec.objects.filter(id=idcli).delete()

        return Response({'ok': True})



#------------------------------------------------------------------------------------------

class ZapisAllView(APIView):
    def post(self, request, *args, **kwargs):
        idfirma = request.data['idfirma']
        zap = Zapis.objects.filter(firma_id=idfirma).order_by('-datezapis')
        spisok = []
        idb=0
        count=0
        i=1
        for mst in zap:
            op = {}
            id = mst.id
            master = mst.master.fio
            time = mst.begin + ", "+str(mst.datezapis.day)+'/'+str(mst.datezapis.month)+'/'+str(mst.datezapis.year)
            client = mst.client.fio
            phone = mst.client.phone
            status = mst.status
            if status==0:
                status='В ожидании'
            if status==1:
                status='Завершено'
            if status==2:
                status='Отменено'
            # count = Master.objects.filter(spec=mst).count()
            op['number'] = i
            op['bookingdate'] = time
            op['specialist'] = master
            op['client'] = client
            op['clientphone'] = phone
            op['status'] = status
            op['servicename'] = mst.usluga.name
            op['term'] = '1 час'
            i+=1

            spisok.append(op)



        return Response({'headers': spisok})



#------------------------------------------------------------------------------

class MasterView(APIView):
    def post(self, request, *args, **kwargs):
        #master = Master.objects.all()
        idfirma = request.data['idfirma']
        #serializer = MasterSerializer(master, many=True)
        mast = Master.objects.filter(firma_id=idfirma)
        spisok=[]
        for mst in mast:
            op={}
            op['fio'] = mst.fio
            op['profession'] = mst.profession
            try:
                op['photo'] = "https://apivisiter.ru" + mst.photo.url #"
            except:
                op['photo'] = "img/avatars/nobody.jpg"
            spisok.append(op)

        spec_all = Spec.objects.filter(firma_id=idfirma)
        all_spec = []
        for sp in spec_all:
            op2 = {}
            op2['text'] = sp.name
            op2['value'] = sp.id
            all_spec.append(op2)

        return Response({'headers': spisok, 'specall':all_spec})


class GetMasterView(APIView):
    def post(self, request, *args, **kwargs):

        idfirma = request.data['idfirma']
        id = request.data['id']
        ok=1
        mast = Master.objects.get(id=id , firma_id=idfirma)
        spisok = []
        op = {}
        op['name'] = mast.fio
        op['profession'] = mast.profession
        try:
            op['photo'] = "https://apivisiter.ru" + mast.photo.url #"
        except:
            op['photo'] = "img/avatars/nobody.jpg"

        spec_all = Spec.objects.filter(firma_id=idfirma)
        all_spec = []
        for sp in spec_all:
            op2 = {}
            op2['text'] = sp.name
            op2['value'] = sp.id
            all_spec.append(op2)
        sp_master = mast.spec.filter(firma_id=idfirma)
        spec = []
        for sp in sp_master:
            # op2={}
            # op2['text'] = sp.name
            # op2['value'] = sp.id
            spec.append(sp.id)

        work = Workday.objects.filter(master=mast,firma_id=idfirma)
        workd = []
        for sp in work:
            # op2={}
            # op2['text'] = sp.name
            # op2['value'] = sp.id
            workd.append(sp.nomday)

        vac = Vacation.objects.filter(master=mast,firma_id=idfirma)
        vacday=[]
        for vc in vac:
            vacday = {}
            vacday['date_start'] = vc.datestart
            vacday['date_end'] = vc.dateend
            #vacday.append(op2)

        #op['spec'] = spec
        #spisok.append(op)
        return Response({'headers': op, 'spec':spec, 'all_spec':all_spec, 'workday':workd, 'vacday':vacday})




class UpdateMasterView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        date_start = request.data['date_start']
        date_end = request.data['date_end']
        spec = request.data['spec'].split(',')
        daywork = request.data['daywork'].split(',')
        id = request.data['idmaster']
        idfirma = request.data['idfirma']

        try:
            photo = request.data['files']
            mast = Master.objects.get(id=id, firma_id=idfirma)
            mast.photo = photo
            mast.save()
            #Master.objects.filter(id=id).update(photo=photo)
        except:
            photo=''




        mast = Master.objects.get(id=id, firma_id=idfirma)

        # spec_all = mast.spec.all()
        # for sp in spec_all:
        #     if sp.id in spec:
        #         spec.remove(sp.id)

        mast.spec.clear()

        for sp in spec:
            mast.spec.add(sp)

        # workday = list(Workday.objects.filter(master=mast).values('nomday'))
        # for wk in workday:
        #     if wk['nomday'] in daywork:
        #         ok=1
        #         daywork.remove(wk['nomday'])

        Workday.objects.filter(master=mast, firma_id=idfirma).delete()
        for add  in daywork:
            a = Workday(master=mast,nomday=add, firma_id=idfirma)
            a.save()

        try:
            if len(date_start)>0:
                date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
                date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
                if Vacation.objects.filter(master=mast, firma_id=idfirma).count()==0:
                    a = Vacation(master=mast, firma_id=idfirma, datestart=date_start, dateend=date_end)
                    a.save()
                else:
                    Vacation.objects.filter(master=mast, firma_id=idfirma).update(datestart=date_start, dateend=date_end)
        except:
            pass

        ok=True
        return Response({'ok': ok})




class MasterlistView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']

        mast = Master.objects.filter(firma_id=idfirma)
        spisok = []
        for mst in mast:
            all = {}

            op = {}
            try:
                op['url'] = "https://apivisiter.ru" + mst.photo.url  # "
            except:
                op['url'] = "img/avatars/nobody.jpg"
            op['status'] = 'danger'
            all['avatar'] = op
            op = {}
            op['name'] = mst.fio
            op['new'] = 'true'
            op['registered'] = 'Jan 1, 2015'
            all['user'] = op
            op = {}
            sp_all = mst.spec.filter(firma_id=idfirma)
            spec = ''
            for sp in sp_all:
                spec += sp.name + ' , '
            op['name'] = spec
            all['usage'] = op
            op = {}
            op['name'] = 'Сотрудник'
            all['payment'] = op
            op = {}
            op['name'] = 'Редактировать'
            op['href'] = '#/employeepage/' + str(mst.pk)
            all['more'] = op
            op = {}
            op['href'] = str(mst.pk)
            op['fio'] = mst.fio
            all['edit'] = op

            spisok.append(all)

        return Response({'headers': spisok})







class AddmasterView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio']
        spec = request.data['spec'].split(',')
        try:
            photo = request.data['files']
        except:
            photo=''
        idfirma = request.data['idfirma']
        # filename = 'name.txt'
        # with open(filename, 'wb+') as temp_file:
        #     for chunk in photo.chunks():
        #         temp_file.write(chunk)
       # a = Master(fio=fio, spec)
        mst = Master.objects.create(fio=fio, photo=photo, firma_id=idfirma)

        for sp in spec:
            mst.spec.add(sp)

        return Response({'ok': 1})

class DelemployeeView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        id = request.data['idemp']
        fio = request.data['name']
        ok=1
        Master.objects.filter(id=id).delete()

        return Response({'ok': 1})



#----     Client    ---------------------

class UpdateclientView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio']
        phone = request.data['phone']
        time_begin = request.data['time_begin']
        time_end = request.data['time_end']
        idmaster = request.data['idmaster']
        deltime = request.data['deltime']
        idfirma = request.data['idfirma']

        date_now = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()
        date_to = datetime.datetime.strptime(request._data['date_zapis'], "%Y-%m-%d").date()
        idclient = request.data['idclient']
        #usluga = request.data['usluga']

        # if Client.objects.filter(id=idclient).count() == 0:  #fio=fio, phone=phone
        #     cl = Client(fio=fio, phone=phone)
        #     cl.save()
        # else:
        cl = Client.objects.get(id=idclient, firma_id=idfirma)

        mast = Master.objects.get(id=idmaster, firma_id=idfirma)
        #  Check time master
        result = check_time(mast, date_to, time_begin, time_end, idfirma)
        if result == 1:
            return Response({'ok': False})

        # Test Vacation
        if len(Vacation.objects.filter(master=mast, firma_id=idfirma, datestart__lte=date_to, dateend__gte=date_to))>0:
            return Response({'ok': False})

        # Test Workday
        #now = datetime.datetime.now()
        nomday = date_to.weekday()+1
        if len(Workday.objects.filter(master=mast, firma_id=idfirma, nomday=nomday))==0:
            return Response({'ok': False})

        if Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis=date_to, status__lt=2).count() == 0:
            usluga = Zapis.objects.filter(master=mast, firma_id=idfirma, begin=deltime)[0].usluga.id
            a = Zapis(client=cl, firma_id=idfirma, master=mast, begin=time_begin, end=time_end, datezapis=date_to, usluga_id=usluga)
            a.save()
            deletetime(mast, deltime, date_now, idfirma)
        else:
            return Response({'ok': False})

        return Response({'ok': True})


def deletetime(mast,time_begin,date_srez,idfirma):
    Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis=date_srez).delete()

    return 1



class NewclientView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio'].strip()
        phone = request.data['phone'].strip()
        time_begin = request.data['time_begin'].strip()
        time_end = request.data['time_end'].strip()
        master = request.data['master'].strip()
        spec = request.data['spec']
        idfirma = request.data['idfirma'].strip()

        date_srez = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()

        if Client.objects.filter(fio=fio, firma_id=idfirma, phone=phone).count()==0:
            cl = Client(fio=fio, phone=phone, firma_id=idfirma)
            cl.save()
        else:
            cl = Client.objects.get(fio=fio, firma_id=idfirma, phone=phone)

        mast = Master.objects.get(fio=master, firma_id=idfirma)
        #  Check time master
        result = check_time(mast, date_srez, time_begin, time_end,idfirma)
        if result==1:
            return Response({'ok': False})

        if Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis = date_srez, status__lt=2).count()==0:
            a = Zapis(client=cl, master=mast, firma_id=idfirma, begin=time_begin, end =time_end, datezapis = date_srez, usluga_id=spec)
            a.save()
        else:
            return Response({'ok': False})


        return Response({'ok': True})


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



class ScheduleView(APIView):
    def post(self, request, *args, **kwargs):
        # articles = Master.objects.all()
        idfirma = request.data['idfirma']
        date_to = request.data['date']
        date_srez = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()

        work = Workcalendar.objects.filter(firma_id=idfirma)
        ok = 1
        begin = work[0].start  # work[0].start
        endtime = work[0].end  # work[0].end
        client = Client.objects.all()
        start=int(begin.split(':')[0])
        end = int(endtime.split(':')[0])
        worktime = []
        for i in range(start, end):
            st = str(i) + ':00'
            worktime.append(st)
            st2 = str(i) + ':30'
            worktime.append(st2)
        st = str(i+1) + ':00'
        worktime.append(st)
       # countMaster = Master.objects.filter(firma_id=idfirma).count()
        master = Master.objects.filter(firma_id=idfirma).select_related()
        zapis = []
        i = 0
        for ms in master:
            indiv = []

            df = 1
            vac = ms.vacation_set.filter(dateend__gte=date_srez, datestart__lte=date_srez)
            # --   Workday  --------
            nomday = date_srez.weekday() + 1
            wkday = ms.workday_set.filter(nomday=nomday)
            for w in worktime:
                # if df>0:
                #    df-=2
                #    continue

                desc = {}

                if len(vac) > 0:
                    ok = 1
                    desc['split'] = 1
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 5
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                #     continue
                    # --   Workday  --------
                # nomday = date_srez.weekday() + 1
                # wkday = ms.workday_set.filter( nomday=nomday)
                if len(wkday) == 0:
                    ok = 1
                    desc['split'] = 1
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 4
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                    continue

                has = ms.zapis_set.filter( begin=w, datezapis=date_srez, status__lte=2)
                if has.count() == 0:
                    if df > 1:
                        desc['split'] = -df
                        # df -= 1
                    else:
                        desc['split'] = df
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 0
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                    df -= 1
                    if df == 0:
                        df = 1
                    # i += 1
                    continue
                cl = has[0].client  #Client.objects.get(firma_id=idfirma, pk=has[0].client.id)
                start = has[0].begin
                endclient = has[0].end
                df = int(diferhour(start, endclient) * 2)
                if df == 0:
                    df = 1
                desc['split'] = df
                desc['client'] = cl.fio + ' : ' + cl.phone + ' - ' + has[0].usluga.name
                st = 'time'  # + str(i)
                desc['have'] = 1
                desc['master'] = i
                desc['idclient'] = cl.id
                desc['idmaster'] = ms.id
                desc['status'] = has[0].status
                desc[st] = w
                indiv.append(desc)
                # i += 1
                pass
            zapis.append(indiv)
            i += 1
        ok = 1
        newspisok = []
        # for zp in zapis:
        #    count_row=len(zp)

        count_row = len(worktime)
        count_col = Master.objects.filter(firma_id=idfirma).count()
        for j in range(0, count_row):
            desc = {}
            spis = []
            desc['split'] = -1
            desc['client'] = ''
            desc['have'] = 0
            desc['master'] = 0
            desc['status'] = 0
            desc['idclient'] = ''
            desc['idmaster'] = ms.id
            st = 'time'  # + str(i)
            desc[st] = worktime[j]
            spis.append(desc)
            for i in range(0, count_col):
                ok = 1
                try:
                    spis.append(zapis[i][j])
                except:
                    pass

            newspisok.append(spis)


        #-----------  Master ---------------------------------------------------------
        idfirma = request.data['idfirma']
        # serializer = MasterSerializer(master, many=True)
        mast = Master.objects.filter(firma_id=idfirma)
        spisok = []
        for mst in mast:
            op = {}
            op['fio'] = mst.fio
            op['profession'] = mst.profession
            try:
                op['photo'] = "https://apivisiter.ru" + mst.photo.url  # "
            except:
                op['photo'] = "img/avatars/nobody.jpg"
            spisok.append(op)

        spec_all = Spec.objects.filter(firma_id=idfirma)
        all_spec = []
        for sp in spec_all:
            op2 = {}
            op2['text'] = sp.name
            op2['value'] = sp.id
            all_spec.append(op2)

        # return Response({'headers': spisok, 'specall': all_spec})

        return Response({'zapis': newspisok, 'headers': spisok, 'specall': all_spec})

class ScheduleView2(APIView):
    def post(self, request, *args, **kwargs):
        # articles = Master.objects.all()
        idfirma = request.data['idfirma']
        date_to = request.data['date']
        date_srez = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()

        work = Workcalendar.objects.filter(firma_id=idfirma)
        ok = 1
        begin = work[0].start  # work[0].start
        endtime = work[0].end  # work[0].end
        client = Client.objects.all()
        start=int(begin.split(':')[0])
        end = int(endtime.split(':')[0])
        worktime = []
        for i in range(start, end):
            st = str(i) + ':00'
            worktime.append(st)
            st2 = str(i) + ':30'
            worktime.append(st2)
        st = str(i+1) + ':00'
        worktime.append(st)
       # countMaster = Master.objects.filter(firma_id=idfirma).count()
        master = Master.objects.filter(firma_id=idfirma)
        zapis = []
        i = 0
        for ms in master:
            indiv = []

            df = 1
            for w in worktime:
                # if df>0:
                #    df-=2
                #    continue

                desc = {}

                # --   Vacation  ---------
                vac = Vacation.objects.filter(firma_id=idfirma, master=ms, dateend__gte=date_srez, datestart__lte=date_srez)
                if len(vac) > 0:
                    ok = 1
                    desc['split'] = 1
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 5
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                #     continue


                #--   Workday  --------
                nomday = date_srez.weekday()+1
                wkday= Workday.objects.filter(firma_id=idfirma, master=ms, nomday=nomday)
                if len(wkday)==0:
                    ok=1
                    desc['split'] = 1
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 4
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                    continue


                has = Zapis.objects.filter(firma_id=idfirma, begin=w, master=ms, datezapis = date_srez, status__lte=2)
                if has.count() == 0:
                    if df > 1:
                        desc['split'] = -df
                        #df -= 1
                    else:
                        desc['split'] = df
                    desc['client'] = ''
                    desc['have'] = 0
                    desc['status'] = 0
                    desc['master'] = i
                    desc['idclient'] = ''
                    desc['idmaster'] = ms.id
                    st = 'time'  # + str(i)
                    desc[st] = w
                    indiv.append(desc)
                    df -= 1
                    if df == 0:
                        df=1
                    #i += 1
                    continue
                cl = Client.objects.get(firma_id=idfirma, pk=has[0].client.id)
                start = has[0].begin
                endclient = has[0].end
                df = int(diferhour(start, endclient) * 2)
                if df == 0:
                    df=1
                desc['split'] = df
                desc['client'] = cl.fio + ' : ' + cl.phone+' - '+has[0].usluga.name
                st = 'time'  # + str(i)
                desc['have'] = 1
                desc['master'] = i
                desc['idclient'] = cl.id
                desc['idmaster'] = ms.id
                desc['status'] = has[0].status
                desc[st] = w
                indiv.append(desc)
                #i += 1
                pass
            zapis.append(indiv)
            i += 1

        ok = 1
        newspisok = []
        # for zp in zapis:
        #    count_row=len(zp)

        count_row = len(worktime)
        count_col = Master.objects.filter(firma_id=idfirma).count()
        for j in range(0, count_row):
            desc = {}
            spis = []
            desc['split'] = -1
            desc['client'] = ''
            desc['have'] = 0
            desc['master'] = 0
            desc['status'] = 0
            desc['idclient'] = ''
            desc['idmaster'] = ms.id
            st = 'time'  # + str(i)
            desc[st] = worktime[j]
            spis.append(desc)
            for i in range(0, count_col):
                ok = 1
                try:
                    spis.append(zapis[i][j])
                except:
                    pass

            newspisok.append(spis)

        # serializer = ArticleSerializer(articles, many=True)
        ok = 1
        return Response({'zapis':newspisok})


def diferhour(begin, end):
    s =begin.split(':')
    h1=s[0]
    min1 = s[1]
    s = end.split(':')
    h2 = s[0]
    min2 = s[1]
    dif = int(h2) - int(h1)
    if int(min1) - int(min2) > 0:
        dif = dif+0.5
    elif int(min1) - int(min2) < 0:
        dif = dif+0.5

    ok=1

    return dif


class ChangeStatusView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio'].strip()
        phone = request.data['phone'].strip()
        time_begin = request.data['time_begin'].strip()
        time_end = request.data['time_end'].strip()
        idmaster = request.data['idmaster']
        idclient = request.data['idclient']
        idfirma = request.data['idfirma']

        date_srez = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()

        cl = Client.objects.get(id = idclient, firma_id=idfirma)  #fio=fio, phone=phone

        mast = Master.objects.get(id=idmaster, firma_id=idfirma)

        Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis = date_srez, client=cl).update(status=1)



        return Response({'ok': True})


class DeletezapisView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio'].strip()
        phone = request.data['phone'].strip()
        time_begin = request.data['time_begin'].strip()
        time_end = request.data['time_end'].strip()
        idmaster = request.data['idmaster']
        idfirma = request.data['idfirma']

        date_srez = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()

       # cl = Client.objects.get(fio=fio, phone=phone)

        mast = Master.objects.get(id=idmaster, firma_id=idfirma)

        #Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis = date_srez).update(status=2)  #.delete()
        Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis=date_srez).delete()

        return Response({'ok': True})


class NotComezapisView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        fio = request.data['fio'].strip()
        phone = request.data['phone'].strip()
        time_begin = request.data['time_begin'].strip()
        time_end = request.data['time_end'].strip()
        idmaster = request.data['idmaster']
        idfirma = request.data['idfirma']

        date_srez = datetime.datetime.strptime(request._data['date'], "%Y-%m-%d").date()

       # cl = Client.objects.get(fio=fio, phone=phone)

        mast = Master.objects.get(id=idmaster, firma_id=idfirma)

        #Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis = date_srez).update(status=2)  #.delete()
        Zapis.objects.filter(master=mast, firma_id=idfirma, begin=time_begin, datezapis=date_srez).update(status=2)

        return Response({'ok': True})


class AllSpecView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        spec_all = Spec.objects.filter(firma_id=idfirma)
        all_spec = []
        for sp in spec_all:
            op2 = {}
            op2['text'] = sp.name
            op2['value'] = sp.id
            all_spec.append(op2)

        return Response({'headers': all_spec})


class WorkcalendarPostView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        timestart = request.data['timestart'].strip()
        timeend = request.data['timeend'].strip()
        idfirma = request.data['idfirma']
        timezone = request.data['timezone']
        timeoffset = request.data['timeoffset']
        place = request.data['place']
        adress = request.data['address']
        timezone_text = request.data['timezone']
        if Workcalendar.objects.filter(firma_id=idfirma).count()==0:
            a= Workcalendar(firma_id=idfirma,start=timestart, end=timeend )
            a.save()
        else:
            Workcalendar.objects.filter( firma_id=idfirma).update(start=timestart, end=timeend)


        Firma.objects.filter(id=idfirma).update(timeoffset=timeoffset, timezone = place, adress=adress,timezone_text=timezone_text)

        # user = request.user.userprofile
        # user.timeoffset=timeoffset
        # user.timezone = place
        # user.save()

        return Response({'ok': 1})


class GetWorkcalendarView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        a = Workcalendar.objects.filter(firma_id=idfirma)
        ds={}

        ds['end'] = a[0].end
        ds['start'] = a[0].start



        link = Firma.objects.get(id=idfirma)
        ds['timezone'] = link.timezone_text
        ds['adress'] = link.adress

        if link.booklink == "":
            booklink="http://myvisiter.ru/#/newbooking/"+str(link.id)
            link.booklink=booklink
            link.save()
        else:
            booklink = link.booklink

        return Response({'headers': ds, 'booklink':booklink})


class SmsPostView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        hour = request.data['beforehour']
        beforeday = request.data['before'][0]
        idfirma = request.data['idfirma']
        a = SMS.objects.filter(firma_id=idfirma)
        new=0
        day=0
        if len(a)==0:
            if 'new' in beforeday:
                new = 1
            if 'day' in beforeday:
                day=1
            a =SMS(newclient=new, beforeday=day, beforehour=hour,firma_id=idfirma )
            a.save()
        else:
            if 'new' in beforeday:
                new = 1
            if 'day' in beforeday:
                day=1
            SMS.objects.filter(firma_id=idfirma).update(newclient=new, beforeday=day, beforehour=hour)


        return Response({'ok': 1})



class GetSMSView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        ok=1
        a = SMS.objects.filter(firma_id=idfirma)
        ds={}
        sm=[]
        if a[0].newclient == 1:
            sm.append('new')
            # ds['smsSelected'] = 'new'

        if a[0].beforeday == 1:
            sm.append('day')
            # ds['smsSelected'] = 'day'
        ds['smsSelected']=sm
        ds['beforehour'] = a[0].beforehour

        # b = Workcalendar.objects.all()
        # work={}
        # start = b[0].start
        # end = b[0].end
        # work[]

        return Response({'headers': ds})


#  --------------  ANALITICA         ----------------------------------------

class StatAllView(APIView):
    def post(self, request, *args, **kwargs):
        ok=1
        idfirma = request.data['idfirma']
        ok=1
        #zap = Zapis.objects.all()
        date_begin = datetime.datetime.now() - datetime.timedelta(days=30)
        zap = Zapis.objects.filter(datezapis__gte=date_begin, firma_id=idfirma)
        all_done=0
        all_wait=0
        all_delete=0

        for zp in zap:
            status = zp.status
            if status==1:
                all_done+=1
            if status==0:
                all_wait+=1
            if status==2:
                all_delete+=1

        ds={}
        ds['all_done'] = all_done
        ds['all_wait'] = all_wait
        ds['all_delete'] = all_delete

        return Response({'headers': ds})


class ClientCountView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        ok=1
        date_begin = datetime.datetime.now() - datetime.timedelta(days=30)
        zap = Zapis.objects.filter(datezapis__gte=date_begin, firma_id=idfirma).order_by('datezapis')      # Zapis.objects.all().order_by('datezapis')
        count_day_wait = {}
        count_day_done = {}
        count_day_delete = {}
        # for i in range(1, 7):
        #     count_month_notdone[i] = 0
        labels=[]

        for rq in zap:
            ok = 1
            day = rq.datezapis.strftime('%d-%m-%Y')
            if day not in labels:
                labels.append(day)


            # try:
            #     count_day[day] += 1
            # except:
            #     count_day[day] = 1
            #     count_day[day] = 0
            #     count_day[day] = 0

            if rq.status == 1:
                try:
                    count_day_done[day] += 1
                except:
                    count_day_done[day] = 1
            if rq.status == 0:
                try:
                    count_day_wait[day] += 1
                except:
                    count_day_wait[day] = 1
            if rq.status == 2:
                try:
                    count_day_delete[day] += 1
                except:
                    count_day_delete[day] = 1

        delm=[]
        wait=[]
        done=[]
        max=0
        for dt in labels:
            try:
                dl=count_day_delete[dt]
                delm.append(count_day_delete[dt])
                if dl> max:
                    max=dl
            except:
                delm.append(0)
                pass
            try:
                dl=count_day_wait[dt]
                wait.append(count_day_wait[dt])
                if dl> max:
                    max=dl
            except:
                wait.append(0)
                pass
            try:
                dl=count_day_done[dt]
                done.append(count_day_done[dt])
                if dl> max:
                    max=dl
            except:
                done.append(0)
                pass




        return Response({'labels': labels, 'delete':delm, 'wait':wait, 'done':done, 'max':max+3})


class UslugiChartView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        ok=1
        spec = Spec.objects.filter(firma_id=idfirma)
        spec_all=[]
        spis_uslug={}
        for i in spec:
            spec_all.append(i.name)
            spis_uslug[i.name]=0

        date_begin = datetime.datetime.now() - datetime.timedelta(days=30)
        zap = Zapis.objects.filter(datezapis__gte=date_begin,firma_id=idfirma)
        all_done=0
        all_wait=0
        all_delete=0

        for zp in zap:
            try:
                usluga = zp.usluga.name
                spis_uslug[usluga]+=1
            except:
                pass

        spis=[]
        for key, item in spis_uslug.items():
            spis.append(item)


        return Response({'data': spis, 'labels':spec_all})

class MasterChartView(APIView):
    def post(self, request, *args, **kwargs):
        ok = 1
        idfirma = request.data['idfirma']
        ok=1
        mast = Master.objects.filter(firma_id=idfirma)
        mast_all=[]
        spis_mast={}
        for i in mast:
            mast_all.append(i.fio)
            spis_mast[i.fio]=0

        date_begin = datetime.datetime.now() - datetime.timedelta(days=30)
        zap = Zapis.objects.filter(datezapis__gte=date_begin,firma_id=idfirma)


        for zp in zap:
            if zp.status<2:
                usluga = zp.master.fio
                spis_mast[usluga]+=1

        spis=[]
        for key, item in spis_mast.items():
            spis.append(item)


        return Response({'data': spis, 'labels':mast_all})

#--------------------------------------------------------------------

class CompanyAllView(APIView):
    def post(self, request, *args, **kwargs):

        company = Firma.objects.all()
        spis = []
        for mst in company:
            all = {}

            op = {}
            op['label'] = mst.name
            all['user'] = op
            op = {}

            op['label'] =  mst.adress
            all['usage'] = op

            op = {}
            op['label'] = str(mst.date.day)+'/'+str(mst.date.month)+'/'+str(mst.date.year)
            all['regtime'] = op
            op = {}
            op['label'] = 'Редактировать'
            op['url'] = '/companypage/' + str(mst.id)
            all['more'] = op

            op = {}
            op['label'] =''
            op['url'] = '/companypage/'+str(mst.id)
            all['edit'] = op

            spis.append(all)

        return Response({'company': spis})



class GetCompanyView(APIView):
    def post(self, request, *args, **kwargs):

        idcompany = request.data['id']

        company = Firma.objects.get(id=idcompany)
        spis = []

        all = {}
        all['name'] = company.name
        all['adress'] = company.adress

        return Response({'company': all})


class SaveCompanyView(APIView):
    def post(self, request, *args, **kwargs):

        idcompany = request.data['id']
        name = request.data['name']
        adress = request.data['adress']

        company = Firma.objects.filter(id=idcompany).update(name=name, adress = adress)

        return Response({'ok': 1})


class AddCompanyView(APIView):
    def post(self, request, *args, **kwargs):
        namecompany = request.data['namecompany']
        adress = request.data['adress']

        a = Firma(name=namecompany, adress=adress)
        a.save()

        return Response({'ok': 1})


#---------------- Users -------------------------------------



class UsersAllView(APIView):
    def post(self, request, *args, **kwargs):

        company = User.objects.all()
        spis = []
        for mst in company:
            all = {}

            op = {}
            try:
                op['label'] = mst.userprofile.fio   #.first_name+' '+mst.last_name
            except:
                op['label'] =''
            all['user'] = op

            op = {}
            try:
                op['label'] = mst.userprofile.firma.name
            except:
                op['label'] = ''
            all['usage'] = op

            op = {}
            try:
                op['label'] = mst.userprofile.firma.adress
            except:
                op['label'] = ''
            all['payment'] = op

            op = {}
            try:
                op['label'] = mst.username
            except:
                op['label'] = ''
            all['login'] = op

            op = {}
            op['label'] = 'Редактировать'
            op['url'] = '/userpage/' + str(mst.id)
            all['more'] = op

            op = {}
            op['label'] =''
            op['url'] = '/userpage/'+str(mst.id)
            all['edit'] = op

            spis.append(all)

            company = Firma.objects.all()
            prob = []
            for mst in company:
                op = {}
                op['text'] = mst.name
                op['value'] = mst.id
                prob.append(op)




        return Response({'users': spis, 'company':prob})


class GetUserView(APIView):
    def post(self, request, *args, **kwargs):

        iduser = request.data['id']

        user = User.objects.get(id=iduser)
        spis = []

        all = {}
        all['login'] = user.username
        try:
            all['fio'] = user.userprofile.fio
            all['idcompany'] =user.userprofile.firma.id
            all['phone'] = user.userprofile.phone

            all['password'] = user.userprofile.password
            all['email'] = user.userprofile.email
        except:
            all['fio'] = ''
            all['idcompany'] = ''
            all['phone'] = ''

            all['password'] = ''
            all['email'] = ''

        company = Firma.objects.all()
        spis = []
        for mst in company:
            op = {}
            op['text'] = mst.name
            op['value'] = mst.id
            spis.append(op)

        return Response({'user': all, 'company':spis})



class SaveUserView(APIView):
    def post(self, request, *args, **kwargs):

        iduser = request.data['iduser']
        fio = request.data['fio']
        idcompany = request.data['idcompany']
        phone = request.data['phone']
        login = request.data['login']
        password = request.data['password']
        email = request.data['email']

        rq = User.objects.get(id=iduser)
        rq.set_password(password)
        rq.is_staff = True
        rq.email = email
        rq.username = login
        rq.save()

        firm = Firma.objects.get(id=idcompany)
        if Firma.objects.filter(userprofile__user_id=iduser).count()==0:
            ok=1



        prof = UserProfile.objects.get(user_id=iduser)
        prof.firma = firm
        prof.phone = phone
        prof.fio = fio
        prof.email = email
        prof.password = password
        prof.save()

        return Response({'ok': 1})


class AddUserView(APIView):
    def post(self, request, *args, **kwargs):

        fio = request.data['fio']
        idcompany = request.data['idcompany']
        phone = request.data['phone']
        login = request.data['login']
        password = request.data['password']
        email = request.data['email']

        rq = User.objects.create_user(login, email, password)
        # rq = User.objects.get(id=iduser)
        # rq.set_password(password)
        rq.is_staff = True
        # rq.email = email
        # rq.username = login
        rq.save()
        iduser = rq.id

        firm = Firma.objects.get(id=idcompany)
        # if Firma.objects.filter(userprofile__user_id=iduser).count()==0:
        #     ok=1
        #     firm.user.add(rq)



        a = UserProfile(user=rq, firma=firm, phone=phone, fio=fio, email=email, password=password)
        a.save()
        # prof.firma = firm
        # prof.phone = phone
        # prof.fio = fio
        # prof.email = email
        # prof.password = password
        # prof.save()

        return Response({'ok': 1})


class LoadfirmView(APIView):
    def post(self, request, *args, **kwargs):
        idfirm = request.data['idfirma']
        ok=1

        firm = Firma.objects.all()
        spisok=[]
        for f in firm:
            ok=1
            op={}
            op['name']=UserProfile.objects.filter(firma_id=f.id)[0].fio
            op['id'] = f.id
            op['company'] = f.name
            op['tel'] = UserProfile.objects.filter(firma_id=f.id)[0].phone
            op['email'] = UserProfile.objects.filter(firma_id=f.id)[0].email
            try:
                op['tarifftime'] = (f.datetarif - datetime.datetime.now().date()).days
            except:
                op['tarifftime'] = 0
            op['sms'] = f.balans
            # op['balans'] = f.balans
            op['url'] = '/payment/'+str(f.id)
            spisok.append(op)

        return Response({'company': spisok})



class LoadpaymentsView(APIView):
    def post(self, request, *args, **kwargs):
        idcompany = request.data['idfirma']
        ok=1
        name=Firma.objects.get(id=idcompany).name
        pay = Accounting.objects.filter(firma_id=idcompany).order_by('-date')
        spisok=[]
        for f in pay:
            ok=1
            op={}
            item={}
            item['label']=str(f.date.day)+'/'+str(f.date.month)+'/'+str(f.date.year)
            op['user']=item
            item = {}
            item['label'] = f.type
            op['usage'] = item
            item = {}
            item['label'] = f.quantity
            op['payment'] = item
            item = {}
            item['label'] = f.summa
            op['login'] = item
            item = {}
            item['label'] ='/editpay/'+str(f.id)
            op['url'] = item
            spisok.append(op)

        return Response({'payments': spisok , 'name':name})


class AddpaymentsView(APIView):
    def post(self, request, *args, **kwargs):
        idcompany = request.data['idfirma']
        selectedTime = request.data['selectedTime']
        tarifsum = request.data['tarifsum']
        ok=1
        a = Accounting(firma_id=idcompany, type="За тариф", quantity=selectedTime, summa=tarifsum)
        a.save()
        delta = 30*selectedTime
        enddate = datetime.datetime.now()+ datetime.timedelta(days=delta)
        firm = Firma.objects.filter(id=idcompany).update(datetarif=enddate)



        return Response({'ok': 1})


class AddSMSView(APIView):
    def post(self, request, *args, **kwargs):
        idcompany = request.data['idfirma']
        selectedSMS = 0     #request.data['selectedSMS']
        tarifsms = request.data['tarifsms']
        ok=1
        a = Accounting(firma_id=idcompany, type="За СМС", quantity=selectedSMS, summa=tarifsms)
        a.save()
        firm = Firma.objects.get(id=idcompany)
        sms = firm.smslast+int(selectedSMS)
        balans = firm.balans+int(tarifsms)
        Firma.objects.filter(id=idcompany).update(datesms=datetime.datetime.now(), smslast=sms, balans=balans)

        return Response({'ok': 1})


class GetStatusFirmView(APIView):
    def post(self, request, *args, **kwargs):
        idcompany = request.data['idfirma']

        firm = Firma.objects.get(id=idcompany)
        tarif = (firm.datetarif - datetime.datetime.now().date()).days
        sms = firm.smslast
        balans = firm.balans

        return Response({'tarif': tarif, 'sms':sms ,'balans':balans})


class LogsView(APIView):
    def post(self, request, *args, **kwargs):
        idcompany = request.data['idfirma']

        spisok = []
        i = 1
        acc = Accounting.objects.filter(firma_id=idcompany)#.order_by('-date')
        balans=0
        acc_list=[]
        for ac in acc:
            po={}
            if  'За СМС' in ac.type:
                dat = str(ac.date.day) + '-' + str(ac.date.month) + '-' + str(ac.date.year)
                po['date']=dat
                po['summa']=ac.summa

                acc_list.append(po)

                #break




        log = Log.objects.filter(firma_id=idcompany)    #.order_by('-date')

        for lg in log:
            dat=str(lg.date.day) + '-' + str(lg.date.month) + '-' + str(lg.date.year)
            for ac in acc_list:
                ok=1
                if ac['date']<=dat:
                    op = {}
                    op['number'] = i
                    i += 1
                    op['date'] = ac['date']       #str(ac.date.day) + '-' + str(ac.date.month) + '-' + str(ac.date.year)
                    op['type'] = 'Пополнение баланса СМС общая сумма'
                    op['tel'] = ''
                    price = 0
                    op['price'] = str(ac['summa']) + ' р'
                    op['balance'] = ac['summa']
                    balans += ac['summa']
                    spisok.append(op)
                    acc_list.remove(ac)

            op={}
            op['number']=i
            i+=1
            op['date'] = str(lg.date.day)+'-'+str(lg.date.month)+'-'+str(lg.date.year)
            op['type'] = lg.type
            op['tel'] = lg.thewho
            price=0
            if lg.sms==0:
                price=0.5
            else:
                price=2.7
            op['price'] = str(price)+' тг'
            balans=balans-price
            op['balance'] = balans
            spisok.append(op)

        if balans<0:
            balans=0
        firm = Firma.objects.filter(id=idcompany).update(balans=balans)

        spisok.reverse()

        return Response({'logs': spisok})


def SendTelegrammEvent(text, body):
    cont = "425750182"
    text_email = 'Оплата {0}  -  {1} '.format(text, body)
    urlsms = "https://api.telegram.org/bot874312188:AAF4sZqc1rzs49qA5TfyY_hWE-_uN8eURaA/sendMessage?chat_id={0}&text={1}".format(
        cont, text_email)
    response = requests.post(urlsms, headers={'Content-Type': 'application/xml; charset=UTF-8'})
    cont = "407110866"
    ttext_email = 'Оплата {0}  -  {1} '.format(text, body)
    urlsms = "https://api.telegram.org/bot874312188:AAF4sZqc1rzs49qA5TfyY_hWE-_uN8eURaA/sendMessage?chat_id={0}&text={1}".format(
        cont, text_email)
    response = requests.post(urlsms, headers={'Content-Type': 'application/xml; charset=UTF-8'})



class YandexView(APIView):
    def post(self, request, *args, **kwargs):
        sum = request.data['sum']
        text = request.data['text']
        namefirma = request.user.userprofile.firma.name
        body=namefirma+ '  '+text
        print(text, sum)
        #sum=50

        try:
            SendTelegrammEvent(sum, body)
        except:
            pass

        # Configuration.account_id =  '612617'
        # Configuration.secret_key = 'test_Tf9Xc4H74obqKqLIuf58g2RrF7wsVGNR1K-uz24n9GE'

        Configuration.account_id =  '672600'
        Configuration.secret_key = 'live_1N41MlGRbgxfGyIgKPqq-Sqd27gqiSTPRLeGNWatHXo'


        payment = Payment.create({
            "amount": {
                "value": sum,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://apivisiter.ru/api/yandexsucess",
                "confirmation_url": "https://apivisiter.ru/api/yandexsucess"
            },
            "capture": True,
            "description": text,
            "metadata": {
                "order_id": "37"
            }
        })

        ok=1

        return Response({'yandex': payment.confirmation.confirmation_url})


@permission_classes((AllowAny,))
class YandexsuccessView(APIView):
    def get(self, request):
        #sum = request.data['sum']
        print('request.GET  YandexsuccessView')
        print(request.POST)

        print(request.GET)
        ok=1

        return redirect("https://myvisiter.ru")

    def post(self, request, *args, **kwargs):
        ok=1
        print('request.post  YandexsuccessView')
        print(request.POST)

        print(request.data)

        return redirect("https://myvisiter.ru")

@permission_classes((AllowAny,))
class YandexcheckView(APIView):
    def get(self, request):
        #sum = request.data['sum']
        ok=1
        print('request.GET YandexcheckView')
        print(request.GET)

        return redirect("http://myvisiter.r")

    def post(self, request, *args, **kwargs):
        ok=1

        return redirect("http://myvisiter.r")

@permission_classes((AllowAny,))
class YandexavisoView(APIView):
    def get(self, request):
        #sum = request.data['sum']
        ok=1

        return redirect("http://myvisiter.r")

    def post(self, request, *args, **kwargs):
        ok=1

        return redirect("http://myvisiter.r")

@permission_classes((AllowAny,))
class YandexfailView(APIView):
    def get(self, request):
        #sum = request.data['sum']
        ok=1

        return redirect("http://myvisiter.r")

    def post(self, request, *args, **kwargs):
        ok=1

        return redirect("http://myvisiter.r")


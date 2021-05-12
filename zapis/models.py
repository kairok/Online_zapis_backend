from django.db import models

# Create your models here.

from django.contrib.auth.models import User
# Create your models here.


class Firma(models.Model):
    name = models.CharField(max_length=100)
    user = models.ManyToManyField(User)
    tarif = models.PositiveIntegerField(default=0)
    datetarif=models.DateField(blank=True, null=True)
    smslast = models.PositiveIntegerField(default=0)
    balans = models.PositiveIntegerField(default=0)
    datesms = models.DateField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    adress = models.CharField(max_length=100, blank=True)
    booklink= models.CharField(max_length=100, blank=True)
    timeoffset = models.PositiveIntegerField(default=0)
    timezone = models.CharField(max_length=50, default='')
    timezone_text = models.CharField(max_length=50, default='')

    def __str__(self):
        return 'Firma'.format(self.name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=100)
    role = models.PositiveIntegerField(default=1)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    password = models.CharField(max_length=30)
    timeoffset = models.PositiveIntegerField(default=0)
    timezone = models.CharField(max_length=30, default='')
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'UserProfile'.format(self.user)

class Client(models.Model):
    fio = models.CharField(max_length=100)
    phone  = models.CharField(max_length=20)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Client'.format(self.fio)
    class Meta:
        # db_table = 'Zapis'
        indexes = (
            models.Index(fields=['firma', 'id']),

        )


class Master(models.Model):
    fio = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='photo/',null=True, blank=True,  verbose_name='Ваше изображение')
    #photo = models.ImageField(upload_to='photo/',blank=False, null=False)
    spec = models.ManyToManyField('Spec')
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)
    #file = models.FileField(blank=False, null=False)
    #phone  = models.CharField(max_length=20)

    def __str__(self):
        return 'Master'.format(self.fio)
    class Meta:
        # db_table = 'Zapis'
        indexes = (
            models.Index(fields=['firma']),
            models.Index(fields=['firma', 'id']),

        )

class Spec(models.Model):
    name = models.CharField(max_length=100)
    time = models.CharField(max_length=10, default='1 час')
    price = models.PositiveIntegerField(default=0)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Spec'.format(self.name)

class Workcalendar(models.Model):
    start = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Workcalendar'.format(self.start)
    class Meta:
        # db_table = 'Zapis'
        indexes = (
            models.Index(fields=['firma']),

        )


class Zapis(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    begin = models.CharField(max_length=5)
    end = models.CharField(max_length=5)
    datezapis = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=0)
    usluga = models.ForeignKey(Spec, on_delete=models.DO_NOTHING)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)


    def __str__(self):
        return 'Zapis'.format(self.client)

    class Meta:
        # db_table = 'Zapis'
        indexes = (
            models.Index(fields=['firma', 'begin', 'master','datezapis','status']),
            models.Index(fields=['firma', 'datezapis']),
        )

class Workday(models.Model):
    master = models.ForeignKey('Master', on_delete=models.CASCADE)
    nomday = models.IntegerField()
    nameday = models.CharField(max_length=10)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Workday'.format(self.master)
    class Meta:
        # db_table = 'Zapis'
        indexes = (
            models.Index(fields=['firma','master','nomday']),

        )


class Vacation(models.Model):
    master = models.ForeignKey('Master', on_delete=models.CASCADE)
    datestart = models.DateField(null=True, blank=True)
    dateend = models.DateField(null=True, blank=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Vacation'.format(self.master)

#   Send SMS
class SMS(models.Model):
    newclient = models.BooleanField(default=0)
    beforeday = models.BooleanField(default=0)
    beforehour = models.PositiveIntegerField(default=0)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'SMS'.format(self.newclient)


#   Accounting
class Accounting(models.Model):
    quantity= models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=100)
    summa = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'SMS'.format(self.newclient)


#   Log
class Log(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    thewho = models.CharField(max_length=100)
    whatsap = models.PositiveIntegerField(default=0)
    sms = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    firma = models.ForeignKey('Firma', on_delete=models.CASCADE)

    def __str__(self):
        return 'Log'.format(self.type)

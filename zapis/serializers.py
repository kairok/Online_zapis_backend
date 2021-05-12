from rest_framework import serializers




class MasterSerializer(serializers.Serializer):
    fio = serializers.CharField(max_length=120)
    profession = serializers.CharField()
    photo = serializers.CharField()
    #body = serializers.CharField()
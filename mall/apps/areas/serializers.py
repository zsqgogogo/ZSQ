from rest_framework import serializers
from areas.models import Area



#
# class ProvienceSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model=Area
#         fields=['id','name']
#
#
# class DistrictSerializer(serializers.ModelSerializer):
#     abc = ProvienceSerializer(read_only=True,many=True)
#     class Meta:
#         model=Area
#         fields=['id','name','abc']



class ProvienceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Area
        fields=['id','name']



class DistrictSerializer(serializers.ModelSerializer):
    subs=ProvienceSerializer(read_only=True, many=True)
    class Meta:
        model=Area
        fields=['id','name','subs']




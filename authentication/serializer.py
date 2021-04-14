from rest_framework.serializers import ModelSerializer
from authentication.models import User
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=("id","username","email","password")
        # for hiding password to be serialize in postman
        extra_kwargs={
            'password': {'write_only':True}
        }
    # for saving password in hash form
    def create(self,validated_data):
        password=validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None :
            instance.set_password(password)
        instance.save()
        return instance

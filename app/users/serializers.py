from rest_framework import serializers
from .models import User, WorkStatics
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'phone_number',
            'user_roles',
            'image',
            'password',
            'salary_worker'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'image': {'required': False},
            'salary_worker': {'required': False}
        }

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        username = data.get('username')

        if username and User.objects.filter(username=username).exists():
            raise ValidationError({'username': 'Username already exists'})
    
        return data


class LoginSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password'
        ]


class WorkStaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkStatics
        fields = ['id', 'worker', 'qty', 'price', 'name', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    worker_static = WorkStaticSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'first_name', 'last_name', 'image', 'user_roles', 'created_at'
                  , 'filial_name', 'password', 'worker_static', 'monthly_earnings', 'salary_worker')
        extra_kwargs = {
            'filial_name': {'required': False},
            'worker_static': {'required': False},
            'image': {'required': False},
        }

        def create(self, validated_data):
            worker_static_data = validated_data.pop('worker_static', [])
            user = User.objects.create_user(**validated_data)
            for work_static in worker_static_data:
                WorkStatics.objects.create(worker=user, **work_static)

            return user


class WorkStaticGetSerializer(serializers.ModelSerializer):
    worker = UserSerializer()
    class Meta:
        model = WorkStatics
        fields = ['id', 'worker', 'qty', 'price', 'name', 'created_at']
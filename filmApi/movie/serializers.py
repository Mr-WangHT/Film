"""
author:Wenquan Yang
time:2020/4/21 22:16
"""
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from movie.models import *
from rest_framework import exceptions


def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # 数据表中的所有字段


class RegSerializers(serializers.ModelSerializer):
    pwd2 = serializers.CharField(max_length=32, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'pwd2')

    def validate(self, attrs):
        if attrs['pwd2'] != attrs['password']:
            raise exceptions.ValidationError('两次输入的密码不一致')
        del attrs['pwd2']
        attrs['password'] = make_password(attrs['password'])
        return attrs


class LogSerializers(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        user_obj = User.objects.filter(username=attrs['username']).first()
        if user_obj:
            if check_password(attrs['password'], user_obj.password):
                token = md5(user_obj.username)
                UserToken.objects.update_or_create(
                    username=user_obj,
                    defaults={
                        'token': token
                    }
                )
                attrs['token'] = token
                del attrs['password']
                return attrs
        raise exceptions.ValidationError('用户名或密码错误')


class CommentSerializers(serializers.ModelSerializer):
    token = serializers.CharField(max_length=60)

    class Meta:
        model = Comment
        fields = ('movie_id', 'user_score', 'comment_content', 'token')
        token = models.CharField(max_length=60)

    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) + list(kwargs.items())
        )
        del validated_data['token']
        self.instance = self.create(validated_data)
        return self.instance


class OrderSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=60)

    class Meta:
        model = Order
        fields = ('schedule_id', 'token', 'order_seat_info', 'pay_type')

    # 用户购买电影票
    def save(self, **kwargs):
        pass

    # 用户删除订单

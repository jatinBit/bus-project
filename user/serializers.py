from rest_framework import serializers
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from . models import *
from . utils import Util
from rest_framework.exceptions import ValidationError
# for send reset password link to email
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 

import re

def validCollegeId(num):
    if(len(num)!=5): 
        return False 
    for i in num:
           if not i.isdigit():
                return False
    return True

def validPhoneNo(num):
    if(len(num)!=10): 
        return False 
    for i in num:
           if not i.isdigit():
                return False
    return True

def check_email_domain(email):
    allowed_domain=r"@bitmesra\.ac\.in$"
    """
    'r':  This denotes a raw string literal in Python. 
          It's used to specify that backslashes within the string should be treated as literal characters rather than escape characters.

    '\.': Matches the dot character "." literally. 
          The backslash \ is used to escape the dot, indicating that it should be treated as a literal dot.
    '$':  This anchors the pattern to the end of the string. 
          It ensures that the pattern matches only when the domain @abc.ac.in is at the end of the string. 
          This prevents partial matches where the domain appears somewhere within the string but not at the end.
    """
    if re.search(allowed_domain, email):
        return True
    else:
        return False

class UserSerializer(serializers.ModelSerializer):
    # we are writing this because we need confrim password field in our registration request
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password=attrs['password']
        password2=attrs['password2']
        if(password!=password2):
            raise serializers.ValidationError({'password':"password and confrim password doesn't match"})
        if(not check_email_domain(attrs['email'])):
            raise serializers.ValidationError({'email':"Email is not valid, Email domain must end with @bitmesra.ac.in"})
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'  

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'  
    
    
    def validate(self, attrs):
        print(attrs)
        collegeId=attrs.get('collegeId')
        if collegeId is not None:

            if(not validCollegeId(collegeId)):
                raise ValidationError('enter a valid college Id.')
        phone=attrs.get('phone_no')
        if phone is not None:
            if(not validPhoneNo(phone)):
                raise ValidationError('enter a valid phone no.')
        return attrs
    def to_representation(self, instance):
        
        base_url=settings.BASE_URL
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user).data
        response["image"]=base_url+"user"+response['image']
        return response

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if(password!=password2):
            raise serializers.ValidationError({'passwordError':"password and confrim password doesn't match"})
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password reset Token',token)
            link='http://localhost:3000/user/reset/'+uid+'/'+token
            print('password reset link',link)
            # send Email
            body='Click Following Link to Reset Your Password '+link
            data={
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError({'emailError':"Email is not valid"})
        return attrs

class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password','password2']
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if(password!=password2):
                raise serializers.ValidationError({'passwordError':"password and confrim password doesn't match"})
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as  identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not Valid or Expired')

      
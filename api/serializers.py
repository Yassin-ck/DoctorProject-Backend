from rest_framework import serializers
from .models import User,Doctor
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    is_doctor = serializers.BooleanField(default=False,required=False)
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password','password2','is_doctor']

    
        def validate(self,data):
            password = data.get('password')
            password2 = data.get('password2')
            if password != password2:
                raise serializers.ValidationError('Password Does Not Match')
            return data




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['is_doctor'] = user.is_doctor
        return token
    

class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Doctor
        fields = ['id','hospital','department','user']
        read_only_fields = ('user',)

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = args[0]
        if  users.is_doctor:
            self.fields['doctor'] = DoctorSerializer()
  

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)

        if instance.is_doctor:
            doctor_data = validated_data.get('doctor')
            if doctor_data:
                doctors = Doctor.objects.filter(user=instance)
                if doctors.exists():
                    doctor = doctors.first()  
                    doctor.hospital = doctor_data.get('hospital', doctor.hospital)
                    doctor.department = doctor_data.get('department', doctor.department)
                    doctor.save()
                else:
                    raise ValidationError("No doctor record found for this user.")

        instance.save() 
        return instance
            
            

class UserProfileAdminSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)   
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name','username', 'email','is_active','doctor')

 
    def update(self,instance,validated_data):
        instance.is_active = validated_data.get('is_active',instance.is_active)
        instance.save()
        return instance
    

class UserLogoutSerializer(serializers.Serializer):
    refresh  = serializers.CharField()
    
    default_error_messages ={
        'bad_token':('Token is Expired')
    }
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self,*args,**kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_Token')
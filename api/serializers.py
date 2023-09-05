from rest_framework import serializers
from .models import User,Doctor


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



class UserLoginSerilizer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email','password']
        

class DoctorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Doctor
        fields = ['hospital','department','user']
        read_only_fields = ('user',)

class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = args[0]
        if user.is_doctor:
            self.fields['doctor'] = DoctorSerializer()

    def update(self, instance, validated_data):
        print('iii',instance)
       
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
       
        if instance.is_doctor:
            doctors = Doctor.objects.get(user=instance)
            doctor_value = list(validated_data.get('doctor').values()) 
            doctors.hospital = doctor_value[0]
            doctors.department = doctor_value[1]
            doctors.save()
        instance.save()
        return instance
            
            

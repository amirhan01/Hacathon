from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordCompleteSerializer
from rest_framework.permissions import IsAuthenticated



User = get_user_model()

'''Функция регистрации'''
class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        serializers = RegisterSerializer(data=data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            massage = f'Успешная регистрация!. Письмо отправленно Вам на почту.'
            return Response(massage, status=201)


'''Функция для активации аккаунта'''
class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'Ваш аккаунт был активирован'}, status=200)
        except User.DoesNotExist:
            return Response({'msg': 'Неверный код!'}, status=400)


'''Фукция для смены пароля'''
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = ChangePasswordSerializer(data=request.data,
                                               context={'request': request})
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response('Пароль успешно обнавлен!')


'''Функция для востановления пароля по почте'''
class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам отправлено письмо для восстановления пароля')


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_pass()
        return Response('Паротль был успешно изменен!')




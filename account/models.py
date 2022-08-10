from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Кастомный пользователь
class UserManager(BaseUserManager):

    # Защищенный метод для создания пользователя
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    # Метод для создания пользователя
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # Метод для создания админа
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# Параметры для пользователя
class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=100)
    activation_code = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    username = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # Метод для создания активационного кода
    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code

    # Метод создания кода для ForgotPassword
    def code_generation(self):
        import random
        from string import ascii_letters, digits
        symb = ascii_letters + digits
        secure_random = random.SystemRandom()
        code = ''.join(secure_random.choice(symb) for i in range(8))
        self.activation_code = code



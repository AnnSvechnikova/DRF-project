# при создании собственной модели пользователя надо переопределить методы менеджера пользователей по умолчанию
from django.contrib.auth.base_user import BaseUserManager

# full_name, is_staff - extra fields


class UserManager(BaseUserManager):

    def _create_user(self, username, full_name, password=None, **extra_fields):
        if not username:
            raise ValueError('Нужно установить ник пользователя')
        if not full_name:
            raise ValueError('Нужно установить фамилию и имя пользователя')
        user = self.model(username=username, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, full_name, password, **extra_fields)

    def create_staff(self, username, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Менеджер должен иметь is_staff=True.')
        return self._create_user(username, full_name, password, **extra_fields)

    def create_superuser(self, username, full_name,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Администратор должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Администратор должен иметь is_superuser=True.')
        return self._create_user(username, full_name, password, **extra_fields)
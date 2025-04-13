from django.db.models import CharField, IntegerField, EmailField, TextField, BooleanField, DateTimeField
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator




class MiManejadorUsuario(BaseUserManager):
    """Este indicará como crear al usuario y superusuario."""

    def create_user(self, correo, usuario, password, **other_fields):

        # Validación
        if not correo:
            raise ValueError("El usuario debe tener un correo electornico.")
        if not usuario:
            raise ValueError("El usuario debe tener un nombre de usuario.")
        if not password:
            raise ValueError("El usuario debe tener una contraseña/password.")

        # Creo el usuario
        user = self.model(correo=self.normalize_email(correo), usuario=usuario, **other_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, correo, usuario, password, **other_fields):

        # Validación
        if not correo:
            raise ValueError("El usuario debe tener un correo electornico.")
        if not usuario:
            raise ValueError("El usuario debe tener un nombre de usuario.")
        if not password:
            raise ValueError("El usuario debe tener una contraseña/password.")
        
        # Creo el superusuario
        superuser = self.create_user(correo=self.normalize_email(correo), usuario=usuario, password=password, **other_fields)
        superuser.is_staff = True
        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.set_password(password)
        superuser.save()
        return superuser



class Usuario(AbstractBaseUser, PermissionsMixin):
    """Este usuario creara los cosiacos y las opiniones."""

    # Campos requeridos
    correo = EmailField(verbose_name="correo electrónico", max_length=100, unique=True)
    usuario = CharField(verbose_name="usuario", max_length=100, unique=True)
    date_joined = DateTimeField(verbose_name="fecha de registro", auto_now=True)
    last_login = DateTimeField(verbose_name="ultimo accesso", auto_now_add=True)
    is_active = BooleanField(verbose_name="esta activo", default=True)
    is_staff = BooleanField(verbose_name="es staff", default=False)
    is_admin = BooleanField(verbose_name="es admin", default=False)
    is_superuser = BooleanField(verbose_name="es superusuario", default=False)

    # Campos opcionales
    bio = TextField(verbose_name="bio", max_length=500, null=True, blank=True)
    celular = IntegerField(verbose_name="celular", validators=[MaxValueValidator], unique=True, blank=True, null=True)

    # Campo para hacer login
    USERNAME_FIELD = "correo"

    # Campos obligatorias para creación del usuario
    REQUIRED_FIELDS = [
        "usuario"
    ]

    # Paso el manejador de usuarios
    objects = MiManejadorUsuario()

    def __str__(self):
        return self.usuario
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True




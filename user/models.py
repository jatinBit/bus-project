from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import os

# custom user model imports
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

# custom user manager

class UserManager(BaseUserManager):
    def create_user(self, email, name, tc , password=None, password2=None):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc , password=None):
        """
        Creates and saves a superuser with the given email, name, tc and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# custom user model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email",
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    name=models.CharField(max_length=200)
    tc=models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name",'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

@receiver(post_save, sender=User)
def watchlist_create(sender, instance=None, created=False, **kwargs):
    if created:
        Profile.objects.create(user=instance,)

def get_upload_path(instance,filename):
    return os.path.join('images','profile_pic',str(instance.pk),filename)

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    image=models.ImageField(upload_to=get_upload_path,default='default.png')
    phone_no=models.CharField(max_length=10,unique=True,null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    DEPARTMENT_CHOICES=(
        ('Architecture and Planning','Architecture and Planning'),
        ('Bioengineering and Biotechnology','Bioengineering and Biotechnology'),
        ('Chemical Engineering','Chemical Engineering'),
        ('Center for Food Engineering and Technology','Center for Food Engineering and Technology'),
        ('Chemistry','Chemistry'),
        ('Civil and Env Engineering','Civil and Env Engineering'),
        ('Computer Science and Engg','Computer Science and Engg'),
        ('Centre for Quantitative Economics and Data Science','Centre for Quantitative Economics and Data Science'),
        ('Electrical and Electronics Engg','Electrical and Electronics Engg'),
        ('Electronics and Communication Engg','Electronics and Communication Engg'),
        ('Hotel Management and Catering Tech','Hotel Management and Catering Tech'),
        ('Humanities and Social Science','Humanities and Social Science'),
        ('Management','Management'),
        ('Mathematics','Mathematics'),
        ('Mechanical Engineering','Mechanical Engineering'),
        ('Pharmaceutical Sciences and Tech','Pharmaceutical Sciences and Tech'),
        ('Physics','Physics'),
        ('Production and Industrial Engineering','Production and Industrial Engineering'),
        ('Remote Sensing','Remote Sensing'),
        ('Space Engineering and Rocketry','Space Engineering and Rocketry'),
    )
    department=models.CharField(max_length=150,null=True,blank=True,choices=DEPARTMENT_CHOICES)
    collegeId=models.CharField(max_length=5,unique=True,null=True,blank=True)
    def __str__(self):
        return self.user.name
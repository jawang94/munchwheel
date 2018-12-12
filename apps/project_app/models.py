from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors["first_name_length"] = "First Name cannot be blank!"
        if not postData['first_name'].isalpha():
            errors["first_name_alpha"] = "First Name cannot contain numbers!"
        if len(postData['last_name']) < 1:
            errors["last_name_length"] = "Last Name cannot be blank!"
        if not postData['last_name'].isalpha():
            errors["last_name_alpha"] = "Last Name cannot contain numbers!"
        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be empty!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_regex'] = "Invalid Email!"
        if User.objects.filter(email=postData['email']):
            errors['email_taken'] = "Email already taken."
        if len(postData['password']) < 8:
            errors['password_length'] = "Password must be 8+ characters!"
        if postData['password'] != postData['confirm_password']:
            errors['password_confirmation'] = "Passwords do not match!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(('password'), max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

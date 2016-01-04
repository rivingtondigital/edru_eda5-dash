from django.db import models
from django.contrib.auth.models import User
import hashlib
from datetime import datetime

# Create your models here.

class AuthToken(models.Model):
    ip_address = models.CharField(max_length=255, null=True)
    token = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, null=True)
    issued = models.DateTimeField(null=True)
    renewed = models.DateTimeField(null=True)

    def get_token(self):
        if not self.token:
            m = hashlib.md5()
            m.update('{}{}'.format(self.user.email, datetime.now()))
            rags = m.hexdigest()
            self.token = '{}-{}'.format(rags[0:5], rags[5:-5])
            self.save()
        return self.token

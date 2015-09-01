from django.db import models as m

# Create your models here.


class Collection(m.Model):
    user_group = m.CharField(max_length=25)
    name = m.CharField(max_length=25)
    description = m.CharField(max_length=225)
    date_created = m.CharField(max_length=25)
    date_updated = m.CharField(max_length=25)
    date_added = m.CharField(max_length=25)
    is_visible = m.BooleanField(default=True)
    is_active = m.BooleanField(default=True)
    stats = m.CharField(max_length=225)

    def __unicode__(self):
        return self.name

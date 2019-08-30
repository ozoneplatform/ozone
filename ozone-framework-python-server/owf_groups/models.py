from django.db import models
from enum import Enum
from people.models import Person


class GroupStatus(Enum):
    active = 'active'
    inactive = 'inactive'


class OwfGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField(default=0)
    status = models.CharField(default=GroupStatus.active, max_length=8,
                              choices=[(tag.value, tag.name) for tag in GroupStatus])
    email = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=200, unique=True)
    automatic = models.BooleanField(default=True)
    display_name = models.CharField(max_length=200, blank=True, null=True)
    stack_default = models.BooleanField(default=False, blank=True, null=True)

    people = models.ManyToManyField(Person, through='OwfGroupPeople')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.display_name is None:
            self.display_name = self.name
            super(OwfGroup, self).save(*args, **kwargs)
        else:
            super(OwfGroup, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'owf_group'


class OwfGroupPeople(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(OwfGroup, on_delete=models.CASCADE)
    person = models.ForeignKey('people.Person', on_delete=models.CASCADE)

    def __str__(self):
        return f'group  = {self.group.name} & person =  {self.person.username}'

    class Meta:
        managed = True
        db_table = 'owf_group_people'
        unique_together = (('group', 'person'),)
from django.db import models
from intents.models import Intent, IntentDataType, IntentDataTypes


class WidgetDefIntent(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField(default=0)
    receive = models.BooleanField()
    send = models.BooleanField()
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE)
    widget_definition = models.ForeignKey('WidgetDefinition', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.intent.action} & {self.widget_definition.description}'

    class Meta:
        managed = True
        db_table = 'widget_def_intent'


class WidgetDefIntentDataTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    intent_data_type = models.ForeignKey(IntentDataType, on_delete=models.CASCADE)
    widget_definition_intent = models.ForeignKey(WidgetDefIntent, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'widget_def_intent_data_types'


class WidgetDefinition(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField()
    visible = models.BooleanField()
    image_url_medium = models.CharField(max_length=2083)
    image_url_small = models.CharField(max_length=2083)
    singleton = models.BooleanField()
    width = models.IntegerField()
    widget_version = models.CharField(max_length=2083, blank=True, null=True)
    height = models.IntegerField()
    widget_url = models.CharField(max_length=2083)
    widget_guid = models.CharField(unique=True, max_length=255)
    display_name = models.CharField(max_length=256)
    background = models.BooleanField(blank=True, null=True)
    universal_name = models.CharField(max_length=255, blank=True, null=True)
    descriptor_url = models.CharField(max_length=2083, blank=True, null=True)
    description = models.CharField(max_length=4000, blank=True, null=True)
    mobile_ready = models.BooleanField()

    def __str__(self):
        return self.display_name

    class Meta:
        managed = True
        db_table = 'widget_definition'


class WidgetDefinitionWidgetTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    widget_definition = models.OneToOneField(WidgetDefinition, on_delete=models.CASCADE)
    widget_type = models.ForeignKey('WidgetType', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'widget_definition_widget_types'
        unique_together = (('widget_definition', 'widget_type'),)


class WidgetType(models.Model):
    id = models.BigAutoField(primary_key=True)
    version = models.BigIntegerField()
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'widget_type'

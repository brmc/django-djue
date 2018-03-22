# -*- coding: utf-8 -*-

from django.db import models
from django.utils.text import ugettext_lazy as __
from model_utils.models import TimeStampedModel


class Example(TimeStampedModel):
    name = models.CharField(__('name'), max_length=50)
    description = models.TextField(__('description'))


class OtherExample(TimeStampedModel):
    dogs = models.CharField(__('dogs'), max_length=50,
                            choices=(('a', 'a'), ('b', 'b')))
    dates = models.DateField(__('dates'))


from django import forms


class ExampleForm(forms.ModelForm):
    class Meta:
        model = Example
        exclude = ()

    def as_vue(self):
        for name, field in self.fields.items():
            template: str = field.widget.template_name
            field.widget.template_name = template.replace('django/forms',
                                                          'djue')

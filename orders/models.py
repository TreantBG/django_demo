from django.db import models


class Products(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
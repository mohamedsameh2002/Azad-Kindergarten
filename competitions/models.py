from django.db import models


class Competitors(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    score=models.IntegerField()
    def __str__(self) -> str:
        return self.name

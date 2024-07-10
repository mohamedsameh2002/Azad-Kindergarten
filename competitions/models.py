from django.db import models


class Competitors(models.Model):
    All_GAMES = [
        ("Memory game", "Memory game"),
    ]

    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,unique=True)
    the_game=models.CharField(max_length=100,choices=All_GAMES,default="Memory game")
    score=models.IntegerField()
    Ranking=models.IntegerField()

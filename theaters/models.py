from django.db import models

class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=5)
    number = models.IntegerField()

    class Meta:
        unique_together = ('theater', 'row', 'number')

    def __str__(self):
        return f"{self.row}{self.number} - {self.theater.name}"
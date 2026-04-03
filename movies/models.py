from django.db import models
from theaters.models import Theater

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return self.title
    

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='showtimes')
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.start_time}"
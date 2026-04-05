from rest_framework import serializers
from .models import Movie, Showtime


# serializer for Movie model
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

# serializer for Showtime model
class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = '__all__' 

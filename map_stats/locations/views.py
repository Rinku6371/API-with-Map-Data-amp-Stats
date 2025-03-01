from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from django.db.models import Count
from .serializers import LocationSerializer

class LocationList(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [loc.longitude, loc.latitude],
                    },
                    "properties": {
                        "name": loc.name,
                        "category": loc.category,
                    },
                }
                for loc in locations
            ],
        }
        return Response(geojson)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LocationStats(APIView):
    def get(self, request):
        total_locations = Location.objects.count()
        most_common_category = (
            Location.objects.values('category')
            .annotate(count=Count('category'))
            .order_by('-count')
            .first()
        )
        stats = {
            "total_locations": total_locations,
            "most_common_category": most_common_category['category'] if most_common_category else None,
        }
        return Response(stats)

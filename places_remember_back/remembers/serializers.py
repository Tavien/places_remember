from rest_framework_gis.serializers import GeoFeatureModelSerializer

from remembers.models import RemembersModel


class RemembersSerializer(GeoFeatureModelSerializer):
    """
    A class to serialize locations as GeoJSON compatible data
    """
    class Meta:
        model = RemembersModel
        geo_field = 'location_point'
        auto_bbox = True
        fields = '__all__'

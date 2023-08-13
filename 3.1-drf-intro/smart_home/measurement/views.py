from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from .models import Measurement, Sensor
from .serializers import MeasurementSerializer, SensorSerializer


class MeasurementsListView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        sensor = Sensor.objects.filter(id=request.data.get('sensor')).first()
        Measurement.objects.create(
            sensor=sensor,
            temperature=request.data.get('temperature')
        )
        return Response({'status': 'OK'})


class SensorsListView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        Sensor.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        return Response({'status': 'OK'})


class SensorDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

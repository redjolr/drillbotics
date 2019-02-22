from rest_framework.serializers import ModelSerializer
import experiments

class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = experiments.models.Measurement
        fields = ('experiment_id', 'sensor_id', 'time_micro', 'value', 'experiment')

class ExperimentSerializer(ModelSerializer):
    # measurements = MeasurementSerializer(many=True)
    class Meta:
        model = experiments.models.Experiment
        fields = ('start_time', 'rock_id')

from rest_framework import serializers

class HelloSerializer(serializers.Serializer):
    client_ip = serializers.CharField()
    location = serializers.CharField(allow_null=True)
    greeting = serializers.CharField()

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import HelloSerializer

class HelloView(APIView):

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_location(self, ip):
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        if 'city' in data:
            return data['city']
        else:
            return None

    def get_weather(self, location):
        api_key = '63af0f513fc9af819af5def04505c748'
        response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric')
        data = response.json()
        return data['main']['temp']

    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Visitor')
        client_ip = self.get_client_ip(request)
        location = self.get_location(client_ip)
        temperature = self.get_weather(location)

        greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
        response_data = {
            'client_ip': client_ip,
            'location': location,
            'greeting': greeting
        }

        serializer = HelloSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

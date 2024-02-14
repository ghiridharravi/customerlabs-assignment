from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    
    
class DataHandlerView(APIView):
    def post(self, request):

        # Check for app secret token
        secret_token = request.headers.get('CL-X-TOKEN')
        if not secret_token:
            return Response({"message": "Un Authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get account based on secret token
        try:
            account = Account.objects.get(app_secret_token=secret_token)
        except Account.DoesNotExist:
            return Response({"message": "Invalid App Secret Token"}, status=status.HTTP_401_UNAUTHORIZED)

        # Get data and method
        data = request.data

        # Send data to account destinations
        for destination in Destination.objects.filter(account=account):
            response = send_data_to_destination(destination, data)
            
            
        # Check response status
        if response is not None:
            if response.status_code == 200:
                print(f"Data sent successfully to")
                return Response({'message': "Data sent successfully"})
            else:
                print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
                return Response({'message': "Failed to send data"})
        else:
            print(f"Unsupported HTTP method")
            return Response({'message': "Unsupported HTTP method"})
    

# View to get destinations for an account

def send_data_to_destination(destination, data):
    url = destination.url
    method = destination.http_method
    headers = destination.headers

    # Prepare headers
    prepared_headers = {key: value for key, value in headers.items()}
    
    # Send data based on HTTP method
    if method == 'GET':
        # Send data as query parameters
        response = requests.get(url, params=data, headers=prepared_headers)
    elif method == 'POST':
        # Send data as JSON payload
        response = requests.post(url, json=data, headers=prepared_headers)
    elif method == 'PUT':
        # Send data as JSON payload
        response = requests.put(url, json=data, headers=prepared_headers)
    elif method == 'DELETE':
        # Send data as JSON payload
        response = requests.delete(url, json=data, headers=prepared_headers)
    else:
        # Handle unsupported HTTP method
        response = None
        
    return response


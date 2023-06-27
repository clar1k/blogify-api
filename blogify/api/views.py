from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_data(request):
    data = Response({"username":"clar1k", "password":"clar1k123"})
    return data

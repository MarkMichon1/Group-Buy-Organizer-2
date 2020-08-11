from django.http import JsonResponse
from rest_framework.decorators import api_view

from users.models import User
from users.serializers import UserSelectSerializer

@api_view(['GET'])
def api_user_autocomplete(request):
    username = request.query_params['username']
    returned_users = User.objects.filter(username__icontains=username)[:5]
    serializer = UserSelectSerializer(returned_users, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def api_check_for_new_pms(request):
    pass


def api_send_pm(request):
    pass
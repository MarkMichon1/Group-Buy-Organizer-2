from rest_framework import serializers

from users.models import User

class UserSelectSerializer(serializers.ModelSerializer):
    '''Used in autocomplete forms to simply return the user's name and ID.'''
    class Meta:
        model = User
        fields = ['id', 'username']
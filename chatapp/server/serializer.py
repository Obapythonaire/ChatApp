from rest_framework import serializers
from .models import Category, Server, Channel


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for Channel model - converts channel data to/from JSON"""
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    """Serializer for Server model with nested channels and optional member count"""
    # Computed field for member count (only included when annotated in queryset)
    num_members = serializers.SerializerMethodField()
    # Nested serializer to include all channels belonging to this server
    channel_server = ChannelSerializer(many=True)
    
    class Meta:
        model = Server
        # Exclude 'member' field to avoid exposing user membership details
        exclude = ['member']

    def get_num_members(self, obj):
        """Return member count if it was annotated in the queryset, otherwise None"""
        if hasattr(obj, 'num_members'):
            return obj.num_members
        return None
    
    def to_representation(self, instance):
        """Override to conditionally remove num_members from response based on context"""
        data = super().to_representation(instance)
        num_members = self.context.get('num_members')
        # Remove num_members field if it wasn't requested via context
        if not num_members:
            data.pop('num_members', None)
        return data
from http.client import responses
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer

# API documentation schema for server list endpoint
# Defines query parameters and response format for OpenAPI/Swagger documentation
server_list_docs = extend_schema(
    # Response will be a list of servers using ServerSerializer
    responses=ServerSerializer(many=True),
    parameters=[
        # Filter servers by category name
        OpenApiParameter(
            name='category',
            description='Category of servers to retrieve',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
        # Limit the number of servers returned
        OpenApiParameter(
            name='quantity',
            description='Number of servers to retrieve',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        # Filter servers where current user is a member (requires authentication)
        OpenApiParameter(
            name='by_user',
            description='Retrieve servers created by the user',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
        ),
        # Get a specific server by ID (requires authentication)
        OpenApiParameter(
            name='by_server_id',
            description='Retrieve a specific server by its ID',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        # Include member count in the response
        OpenApiParameter(
            name='with_num_members',
            description='Retrieve the number of members in each server',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
        ),
    ],
)

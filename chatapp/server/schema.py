from http.client import responses
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import ServerSerializer, ChannelSerializer

server_list_docs = extend_schema(
    responses = ServerSerializer(many=True),
    parameters = [
        OpenApiParameter(
            name='category',
            description='Category of servers to retrieve',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='quantity',
            description='Number of servers to retrieve',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='by_user',
            description='Retrieve servers created by the user',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='by_server_id',
            description='Retrieve a specific server by its ID',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name='with_num_members',
            description='Retrieve the number of members in each server',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
        ),
    ],
)

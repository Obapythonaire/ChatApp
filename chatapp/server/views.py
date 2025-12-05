from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    ViewSet for listing and filtering servers.
    Supports filtering by category, user membership, server ID, and quantity.
    """
    queryset = Server.objects.all()

    def _check_authentication(self, request):
        """Verify user is authenticated, raise error if not."""
        if not request.user.is_authenticated:
            raise AuthenticationFailed("User must be authenticated for this operation")

    def _parse_query_params(self, request):
        """Extract and parse query parameters from request."""
        return {
            'category': request.query_params.get('category'),
            'quantity': request.query_params.get('quantity'),
            'by_user': request.query_params.get('by_user') == 'True',
            'by_server_id': request.query_params.get('by_server_id'),
            'with_num_members': request.query_params.get('with_num_members') == 'True',
        }

    def _apply_category_filter(self, category):
        """Filter queryset by category name."""
        if category:
            self.queryset = self.queryset.filter(category__name=category)

    def _apply_user_filter(self, request, by_user):
        """Filter queryset by user membership."""
        if by_user:
            self._check_authentication(request)
            self.queryset = self.queryset.filter(member=request.user.id)

    def _apply_server_id_filter(self, request, by_server_id):
        """Filter queryset by specific server ID."""
        if by_server_id:
            self._check_authentication(request)
            try:
                server_id = int(by_server_id)
                self.queryset = self.queryset.filter(id=server_id)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with id {by_server_id} not found"
                    )
            except ValueError:
                raise ValidationError(
                    detail=f"Invalid server ID format: {by_server_id}"
                )

    def _apply_member_count_annotation(self, with_num_members):
        """Annotate queryset with member count if requested."""
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count('member'))

    def _apply_quantity_limit(self, quantity):
        """Limit queryset to specified quantity."""
        if quantity:
            try:
                limit = int(quantity)
                if limit > 0:
                    self.queryset = self.queryset[:limit]
            except ValueError:
                raise ValidationError(detail=f"Invalid quantity format: {quantity}")

    @server_list_docs
    def list(self, request):
        """
        List servers with optional filtering.
        
        Query Parameters:
        - category: Filter by category name
        - by_user: Filter by current user's membership (requires authentication)
        - by_server_id: Filter by specific server ID (requires authentication)
        - with_num_members: Include member count in response
        - quantity: Limit number of results
        """
        params = self._parse_query_params(request)

        # Apply filters in logical order
        self._apply_category_filter(params['category'])
        self._apply_user_filter(request, params['by_user'])
        self._apply_server_id_filter(request, params['by_server_id'])
        self._apply_member_count_annotation(params['with_num_members'])
        self._apply_quantity_limit(params['quantity'])

        serializer = ServerSerializer(
            self.queryset,
            many=True,
            context={'num_members': params['with_num_members']}
        )
        return Response(serializer.data)
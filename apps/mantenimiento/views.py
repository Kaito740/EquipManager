from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters
from apps.core.permissions import DjangoModelPermissionsConView
from .models import TipoMantenimiento, TicketMantenimiento
from .serializers import TipoMantenimientoSerializer, TicketMantenimientoSerializer, CrearTicketMantenimientoSerializer, CerrarTicketMantenimientoSerializer
from .service import crear_ticket, cerrar_ticket


class TipoMantenimientoListView(generics.ListAPIView):
    queryset = TipoMantenimiento.objects.all()
    serializer_class = TipoMantenimientoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class TicketMantenimientoListView(generics.ListAPIView):
    queryset = TicketMantenimiento.objects.select_related('personal', 'tipo_mantenimiento').all()
    serializer_class = TicketMantenimientoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('estado', 'tipo_mantenimiento')
    search_fields = ('descripcion',)
    ordering_fields = ('fecha_inicio', 'fecha_cierre', 'estado')


class TicketMantenimientoDetailView(generics.RetrieveAPIView):
    queryset = TicketMantenimiento.objects.select_related('personal', 'tipo_mantenimiento').all()
    serializer_class = TicketMantenimientoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class TicketMantenimientoCreateView(generics.CreateAPIView):
    queryset = TicketMantenimiento.objects.all()
    serializer_class = TicketMantenimientoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def create(self, request, *args, **kwargs):
        serializer = CrearTicketMantenimientoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            ticket = crear_ticket(
                personal_id=serializer.validated_data['personal'],
                tipo_mantenimiento_id=serializer.validated_data['tipo_mantenimiento'],
                descripcion=serializer.validated_data['descripcion'],
                codigos_patrimoniales=serializer.validated_data['equipos']
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        response_serializer = TicketMantenimientoSerializer(ticket)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, DjangoModelPermissionsConView.para(TicketMantenimiento)])
def cerrar_ticket_view(request, pk):
    serializer = CerrarTicketMantenimientoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # Usar el id del usuario autenticado (del token JWT), nunca del body del request.
    # Esto evita que un usuario pueda suplantar a otro pasando un personal_id arbitrario.
    personal_id = request.user.id

    try:
        ticket = cerrar_ticket(
            ticket_id=pk,
            personal_id=personal_id,
            solucion=serializer.validated_data.get('solucion', ''),
            cambios_componentes=serializer.validated_data.get('cambios_componentes', [])
        )
        return Response(TicketMantenimientoSerializer(ticket).data, status=status.HTTP_200_OK)
    except TicketMantenimiento.DoesNotExist:
        return Response({'error': 'Ticket no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

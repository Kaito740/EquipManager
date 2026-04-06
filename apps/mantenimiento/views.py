from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import TipoMantenimiento, TicketMantenimiento
from .serializers import TipoMantenimientoSerializer, TicketMantenimientoSerializer, CrearTicketMantenimientoSerializer, CerrarTicketMantenimientoSerializer
from .service import crear_ticket, cerrar_ticket

class TipoMantenimientoListView(generics.ListAPIView):
    queryset = TipoMantenimiento.objects.all()
    serializer_class = TipoMantenimientoSerializer

class TicketMantenimientoListView(generics.ListAPIView):
    queryset = TicketMantenimiento.objects.select_related('personal', 'tipo_mantenimiento').all()
    serializer_class = TicketMantenimientoSerializer

class TicketMantenimientoDetailView(generics.RetrieveAPIView):
    queryset = TicketMantenimiento.objects.select_related('personal', 'tipo_mantenimiento').all()
    serializer_class = TicketMantenimientoSerializer

class TicketMantenimientoCreateView(generics.CreateAPIView):
    queryset = TicketMantenimiento.objects.all()
    serializer_class = TicketMantenimientoSerializer
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
@permission_classes([IsAuthenticated])
def cerrar_ticket_view(request, pk):
    serializer = CerrarTicketMantenimientoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    try:
        ticket = cerrar_ticket(
            ticket_id=pk,
            personal_id=serializer.validated_data['personal'],
            solucion=serializer.validated_data.get('solucion', ''),
            cambios_componentes=serializer.validated_data.get('cambios_componentes', [])
        )
        return Response(TicketMantenimientoSerializer(ticket).data, status=status.HTTP_200_OK)
    except TicketMantenimiento.DoesNotExist:
        return Response({'error': 'Ticket no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status, generics
from rest_framework.response import Response
from .models import TipoMantenimiento, TicketMantenimiento
from .serializers import TipoMantenimientoSerializer, TicketMantenimientoSerializer, CrearTicketMantenimientoSerializer
from .service import crear_ticket

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

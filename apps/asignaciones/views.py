from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from apps.actas.models import Acta
from apps.asignaciones.serializers import ActaCreateSerializer, ActaListSerializer, ActaDetailSerializer
from apps.asignaciones.service import crear_acta_entrega


class ActaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Acta.objects.select_related(
            'asignacion__empleado'
        ).order_by('-fecha')
        serializer = ActaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ActaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        personal_id = request.user.id

        try:
            crear_acta_entrega(
                personal_id=personal_id,
                empleado_id=serializer.validated_data['empleado_id'],
                equipo_ids=serializer.validated_data['equipos'],
                terminos_id=serializer.validated_data['terminos_id'],
                observaciones=serializer.validated_data.get('observaciones', ''),
                checklist=serializer.validated_data.get('checklist')
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Acta creada exitosamente'}, status=status.HTTP_201_CREATED)


class ActaDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        acta = get_object_or_404(
            Acta.objects.select_related(
                'asignacion__empleado'
            ).prefetch_related(
                'respuestas_checklist__equipo',
                'respuestas_checklist__checklist_item'
            ),
            pk=pk
        )
        serializer = ActaDetailSerializer(acta)
        return Response(serializer.data)
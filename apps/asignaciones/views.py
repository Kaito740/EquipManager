from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from apps.actas.models import Acta
from apps.core.permissions import DjangoModelPermissionsConView
from apps.asignaciones.serializers import ActaCreateSerializer, ActaListSerializer, ActaDetailSerializer, ActaMantenimientoCreateSerializer, ActaDevolucionCreateSerializer
from apps.asignaciones.service import crear_acta_entrega, crear_acta_mantenimiento, crear_acta_devolucion

# Permiso reutilizable para todas las views de este módulo — todas operan sobre Acta.
_PermisoActa = DjangoModelPermissionsConView.para(Acta)


class ActaView(APIView):
    permission_classes = [IsAuthenticated, _PermisoActa]

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
    permission_classes = [IsAuthenticated, _PermisoActa]

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


class ActaMantenimientoView(APIView):
    permission_classes = [IsAuthenticated, _PermisoActa]

    def post(self, request):
        serializer = ActaMantenimientoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        personal_id = request.user.id

        try:
            crear_acta_mantenimiento(
                personal_id=personal_id,
                ticket_id=serializer.validated_data['ticket_id'],
                terminos_id=serializer.validated_data['terminos_id'],
                observaciones=serializer.validated_data.get('observaciones', ''),
                checklist=serializer.validated_data['checklist']
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Acta de mantenimiento creada exitosamente'}, status=status.HTTP_201_CREATED)


class ActaDevolucionView(APIView):
    permission_classes = [IsAuthenticated, _PermisoActa]

    def post(self, request):
        serializer = ActaDevolucionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        personal_id = request.user.id

        try:
            crear_acta_devolucion(
                personal_id=personal_id,
                asignacion_id=serializer.validated_data['asignacion_id'],
                terminos_id=serializer.validated_data['terminos_id'],
                observaciones=serializer.validated_data.get('observaciones', ''),
                checklist=serializer.validated_data.get('checklist')
            )
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'error': f'Error de base de datos: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Acta de devolución creada exitosamente'}, status=status.HTTP_201_CREATED)
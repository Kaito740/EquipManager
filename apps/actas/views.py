from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.conf import settings
from xhtml2pdf import pisa
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.actas.models import Acta
from apps.core.permissions import DjangoModelPermissionsConView


_PermisoActa = DjangoModelPermissionsConView.para(Acta)


def link_callback(uri, rel):
    """
    Convierte URIs relativos a rutas absolutas del sistema para que
    xhtml2pdf pueda acceder a los recursos estáticos.
    """
    from django.contrib.staticfiles import finders

    if uri.startswith(settings.STATIC_URL):
        path = finders.find(uri.replace(settings.STATIC_URL, ''))
        if path:
            return path.path
    elif uri.startswith(settings.MEDIA_URL):
        path = settings.MEDIA_ROOT + uri.replace(settings.MEDIA_URL, '')
        if path:
            return path
    return None


class ActaPDFView(APIView):
    permission_classes = [IsAuthenticated, _PermisoActa]
    queryset = Acta.objects.all()

    def get(self, request, pk):
        acta = get_object_or_404(
            Acta.objects.select_related(
                # Relaciones para ENTREGA / DEVOLUCIÓN
                'asignacion__empleado__area__sucursal',
                'asignacion__empleado__cargo',
                'asignacion__sucursal',
                # Relaciones para MANTENIMIENTO
                'ticket__tipo_mantenimiento',
                # Personal que registró el acta
                'personal__cargo',
                'personal__area',
                # Términos y condiciones
                'terminos',
            ).prefetch_related(
                # Equipos de asignación: AsignacionEquipo → equipo → tipo_equipo + sucursal
                'asignacion__equipos__equipo__tipo_equipo',
                'asignacion__equipos__equipo__sucursal',
                # Equipos de ticket: TicketEquipo → equipo → tipo_equipo
                'ticket__equipos__equipo__tipo_equipo',
                'ticket__equipos__equipo__sucursal',
            ),
            pk=pk,
        )

        html = render_to_string('actas/acta_template.html', {'acta': acta}, request=request)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="acta_{acta.numero_acta}.pdf"'

        pisa_status = pisa.CreatePDF(
            html,
            dest=response,
            link_callback=link_callback,
            encoding='utf-8',
        )

        if pisa_status.err:
            return Response({'error': 'Error al generar el PDF'}, status=500)

        return response

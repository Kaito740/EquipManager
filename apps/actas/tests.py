import pytest
from django.core.exceptions import ValidationError
from apps.actas.models import TerminosCondiciones, Acta, RespuestaChecklist
from apps.personal.models import Cargo, Sucursal, Area, Personal
from apps.equipos.models import TipoEquipo, Equipo, ChecklistItem
from apps.asignaciones.models import Asignacion
from apps.mantenimiento.models import TipoMantenimiento, TicketMantenimiento
from apps.personal.models import Empleado
from datetime import date


@pytest.mark.django_db
class TestTerminosCondicionesModel:
    def test_crear_terminos(self):
        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Términos de entrega de equipos",
            fecha_vigencia=date.today()
        )

        assert terminos.tipo_acta == TerminosCondiciones.TipoActa.ENTREGA
        assert terminos.contenido == "Términos de entrega de equipos"
        assert terminos.activo is True

    def test_terminos_str(self):
        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        assert "Entrega" in str(terminos)
        assert str(date.today()) in str(terminos)


@pytest.mark.django_db
class TestActaModel:
    def test_crear_acta_entrega(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        assert acta.numero_acta == "001-2025"
        assert acta.tipo == Acta.Tipo.ENTREGA
        assert acta.asignacion == asignacion
        assert acta.personal == personal
        assert acta.ticket is None

    def test_crear_acta_mantenimiento(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")
        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test"
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.MANTENIMIENTO,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.MANTENIMIENTO,
            ticket=ticket,
            personal=personal,
            terminos=terminos
        )

        assert acta.tipo == Acta.Tipo.MANTENIMIENTO
        assert acta.ticket == ticket
        assert acta.asignacion is None

    def test_acta_numero_unique(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        with pytest.raises(Exception):
            Acta.objects.create(
                numero_acta="001-2025",
                tipo=Acta.Tipo.ENTREGA,
                asignacion=asignacion,
                personal=personal,
                terminos=terminos
            )

    def test_acta_str(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        assert "001-2025" in str(acta)
        assert "Entrega" in str(acta)

    def test_acta_asignacion_y_ticket_mutuamente_excluyentes(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")
        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test"
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            ticket=ticket,
            personal=personal,
            terminos=terminos
        )

        with pytest.raises(ValidationError):
            acta.full_clean()

    def test_acta_sin_asignacion_ni_ticket(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            personal=personal,
            terminos=terminos
        )

        with pytest.raises(ValidationError):
            acta.full_clean()

    def test_acta_observaciones_strip(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos,
            observaciones="  Observación de prueba  "
        )

        assert acta.observaciones == "Observación de prueba"


@pytest.mark.django_db
class TestRespuestaChecklistModel:
    def test_crear_respuesta_checklist(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        checklist_item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        respuesta = RespuestaChecklist.objects.create(
            acta=acta,
            equipo=equipo,
            checklist_item=checklist_item,
            respuesta=True
        )

        assert respuesta.acta == acta
        assert respuesta.equipo == equipo
        assert respuesta.checklist_item == checklist_item
        assert respuesta.respuesta is True

    def test_respuesta_checklist_unique(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        checklist_item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        RespuestaChecklist.objects.create(
            acta=acta,
            equipo=equipo,
            checklist_item=checklist_item,
            respuesta=True
        )

        with pytest.raises(Exception):
            RespuestaChecklist.objects.create(
                acta=acta,
                equipo=equipo,
                checklist_item=checklist_item,
                respuesta=False
            )

    def test_respuesta_checklist_str(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        empleado = Empleado.objects.create(
            dni="12345678",
            nombres="John",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        checklist_item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        asignacion = Asignacion.objects.create(
            empleado=empleado,
            personal=personal,
            sucursal=sucursal
        )

        terminos = TerminosCondiciones.objects.create(
            tipo_acta=TerminosCondiciones.TipoActa.ENTREGA,
            contenido="Test",
            fecha_vigencia=date.today()
        )

        acta = Acta.objects.create(
            numero_acta="001-2025",
            tipo=Acta.Tipo.ENTREGA,
            asignacion=asignacion,
            personal=personal,
            terminos=terminos
        )

        respuesta = RespuestaChecklist.objects.create(
            acta=acta,
            equipo=equipo,
            checklist_item=checklist_item,
            respuesta=True
        )

        assert "Conforme" in str(respuesta)

        respuesta_false = RespuestaChecklist.objects.create(
            acta=acta,
            equipo=equipo,
            checklist_item=ChecklistItem.objects.create(pregunta="¿Mouse funciona?"),
            respuesta=False
        )

        assert "No conforme" in str(respuesta_false)

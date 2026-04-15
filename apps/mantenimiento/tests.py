import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.mantenimiento.models import TipoMantenimiento, TicketMantenimiento, TicketEquipo
from apps.personal.models import Cargo, Sucursal, Area, Personal
from apps.equipos.models import TipoEquipo, Equipo


@pytest.mark.django_db
class TestTipoMantenimientoModel:
    def test_crear_tipo_mantenimiento(self):
        tipo = TipoMantenimiento.objects.create(nombre="Preventivo")
        assert tipo.nombre == "Preventivo"

    def test_tipo_mantenimiento_unique(self):
        TipoMantenimiento.objects.create(nombre="Preventivo")
        with pytest.raises(Exception):
            TipoMantenimiento.objects.create(nombre="Preventivo")

    def test_tipo_mantenimiento_str(self):
        tipo = TipoMantenimiento.objects.create(nombre="Correctivo")
        assert str(tipo) == "Correctivo"


@pytest.mark.django_db
class TestTicketMantenimientoModel:
    def test_crear_ticket(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )
        personal.cargo = cargo
        personal.save()

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Mantenimiento programado"
        )

        assert ticket.personal == personal
        assert ticket.tipo_mantenimiento == tipo_mantenimiento
        assert ticket.descripcion == "Mantenimiento programado"
        assert ticket.estado == TicketMantenimiento.Estado.ABIERTO
        assert ticket.fecha_inicio is not None
        assert ticket.fecha_cierre is None

    def test_ticket_estados(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test",
            estado=TicketMantenimiento.Estado.CERRADO,
            solucion="Problema resuelto"
        )

        assert ticket.estado == TicketMantenimiento.Estado.CERRADO
        assert ticket.get_estado_display() == "Cerrado"

    def test_ticket_str(self):
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

        assert "Ticket #" in str(ticket)
        assert "Preventivo" in str(ticket)

    def test_ticket_solucion(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Correctivo")

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Laptop no enciende",
            solucion="Reemplazado el disco duro"
        )

        assert ticket.solucion == "Reemplazado el disco duro"

    def test_ticket_fecha_cierre_anterior_a_inicio(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")

        now = timezone.now()
        yesterday = now - timezone.timedelta(days=1)

        ticket = TicketMantenimiento(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test",
            fecha_inicio=now,
            fecha_cierre=yesterday
        )

        with pytest.raises(ValidationError):
            ticket.full_clean()


@pytest.mark.django_db
class TestTicketEquipoModel:
    def test_crear_ticket_equipo(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal,
            estado=Equipo.Estado.EN_USO
        )

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test"
        )

        ticket_equipo = TicketEquipo.objects.create(
            ticket=ticket,
            equipo=equipo,
            estado_anterior=Equipo.Estado.EN_USO
        )

        assert ticket_equipo.ticket == ticket
        assert ticket_equipo.equipo == equipo
        assert ticket_equipo.estado_anterior == Equipo.Estado.EN_USO

    def test_ticket_equipo_unique(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test"
        )

        TicketEquipo.objects.create(
            ticket=ticket,
            equipo=equipo
        )

        with pytest.raises(Exception):
            TicketEquipo.objects.create(
                ticket=ticket,
                equipo=equipo
            )

    def test_ticket_equipo_str(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )

        tipo_mantenimiento = TipoMantenimiento.objects.create(nombre="Preventivo")
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        ticket = TicketMantenimiento.objects.create(
            personal=personal,
            tipo_mantenimiento=tipo_mantenimiento,
            descripcion="Test"
        )

        ticket_equipo = TicketEquipo.objects.create(
            ticket=ticket,
            equipo=equipo
        )

        assert "EMP-001" in str(ticket_equipo)

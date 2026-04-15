import pytest
from apps.asignaciones.models import Asignacion, AsignacionEquipo
from apps.personal.models import Cargo, Sucursal, Area, Personal, Empleado
from apps.equipos.models import TipoEquipo, Equipo


@pytest.mark.django_db
class TestAsignacionModel:
    def test_crear_asignacion(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="tecnico",
            password="testpass123"
        )
        personal.cargo = cargo
        personal.area = area
        personal.save()

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

        assert asignacion.empleado == empleado
        assert asignacion.personal == personal
        assert asignacion.sucursal == sucursal
        assert asignacion.fecha is not None

    def test_asignacion_str(self):
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

        assert "Asignación #" in str(asignacion)
        assert "Doe, John" in str(asignacion)


@pytest.mark.django_db
class TestAsignacionEquipoModel:
    def test_crear_asignacion_equipo(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")

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

        asignacion_equipo = AsignacionEquipo.objects.create(
            asignacion=asignacion,
            equipo=equipo
        )

        assert asignacion_equipo.asignacion == asignacion
        assert asignacion_equipo.equipo == equipo

    def test_asignacion_equipo_unique(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")

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

        AsignacionEquipo.objects.create(
            asignacion=asignacion,
            equipo=equipo
        )

        with pytest.raises(Exception):
            AsignacionEquipo.objects.create(
                asignacion=asignacion,
                equipo=equipo
            )

    def test_asignacion_equipo_str(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")

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

        ae = AsignacionEquipo.objects.create(
            asignacion=asignacion,
            equipo=equipo
        )

        assert "EMP-001" in str(ae)

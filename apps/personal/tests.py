import pytest
from django.core.exceptions import ValidationError
from apps.personal.models import Cargo, Sucursal, Area, Personal, Empleado


@pytest.mark.django_db
class TestCargoModel:
    def test_crear_cargo(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        assert cargo.nombre == "Técnico"
        assert cargo.activo is True

    def test_cargo_unique(self):
        Cargo.objects.create(nombre="Técnico")
        with pytest.raises(Exception):
            Cargo.objects.create(nombre="Técnico")

    def test_cargo_str(self):
        cargo = Cargo.objects.create(nombre="Administrador")
        assert str(cargo) == "Administrador"

    def test_cargo_strip(self):
        cargo = Cargo.objects.create(nombre="  Técnico  ")
        assert cargo.nombre == "Técnico"


@pytest.mark.django_db
class TestSucursalModel:
    def test_crear_sucursal(self):
        sucursal = Sucursal.objects.create(nombre="Lima")
        assert sucursal.nombre == "Lima"
        assert sucursal.activo is True

    def test_sucursal_unique(self):
        Sucursal.objects.create(nombre="Lima")
        with pytest.raises(Exception):
            Sucursal.objects.create(nombre="Lima")

    def test_sucursal_str(self):
        sucursal = Sucursal.objects.create(nombre="Arequipa")
        assert str(sucursal) == "Arequipa"


@pytest.mark.django_db
class TestAreaModel:
    def test_crear_area(self):
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        assert area.nombre == "Sistemas"
        assert area.sucursal == sucursal
        assert area.activo is True

    def test_area_str(self):
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        assert str(area) == "Lima — Sistemas"

    def test_area_unique_por_sucursal(self):
        sucursal = Sucursal.objects.create(nombre="Lima")
        Area.objects.create(nombre="Sistemas", sucursal=sucursal)
        with pytest.raises(Exception):
            Area.objects.create(nombre="Sistemas", sucursal=sucursal)

    def test_area_diferente_sucursal_mismo_nombre(self):
        sucursal1 = Sucursal.objects.create(nombre="Lima")
        sucursal2 = Sucursal.objects.create(nombre="Arequipa")
        Area.objects.create(nombre="Sistemas", sucursal=sucursal1)
        area2 = Area.objects.create(nombre="Sistemas", sucursal=sucursal2)
        assert area2.nombre == "Sistemas"


@pytest.mark.django_db
class TestPersonalModel:
    def test_crear_personal_completo(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        personal = Personal.objects.create_user(
            username="jsmith",
            password="testpass123",
            first_name="John",
            last_name="Smith",
            dni="12345678",
            cargo=cargo,
            area=area
        )

        assert personal.username == "jsmith"
        assert personal.first_name == "John"
        assert personal.last_name == "Smith"
        assert personal.dni == "12345678"
        assert personal.cargo == cargo
        assert personal.area == area
        assert personal.is_active is True
        assert personal.check_password("testpass123")

    def test_personal_dni_unique(self):
        Personal.objects.create_user(
            username="user1",
            password="testpass123",
            dni="12345678"
        )
        with pytest.raises(Exception):
            Personal.objects.create_user(
                username="user2",
                password="testpass123",
                dni="12345678"
            )

    def test_personal_str(self):
        personal = Personal.objects.create_user(
            username="jsmith",
            password="testpass123",
            first_name="John",
            last_name="Smith"
        )
        assert str(personal) == "Smith, John"

    def test_personal_dni_8_digitos(self):
        personal = Personal.objects.create_user(
            username="user",
            password="pass"
        )
        personal.dni = "12345678"
        personal.full_clean()
        personal.save()
        assert personal.dni == "12345678"

    def test_personal_dni_invalid(self):
        personal = Personal.objects.create_user(
            username="user",
            password="pass"
        )
        personal.dni = "123"
        with pytest.raises(ValidationError):
            personal.full_clean()


@pytest.mark.django_db
class TestEmpleadoModel:
    def test_crear_empleado(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        empleado = Empleado.objects.create(
            dni="87654321",
            nombres="Jane",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        assert empleado.dni == "87654321"
        assert empleado.nombres == "Jane"
        assert empleado.apellidos == "Doe"
        assert empleado.cargo == cargo
        assert empleado.area == area
        assert empleado.activo is True

    def test_empleado_unique(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        Empleado.objects.create(
            dni="87654321",
            nombres="Jane",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        with pytest.raises(Exception):
            Empleado.objects.create(
                dni="87654321",
                nombres="Other",
                apellidos="Name",
                cargo=cargo,
                area=area
            )

    def test_empleado_str(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        empleado = Empleado.objects.create(
            dni="87654321",
            nombres="Jane",
            apellidos="Doe",
            cargo=cargo,
            area=area
        )

        assert str(empleado) == "Doe, Jane"

    def test_empleado_strip(self):
        cargo = Cargo.objects.create(nombre="Técnico")
        sucursal = Sucursal.objects.create(nombre="Lima")
        area = Area.objects.create(nombre="Sistemas", sucursal=sucursal)

        empleado = Empleado.objects.create(
            dni="87654321",
            nombres="  Jane  ",
            apellidos="  Doe  ",
            cargo=cargo,
            area=area
        )

        assert empleado.nombres == "Jane"
        assert empleado.apellidos == "Doe"

import pytest
from django.core.exceptions import ValidationError
from apps.equipos.models import (
    TipoEquipo, TipoAtributo, TipoEquipoAtributo, Equipo,
    ValorAtributo, TipoComponente, Componente, EquipoComponente,
    ChecklistItem, TipoEquipoChecklist
)
from apps.personal.models import Sucursal


@pytest.mark.django_db
class TestTipoEquipoModel:
    def test_crear_tipo_equipo(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop", descripcion="Portátil")
        assert tipo.nombre == "Laptop"
        assert tipo.descripcion == "Portátil"

    def test_tipo_equipo_unique(self):
        TipoEquipo.objects.create(nombre="Laptop")
        with pytest.raises(Exception):
            TipoEquipo.objects.create(nombre="Laptop")

    def test_tipo_equipo_str(self):
        tipo = TipoEquipo.objects.create(nombre="Monitor")
        assert str(tipo) == "Monitor"

    def test_tipo_equipo_strip(self):
        tipo = TipoEquipo.objects.create(nombre="  Laptop  ", descripcion="  Test  ")
        assert tipo.nombre == "Laptop"
        assert tipo.descripcion == "Test"


@pytest.mark.django_db
class TestTipoAtributoModel:
    def test_crear_tipo_atributo(self):
        attr = TipoAtributo.objects.create(nombre="Procesador")
        assert attr.nombre == "Procesador"

    def test_tipo_atributo_unique(self):
        TipoAtributo.objects.create(nombre="Procesador")
        with pytest.raises(Exception):
            TipoAtributo.objects.create(nombre="Procesador")


@pytest.mark.django_db
class TestEquipoModel:
    def test_crear_equipo(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            numero_serie="SN123456",
            tipo_equipo=tipo,
            sucursal=sucursal
        )

        assert equipo.codigo_patrimonial == "EMP-001"
        assert equipo.numero_serie == "SN123456"
        assert equipo.tipo_equipo == tipo
        assert equipo.sucursal == sucursal
        assert equipo.estado == Equipo.Estado.DISPONIBLE

    def test_equipo_codigo_unique(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo,
            sucursal=sucursal
        )

        with pytest.raises(Exception):
            Equipo.objects.create(
                codigo_patrimonial="EMP-001",
                tipo_equipo=tipo,
                sucursal=sucursal
            )

    def test_equipo_serie_unique(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            numero_serie="SN123456",
            tipo_equipo=tipo,
            sucursal=sucursal
        )

        with pytest.raises(Exception):
            Equipo.objects.create(
                codigo_patrimonial="EMP-002",
                numero_serie="SN123456",
                tipo_equipo=tipo,
                sucursal=sucursal
            )

    def test_equipo_str(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo,
            sucursal=sucursal
        )

        assert str(equipo) == "EMP-001 — Laptop"

    def test_equipo_estados(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo,
            sucursal=sucursal,
            estado=Equipo.Estado.EN_USO
        )

        assert equipo.estado == Equipo.Estado.EN_USO
        assert equipo.get_estado_display() == "En uso"

    def test_equipo_strip(self):
        tipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="  EMP-001  ",
            numero_serie="  SN123456  ",
            tipo_equipo=tipo,
            sucursal=sucursal
        )

        assert equipo.codigo_patrimonial == "EMP-001"
        assert equipo.numero_serie == "SN123456"


@pytest.mark.django_db
class TestValorAtributoModel:
    def test_crear_valor_atributo(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        tipo_atributo = TipoAtributo.objects.create(nombre="Procesador")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        valor = ValorAtributo.objects.create(
            equipo=equipo,
            tipo_atributo=tipo_atributo,
            valor="Intel i7"
        )

        assert valor.equipo == equipo
        assert valor.tipo_atributo == tipo_atributo
        assert valor.valor == "Intel i7"

    def test_valor_atributo_unique_por_equipo(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        tipo_atributo = TipoAtributo.objects.create(nombre="Procesador")
        sucursal = Sucursal.objects.create(nombre="Lima")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        ValorAtributo.objects.create(
            equipo=equipo,
            tipo_atributo=tipo_atributo,
            valor="Intel i7"
        )

        with pytest.raises(Exception):
            ValorAtributo.objects.create(
                equipo=equipo,
                tipo_atributo=tipo_atributo,
                valor="AMD Ryzen 7"
            )


@pytest.mark.django_db
class TestTipoComponenteModel:
    def test_crear_tipo_componente(self):
        tipo = TipoComponente.objects.create(nombre="Disco Duro")
        assert tipo.nombre == "Disco Duro"

    def test_tipo_componente_unique(self):
        TipoComponente.objects.create(nombre="Disco Duro")
        with pytest.raises(Exception):
            TipoComponente.objects.create(nombre="Disco Duro")


@pytest.mark.django_db
class TestComponenteModel:
    def test_crear_componente(self):
        tipo = TipoComponente.objects.create(nombre="Disco Duro")
        componente = Componente.objects.create(
            tipo_componente=tipo,
            numero_serie="SN123456",
            descripcion="SSD 512GB"
        )

        assert componente.tipo_componente == tipo
        assert componente.numero_serie == "SN123456"
        assert componente.descripcion == "SSD 512GB"

    def test_componente_str(self):
        tipo = TipoComponente.objects.create(nombre="Disco Duro")
        componente = Componente.objects.create(
            tipo_componente=tipo,
            numero_serie="SN123456",
            descripcion="SSD 512GB"
        )

        assert "SSD 512GB" in str(componente)
        assert "SN123456" in str(componente)


@pytest.mark.django_db
class TestEquipoComponenteModel:
    def test_crear_equipo_componente(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")
        tipo_componente = TipoComponente.objects.create(nombre="Disco Duro")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        componente = Componente.objects.create(
            tipo_componente=tipo_componente,
            descripcion="SSD 512GB"
        )

        from django.utils import timezone

        ec = EquipoComponente.objects.create(
            equipo=equipo,
            componente=componente,
            fecha_entrada=timezone.now()
        )

        assert ec.equipo == equipo
        assert ec.componente == componente
        assert ec.fecha_salida is None

    def test_equipo_componente_fecha_salida(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        sucursal = Sucursal.objects.create(nombre="Lima")
        tipo_componente = TipoComponente.objects.create(nombre="Disco Duro")

        equipo = Equipo.objects.create(
            codigo_patrimonial="EMP-001",
            tipo_equipo=tipo_equipo,
            sucursal=sucursal
        )

        componente = Componente.objects.create(
            tipo_componente=tipo_componente,
            descripcion="SSD 512GB"
        )

        from django.utils import timezone
        fecha_entrada = timezone.now()
        fecha_salida = timezone.now()

        ec = EquipoComponente.objects.create(
            equipo=equipo,
            componente=componente,
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida
        )

        assert ec.fecha_salida is not None


@pytest.mark.django_db
class TestChecklistItemModel:
    def test_crear_checklist_item(self):
        item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")
        assert item.pregunta == "¿Pantalla funciona?"
        assert item.activo is True

    def test_checklist_item_unique(self):
        ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")
        with pytest.raises(Exception):
            ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

    def test_checklist_item_str(self):
        item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")
        assert str(item) == "¿Pantalla funciona?"


@pytest.mark.django_db
class TestTipoEquipoChecklistModel:
    def test_crear_tipo_equipo_checklist(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        checklist_item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

        link = TipoEquipoChecklist.objects.create(
            tipo_equipo=tipo_equipo,
            checklist_item=checklist_item
        )

        assert link.tipo_equipo == tipo_equipo
        assert link.checklist_item == checklist_item

    def test_tipo_equipo_checklist_unique(self):
        tipo_equipo = TipoEquipo.objects.create(nombre="Laptop")
        checklist_item = ChecklistItem.objects.create(pregunta="¿Pantalla funciona?")

        TipoEquipoChecklist.objects.create(
            tipo_equipo=tipo_equipo,
            checklist_item=checklist_item
        )

        with pytest.raises(Exception):
            TipoEquipoChecklist.objects.create(
                tipo_equipo=tipo_equipo,
                checklist_item=checklist_item
            )

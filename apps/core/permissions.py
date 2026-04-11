from rest_framework.permissions import DjangoModelPermissions


class DjangoModelPermissionsConView(DjangoModelPermissions):
    """
    Extiende DjangoModelPermissions para funcionar en APIView puras que no
    tienen atributo `queryset` (solo tienen lógica de negocio en el método).

    DjangoModelPermissions estándar falla con AttributeError en vistas sin
    queryset porque no puede inferir el modelo. Esta clase recibe el modelo
    explícitamente en el constructor y construye el queryset mínimo necesario
    solo para que el sistema de permisos pueda resolver app_label y model_name.

    Uso:
        from apps.core.permissions import DjangoModelPermissionsConView
        from apps.actas.models import Acta

        class MiView(APIView):
            permission_classes = [DjangoModelPermissionsConView.para(Acta)]
    """

    def __init__(self, modelo):
        self._modelo = modelo
        super().__init__()

    def get_queryset(self, view):
        return self._modelo.objects.none()

    @classmethod
    def para(cls, modelo):
        """
        Retorna una subclase de permiso ligada a `modelo`.
        Se usa como: permission_classes = [DjangoModelPermissionsConView.para(Acta)]
        """
        class PermisoParaModelo(cls):
            def __init__(self):
                super().__init__(modelo)
        PermisoParaModelo.__name__ = f'Permiso{modelo.__name__}'
        return PermisoParaModelo

"""Clase abstracta EntidadBase y clase Cliente (encapsulacion + validaciones)."""
import re
from abc import ABC, abstractmethod
from excepciones import ClienteInvalidoError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador):
        self._identificador = identificador      # atributo protegido (encapsulado)

    @property
    def identificador(self):
        """Solo lectura: el identificador no puede cambiarse tras crear la entidad."""
        return self._identificador

    @abstractmethod
    def describir(self):
        """Cada entidad concreta debe describirse a si misma (polimorfismo)."""

    def __str__(self):
        return self.describir()


class Cliente(EntidadBase):
    """Cliente de Software FJ. Los datos personales son privados y se validan al asignarlos."""

    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, identificador, nombre, documento, correo, telefono):
        super().__init__(identificador)
        # Las asignaciones pasan por los setters, que validan y lanzan ClienteInvalidoError
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # ---------------- nombre ----------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres.")
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError("El nombre no puede contener numeros.")
        self.__nombre = valor.strip().title()

    # ---------------- documento ----------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or not 6 <= len(valor) <= 12:
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 digitos numericos.")
        self.__documento = valor

    # ---------------- correo ----------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo electronico invalido: {valor!r}.")
        self.__correo = valor.strip().lower()

    # ---------------- telefono ----------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError("El telefono debe tener entre 7 y 10 digitos.")
        self.__telefono = valor

    def describir(self):
        """Describe al cliente ocultando parte del documento (proteccion de datos)."""
        oculto = "*" * (len(self.documento) - 3) + self.documento[-3:]
        return f"[{self.identificador}] {self.nombre} | Doc: {oculto} | {self.correo}"

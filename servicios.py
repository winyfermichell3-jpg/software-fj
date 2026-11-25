"""Clase abstracta Servicio y tres servicios especializados (herencia + polimorfismo)."""
from abc import abstractmethod
from entidades import EntidadBase
from excepciones import (ServicioInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError)


class Servicio(EntidadBase):
    """Clase abstracta: define el contrato comun de todos los servicios."""

    def __init__(self, identificador, nombre, tarifa_hora):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa por hora invalida: {tarifa_hora!r}.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = True                  # un servicio puede deshabilitarse

    # ----- propiedades -----
    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    # ----- metodos abstractos (cada hija los sobrescribe) -----
    @abstractmethod
    def validar_parametros(self, horas, **extras):
        """Valida duracion y parametros propios del servicio; lanza ServicioInvalidoError."""

    @abstractmethod
    def calcular_costo_base(self, horas, **extras):
        """Costo sin impuestos ni descuentos; la formula depende del tipo de servicio."""

    # ----- SOBRECARGA SIMULADA de calcular_costo -----
    def calcular_costo(self, *args, **extras):
        """
        Tres variantes segun la cantidad de argumentos posicionales:
            calcular_costo(horas)                        -> costo base
            calcular_costo(horas, impuesto)              -> base + impuesto
            calcular_costo(horas, impuesto, descuento)   -> base - descuento + impuesto
        """
        if not 1 <= len(args) <= 3:
            raise ParametroFaltanteError(
                f"calcular_costo requiere de 1 a 3 argumentos y recibio {len(args)}.")
        horas = args[0]
        impuesto = args[1] if len(args) >= 2 else 0.0
        descuento = args[2] if len(args) == 3 else 0.0
        # Validaciones de coherencia financiera
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango [0,1]: {impuesto}.")
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango [0,1]: {descuento}.")
        self.validar_parametros(horas, **extras)
        base = self.calcular_costo_base(horas, **extras)
        total = base * (1 - descuento) * (1 + impuesto)
        if total < 0:
            raise CalculoInconsistenteError("El costo total resulto negativo.")
        return round(total, 2)

    def describir(self):
        estado = "disponible" if self._disponible else "NO disponible"
        return f"[{self.identificador}] {self.nombre} (${self._tarifa_hora:,.0f}/h, {estado})"


class ReservaSala(Servicio):
    """Reserva de salas: depende de la capacidad y del numero de asistentes."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ServicioInvalidoError(f"Capacidad invalida: {capacidad!r}.")
        self._capacidad = capacidad

    def validar_parametros(self, horas, **extras):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 8:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")
        personas = extras.get("personas", 1)
        if personas > self._capacidad:
            raise ServicioInvalidoError(
                f"{personas} personas exceden la capacidad de {self._capacidad}.")

    def calcular_costo_base(self, horas, **extras):
        return self._tarifa_hora * horas

    def describir(self):
        return "SALA " + super().describir() + f" | capacidad {self._capacidad}"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: cobra un cargo fijo de seguro opcional."""
    CARGO_SEGURO = 15000.0

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise ServicioInvalidoError("Debe indicarse el tipo de equipo.")
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, horas, **extras):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")

    def calcular_costo_base(self, horas, **extras):
        seguro = self.CARGO_SEGURO if extras.get("seguro", False) else 0.0
        return self._tarifa_hora * horas + seguro

    def describir(self):
        return f"EQUIPO ({self._tipo_equipo}) " + super().describir()


class AsesoriaEspecializada(Servicio):
    """Asesorias: la tarifa se multiplica segun el nivel del asesor."""
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.2}

    def __init__(self, identificador, nombre, tarifa_hora, area):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(area, str) or not area.strip():
            raise ServicioInvalidoError("Debe indicarse el area de la asesoria.")
        self._area = area.strip()

    def validar_parametros(self, horas, **extras):
        if not isinstance(horas, (int, float)) or not 1 <= horas <= 6:
            raise ServicioInvalidoError("Una asesoria dura entre 1 y 6 horas.")
        if extras.get("nivel", "junior") not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel de asesor invalido. Use: {list(self.NIVELES)}.")

    def calcular_costo_base(self, horas, **extras):
        return self._tarifa_hora * self.NIVELES[extras.get("nivel", "junior")] * horas

    def describir(self):
        return f"ASESORIA ({self._area}) " + super().describir()

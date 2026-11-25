"""Clase Reserva: integra cliente, servicio, duracion y estado."""
from entidades import EntidadBase, Cliente
from servicios import Servicio
from registro import log
from excepciones import (ErrorSoftwareFJ, ReservaInvalidaError, ServicioNoDisponibleError,
                         OperacionNoPermitidaError)

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(EntidadBase):
    def __init__(self, identificador, cliente, servicio, horas, **extras):
        super().__init__(identificador)
        # Validacion de tipos
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Cliente y un Servicio validos.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no esta disponible.")
        try:
            servicio.validar_parametros(horas, **extras)
        except ErrorSoftwareFJ as causa:
            # ENCADENAMIENTO: el error original queda como __cause__ de la nueva excepcion
            raise ReservaInvalidaError(f"Parametros de reserva incorrectos: {causa}") from causa
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._extras = horas, extras
        self._estado = PENDIENTE
        self._costo_total = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva PENDIENTE (estado actual: {self._estado}).")
        self._estado = CONFIRMADA

    def cancelar(self):
        """PENDIENTE o CONFIRMADA -> CANCELADA. Una reserva procesada no se cancela."""
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}.")
        self._estado = CANCELADA

    def procesar(self, impuesto=0.19, descuento=0.0):
        """CONFIRMADA -> PROCESADA, calculando el costo final (try/except/else/finally)."""
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesa una reserva CONFIRMADA (estado actual: {self._estado}).")
        try:
            costo = self._servicio.calcular_costo(self._horas, impuesto, descuento, **self._extras)
        except ErrorSoftwareFJ as causa:
            log.error("Fallo el procesamiento de %s: %s", self.identificador, causa)
            raise OperacionNoPermitidaError("No fue posible procesar la reserva.") from causa
        else:
            # Se ejecuta SOLO si no hubo excepcion
            self._estado, self._costo_total = PROCESADA, costo
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya error o no
            log.debug("Intento de procesamiento de %s finalizado.", self.identificador)

    def describir(self):
        costo = f" | total ${self._costo_total:,.2f}" if self._costo_total is not None else ""
        return (f"[{self.identificador}] {self._cliente.nombre} -> {self._servicio.nombre} "
                f"x {self._horas}h | {self._estado}{costo}")

"""Excepciones personalizadas de Software FJ.
Todas heredan de ErrorSoftwareFJ, lo que permite capturar cualquier error propio
del sistema con un solo 'except ErrorSoftwareFJ' o ser especificos cuando se necesite."""


class ErrorSoftwareFJ(Exception):
    """Excepcion base del sistema (raiz de la jerarquia de errores propios)."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos personales del cliente invalidos (nombre, documento, correo, telefono)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Se intento crear un servicio con datos incorrectos."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parametro obligatorio o la cantidad de argumentos es incorrecta."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado esta deshabilitado y no puede reservarse."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no pudo crearse (cliente, servicio o duracion invalidos)."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Transicion de estado no permitida (ej.: procesar una reserva sin confirmar)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Impuestos, descuentos o costos que producen un resultado incoherente."""

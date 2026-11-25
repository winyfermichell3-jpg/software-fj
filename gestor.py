"""GestorFJ: coordina clientes, servicios y reservas sin base de datos (solo listas)."""
from entidades import Cliente
from reservas import Reserva
from registro import log
from excepciones import ErrorSoftwareFJ, ReservaInvalidaError


class GestorFJ:
    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []   # "base de datos" en memoria

    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """
        Envoltorio que garantiza la estabilidad: ejecuta una operacion, registra el resultado
        y NUNCA deja escapar una excepcion. Devuelve (exito, resultado_o_mensaje).
        """
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as error:                     # errores propios del dominio
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            log.error("%s -> %s: %s%s", descripcion, type(error).__name__, error, causa)
            return False, f"{type(error).__name__}: {error}"
        except Exception as error:                           # cualquier imprevisto
            log.critical("%s -> ERROR INESPERADO %s: %s", descripcion, type(error).__name__, error)
            return False, f"Error inesperado ({type(error).__name__}): {error}"
        else:
            log.info("%s -> OK", descripcion)
            return True, resultado
        finally:
            log.debug("Fin de operacion: %s", descripcion)

    # ----- registros -----
    def registrar_cliente(self, nombre, documento, correo, telefono):
        def crear():
            cliente = Cliente(f"CLI-{len(self.clientes) + 1:03d}", nombre, documento, correo, telefono)
            if any(c.documento == cliente.documento for c in self.clientes):
                raise ReservaInvalidaError("Ya existe un cliente con ese documento.")
            self.clientes.append(cliente)
            return cliente
        return self._ejecutar(f"Registrar cliente {nombre!r}", crear)

    def crear_servicio(self, clase, nombre, tarifa_hora, dato_extra):
        def crear():
            servicio = clase(f"SRV-{len(self.servicios) + 1:03d}", nombre, tarifa_hora, dato_extra)
            self.servicios.append(servicio)
            return servicio
        return self._ejecutar(f"Crear servicio {nombre!r}", crear)

    def crear_reserva(self, cliente, servicio, horas, **extras):
        def crear():
            reserva = Reserva(f"RES-{len(self.reservas) + 1:03d}", cliente, servicio, horas, **extras)
            self.reservas.append(reserva)
            return reserva
        return self._ejecutar(f"Crear reserva ({getattr(servicio, 'nombre', servicio)})", crear)

    def confirmar(self, reserva):
        return self._ejecutar(f"Confirmar {reserva.identificador}", reserva.confirmar)

    def cancelar(self, reserva):
        return self._ejecutar(f"Cancelar {reserva.identificador}", reserva.cancelar)

    def procesar(self, reserva, impuesto=0.19, descuento=0.0):
        return self._ejecutar(f"Procesar {reserva.identificador}", reserva.procesar, impuesto, descuento)

    def calcular(self, servicio, *args, **extras):
        return self._ejecutar(f"Calcular costo {servicio.nombre}", servicio.calcular_costo, *args, **extras)

"""Software FJ - simulacion de 17 operaciones (validas e invalidas) sin base de datos."""
from registro import configurar_logger, RUTA_LOG
from gestor import GestorFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada

contador = 0


def mostrar(titulo, resultado):
    """Imprime el resultado numerado de cada operacion simulada."""
    global contador
    contador += 1
    exito, valor = resultado
    marca = "OK   " if exito else "ERROR"
    print(f"{contador:02d}. [{marca}] {titulo}\n      -> {valor}")


def main():
    configurar_logger(reiniciar=True)
    g = GestorFJ()
    print("=== SOFTWARE FJ: sistema de clientes, servicios y reservas ===\n")

    # ---- Clientes ----
    ok, ana = g.registrar_cliente("ana maria rojas", "1020304050", "ana.rojas@correo.com", "3101234567")
    mostrar("Registro valido de cliente (Ana)", (ok, ana))
    mostrar("Registro invalido: correo sin dominio",
            g.registrar_cliente("Pedro Gomez", "55667788", "pedro@@correo", "3001112233"))
    mostrar("Registro invalido: documento con letras",
            g.registrar_cliente("Luis Perez", "ABC12345", "luis@correo.com", "3001112233"))
    ok, carlos = g.registrar_cliente("Carlos Diaz", "79880011", "carlos.diaz@correo.com", "3157778899")
    mostrar("Registro valido de cliente (Carlos)", (ok, carlos))

    # ---- Servicios ----
    ok, sala = g.crear_servicio(ReservaSala, "Sala Innovacion", 50000, 12)
    mostrar("Servicio valido: sala", (ok, sala))
    mostrar("Servicio invalido: tarifa negativa", g.crear_servicio(ReservaSala, "Sala Fantasma", -100, 5))
    ok, equipo = g.crear_servicio(AlquilerEquipo, "Videobeam HD", 12000, "Proyector")
    mostrar("Servicio valido: equipo", (ok, equipo))
    ok, asesoria = g.crear_servicio(AsesoriaEspecializada, "Asesoria Cloud", 80000, "Computacion en la nube")
    mostrar("Servicio valido: asesoria", (ok, asesoria))

    # ---- Reservas ----
    ok, r1 = g.crear_reserva(ana, sala, 3, personas=10)
    mostrar("Reserva exitosa: Ana en la sala (3h)", (ok, r1))
    mostrar("Reserva fallida: 20 horas en sala", g.crear_reserva(ana, sala, 20))
    equipo.disponible = False
    mostrar("Reserva fallida: equipo no disponible", g.crear_reserva(carlos, equipo, 4))
    equipo.disponible = True

    mostrar("Procesar sin confirmar (no permitido)", g.procesar(r1))
    mostrar("Confirmar reserva de Ana", g.confirmar(r1))
    mostrar("Procesar con IVA 19% y 10% de descuento", g.procesar(r1, 0.19, 0.10))
    mostrar("Cancelar reserva ya procesada (no permitido)", g.cancelar(r1))

    # ---- Sobrecarga y calculos inconsistentes ----
    mostrar("Costo asesoria sin argumentos (parametro faltante)", g.calcular(asesoria))
    mostrar("Costo asesoria nivel experto, 2h, descuento 150% (inconsistente)",
            g.calcular(asesoria, 2, 0.19, 1.5, nivel="experto"))
    mostrar("Costo asesoria nivel senior, 2h, solo base", g.calcular(asesoria, 2, nivel="senior"))
    mostrar("Costo asesoria experto, 2h, con IVA", g.calcular(asesoria, 2, 0.19, nivel="experto"))

    # ---- Flujo completo con cancelacion ----
    ok, r2 = g.crear_reserva(carlos, asesoria, 2, nivel="senior")
    mostrar("Reserva exitosa: Carlos en asesoria senior", (ok, r2))
    mostrar("Cancelar reserva pendiente", g.cancelar(r2))

    # ---- Resumen final ----
    print("\n=== RESUMEN ===")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print("  ", r)
    print(f"\nEl sistema termino sin interrupciones. Log: {RUTA_LOG}")


if __name__ == "__main__":
    main()

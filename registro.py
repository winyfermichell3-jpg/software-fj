"""Configuracion centralizada del archivo de logs (errores y eventos relevantes)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def configurar_logger(reiniciar=False):
    """Crea (o reutiliza) el logger del sistema. Si reiniciar=True, sobrescribe el archivo."""
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)   # crea la carpeta logs/ si no existe
    logger = logging.getLogger("software_fj")
    if logger.handlers:                                      # evita duplicar handlers
        return logger
    logger.setLevel(logging.DEBUG)
    manejador = logging.FileHandler(RUTA_LOG, mode="w" if reiniciar else "a", encoding="utf-8")
    manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                             "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(manejador)
    return logger


# Logger compartido por todos los modulos
log = logging.getLogger("software_fj")

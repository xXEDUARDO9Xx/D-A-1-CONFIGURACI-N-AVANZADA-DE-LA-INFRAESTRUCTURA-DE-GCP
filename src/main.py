import functions_framework
import logging
from google.cloud import logging as cloud_logging

# Inicializa el cliente oficial de Google Cloud Logging
# Esto permite que los logs se guarden como JSON estructurado automáticamente
try:
    log_client = cloud_logging.Client()
    log_client.setup_logging()
except Exception as e:
    # Respaldo por si se corre localmente sin credenciales de GCP
    logging.basicConfig(level=logging.INFO)

@functions_framework.cloud_event
def gcs_metadata_extractor(cloud_event):
    """
    Cloud Function desencadenada por un evento en Cloud Storage.
    Extrae metadatos del archivo subido y los registra en Cloud Logging.
    """
    logging.info(" Cloud Function activada por un nuevo evento de Cloud Storage.")
    
    try:
        # 1. Extraer los datos del evento enviado por Cloud Storage
        event_data = cloud_event.data
        
        if not event_data:
            raise ValueError("El payload del evento está vacío.")

        # 2. Extraer los metadatos requeridos por el reto
        file_name = event_data.get("name")
        file_size = event_data.get("size")
        content_type = event_data.get("contentType")
        bucket_name = event_data.get("bucket")
        time_created = event_data.get("timeCreated")

        # 3. Validación robusta: verificar que el nombre del archivo exista
        if not file_name:
            raise KeyError("No se encontró el nombre del archivo ('name') en los metadatos.")

        # 4. Registro detallado y estructurado para facilitar la depuración (Debugging)
        logging.info(f"ÉXITO: Archivo '{file_name}' detectado correctamente.")
        
        # Enviamos un diccionario para que Cloud Logging lo indexe como campos buscables
        log_payload = {
            "mensaje": "Metadatos extraídos con éxito",
            "estado": "PROCESADO",
            "bucket_origen": bucket_name,
            "archivo": {
                "nombre": file_name,
                "tamano_bytes": file_size,
                "tipo_contenido": content_type,
                "fecha_creacion": time_created
            }
        }
        logging.info(log_payload)

    except KeyError as ke:
        # Captura errores específicos si la estructura del evento cambia o falta el nombre
        logging.error({
            "estado": "ERROR",
            "tipo_error": "KeyError - Metadatos Faltantes",
            "detalles": str(ke)
        })
        
    except ValueError as ve:
        # Captura payloads vacíos o datos con formato incorrecto
        logging.warning({
            "estado": "ADVERTENCIA",
            "tipo_error": "ValueError - Validación fallida",
            "detalles": str(ve)
        })
        
    except Exception as e:
        # Manejo robusto global para evitar que la función muera silenciosamente
        logging.error({
            "estado": "FATAL",
            "tipo_error": "Error inesperado en la ejecución",
            "detalles": str(e)
        }, exc_info=True) # exc_info=True guarda el Traceback completo para depuración

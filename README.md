# Reto Dia 1: Configuracion avanzada de la infraestructura de GCP 

### 1 Creación y Configuración del Proyecto:
*** Proyecto Creado: My First Project
*** Habilitacion de las APIs:
  * Cloud Storage (`storage.googleapis.com`)
  * Cloud Functions (`cloudfunctions.googleapis.com`)
  * Cloud Pub/Sub (`pubsub.googleapis.com`)
  * Cloud Logging (`logging.googleapis.com`)
  * Cloud Build (`cloudbuild.googleapis.com`)
<img width="930" height="638" alt="image" src="https://github.com/user-attachments/assets/e8ab5419-a964-45a3-8ad8-0bf20a243a3a" />

*** Configuracion de roles y permisos a un usuario de prueba 
Creamos antes una cuenta de servicio, para poder darle los roles despues en el IAM.

<img width="921" height="331" alt="image" src="https://github.com/user-attachments/assets/b4a634da-6a3a-46ea-a0b4-814ec1956fff" />


Solamente se le dio el rol de creador de objetos de storage porque dados los privilegios minimos para trabajar serian solamente ese de poder crear, podria ser tambien el de lectura pero podria estar viendo objetos-archivos los cuales no deberia tener acceso, asi avitamos roles administrativos globales y mitigamos riesgos de seguridad.

<img width="1731" height="711" alt="image" src="https://github.com/user-attachments/assets/5861328d-20a4-4e31-b7cf-09389d600d7e" />

### 2 Almacenamiento 

*** Bucket principal:  bucket-retos-gcp
*** Control de Acceso: Configuración a nivel de bucket para aplicar de forma homogénea las políticas de IAM.
*** Reglas de Ciclo de Vida (Lifecycle): Se implementó una regla de retención automática para optimizar costos:
*** Condición: Archivos con antigüedad mayor a 30 días.
*** Acción: Eliminación automática (o transición a almacenamiento en frío *Nearline*, según se requiera).

<img width="774" height="797" alt="Captura de pantalla 2026-05-27 134437" src="https://github.com/user-attachments/assets/5d3d5d56-c1d9-4d7d-871c-29db80460cfa" />

Nuevamente se volvieron a dar permisos al usuario de prueba, para que pudiera crear archivos y tambien que los pudiera visualizar.

<img width="1793" height="914" alt="image" src="https://github.com/user-attachments/assets/c1210230-f147-4f1d-bb64-e9260d930831" />

*** Automatización con Cloud Functions

** Desarrollada en Python 3.14 utilizando el framework de funciones de segunda generación (`functions-framework`) conectado a Eventarc para reaccionar inmediatamente a los eventos de almacenamiento.

** Manejo de Errores: Implementación de bloques `try-except` para capturar payloads corruptos o excepciones inesperadas, evitando fallos silenciosos.

** Estructura de Logs: Los datos se extraen e indexan de forma estructurada en formato JSON directamente hacia Cloud Logging.

<img width="1916" height="857" alt="image" src="https://github.com/user-attachments/assets/a5564cc8-8b90-4a9f-9110-a37eb18affad" />

---

## Estructura del Código

* `src/main.py`: Lógica principal de la función encargada de procesar el evento de Cloud Storage y extraer los metadatos (nombre, tamaño, tipo).
* `src/requirements.txt`: Dependencias del entorno de ejecución de la función.
* `tests/test_main.py`: Set de pruebas unitarias utilizando `unittest.mock` para simular el comportamiento de eventos reales exitosos y flujos con errores de datos.

---




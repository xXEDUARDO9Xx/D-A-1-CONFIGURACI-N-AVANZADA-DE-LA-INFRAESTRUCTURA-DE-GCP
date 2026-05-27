# D-A-1-CONFIGURACI-N-AVANZADA-DE-LA-INFRAESTRUCTURA-DE-GCP

Este repositorio contiene la solución al **Día 1** de las pruebas técnicas de GCP. Se implementó una arquitectura segura y escalable que automatiza la captura de metadatos de archivos subidos a un almacenamiento en la nube utilizando tecnologías Serverless.

## 📌 Arquitectura del Flujo de Trabajo

El flujo diseñado sigue los principios de menor privilegio y automatización dirigida por eventos (*Event-Driven Architecture*):

`Usuario/Cliente` ➡️ Subida de archivo ➡️ `Cloud Storage (Bucket)` ➡️ Disparador de evento ➡️ `Cloud Functions (2nd Gen)` ➡️ Registro estructurado ➡️ `Cloud Logging`

---

## 🛠️ Componentes y Configuración Aplicada

### 1. Creacion y configuración del Proyecto
* **Proyecto Creado:** `Retos-dia-uno-gcp`
* **APIs Habilitadas:**
  * Cloud Storage (`storage.googleapis.com`)
  * Cloud Functions (`cloudfunctions.googleapis.com`)
  * Cloud Pub/Sub (`pubsub.googleapis.com`)
  * Cloud Logging (`logging.googleapis.com`)
  * Cloud Build (`cloudbuild.googleapis.com`)
* **Seguridad (Principio de Menor Privilegio):** 
  Se configuró una Cuenta de Servicio específica para aislamiento de producción controlada, asignándole de forma estricta únicamente el rol de **Creador de objetos de Storage** (`Storage Object Creator`), evitando roles administrativos globales para mitigar riesgos de seguridad.

### 2. Almacenamiento (Cloud Storage)
* **Bucket Principal:** Nombre único para la ingesta de archivos.
* **Control de Acceso:** Configuración **Uniforme** a nivel de bucket para aplicar de forma homogénea las políticas de IAM.
* **Reglas de Ciclo de Vida (Lifecycle):** Se implementó una regla de retención automática para optimizar costos:
  * **Condición:** Archivos con antigüedad mayor a 30 días.
  * **Acción:** Eliminación automática (o transición a almacenamiento en frío *Nearline*, según se requiera).

### 3. Automatización (Cloud Functions)
Desarrollada en **Python 3.10** utilizando el framework de funciones de segunda generación (`functions-framework`) conectado a Eventarc para reaccionar inmediatamente a los eventos de almacenamiento.
* **Manejo de Errores:** Implementación de bloques `try-except` para capturar payloads corruptos o excepciones inesperadas, evitando fallos silenciosos.
* **Estructura de Logs:** Los datos se extraen e indexan de forma estructurada en formato JSON directamente hacia **Cloud Logging**.

---

## 🚀 Estructura del Código

* `src/main.py`: Lógica principal de la función encargada de procesar el evento de Cloud Storage y extraer los metadatos (nombre, tamaño, tipo).
* `src/requirements.txt`: Dependencias del entorno de ejecución de la función.
* `tests/test_main.py`: Set de pruebas unitarias utilizando `unittest.mock` para simular el comportamiento de eventos reales exitosos y flujos con errores de datos.

---

## 📸 Evidencias de Funcionamiento

*(Nota para el evaluador: A continuación se presentan las capturas de pantalla tomadas directamente de la consola de GCP que validan el aprovisionamiento de la infraestructura).*

### Regla de Ciclo de Vida en el Bucket
![Ciclo de Vida](./evidencias/lifecycle.png) *(Reemplaza o sube tu captura aquí)*

### Configuración del Rol con Privilegios Mínimos (IAM)
![IAM Permisos](./evidencias/iam.png) *(Reemplaza o sube tu captura aquí)*

### Ejecución Exitosa y Registro en Cloud Logging
![Cloud Logging JSON](./evidencias/logs.png) *(Reemplaza o sube tu captura aquí)*

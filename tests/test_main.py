import unittest
from unittest.mock import MagicMock
from main import gcs_metadata_extractor

class TestCloudFunction(unittest.TestCase):

    def test_successful_metadata_extraction(self):
        """Prueba el flujo exitoso con un evento válido."""
        mock_event = MagicMock()
        mock_event.data = {
            "name": "reporte_mensual.csv",
            "size": "1024",
            "contentType": "text/csv",
            "bucket": "mi-bucket-prueba",
            "timeCreated": "2026-05-27T12:00:00Z"
        }
        # No debería levantar ninguna excepción
        try:
            gcs_metadata_extractor(mock_event)
        except Exception as e:
            self.fail(f"La función lanzó una excepción inesperada: {e}")

    def test_missing_filename_error_handling(self):
        """Prueba que la función maneje correctamente la falta de datos."""
        mock_event = MagicMock()
        mock_event.data = {
            "size": "1024"
            # Falta el campo 'name'
        }
        # Debería manejar el error internamente mediante los bloques try-except
        try:
            gcs_metadata_extractor(mock_event)
        except Exception as e:
            self.fail(f"El error no fue manejado internamente: {e}")

if __name__ == '__main__':
    unittest.main()

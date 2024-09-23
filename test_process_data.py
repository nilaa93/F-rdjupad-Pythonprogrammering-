import unittest
from process_data import fetch_data_from_api, process_data, update_database, create_connection, validate_data

class TestYourScript(unittest.TestCase):

    def test_fetch_data(self):
        data = fetch_data_from_api()
        self.assertIsNotNone(data)
        self.assertIn('title', data)
        self.assertIn('completed', data)

    def test_process_data(self):
        data = {'title': ' Test Title ', 'completed': True}
        processed_data = process_data(data)
        self.assertEqual(processed_data[0], 'test title')  # Kontrollera att titeln är formaterad korrekt
        self.assertEqual(processed_data[1], 1)  # Kontrollera att completed är int (1)

    def test_validate_data(self):
        self.assertTrue(validate_data('Valid Title', 1))
        self.assertFalse(validate_data('', 1))  # Ogiltig titel
        self.assertFalse(validate_data('Valid Title', 2))  # Ogiltigt värde för completed

    def test_update_database(self):
        processed_data = ('Test Title', 1)  # Datan som ska uppdateras
        update_database(processed_data)  # Anropa funktionen för att uppdatera databasen
        
        # Kontrollerar att datan har lagts till i databasen
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos WHERE title = ?', (processed_data[0],))
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result)  # Kontrollera att resultatet inte är None
        self.assertEqual(result[1], 'Test Title')  # Kontrollera att titeln är korrekt
        self.assertEqual(result[2], 1)  # Kontrollera att completed är True (1 i SQL)

if __name__ == '__main__':
    unittest.main()



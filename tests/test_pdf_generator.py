import sys
import os
sys.path.append(os.getcwd())

from src.pdf.simple_generator import generate_pdf
import unittest
from io import BytesIO

class TestPDFGenerator(unittest.TestCase):
    def test_generate_pdf_basic(self):
        data = {
            "test_key": "test_value",
            "test_list": ["item1", "item2"],
            "test_dict": {"nested_key": "nested_value"}
        }
        title = "Test PDF"
        buffer = generate_pdf(data, title)
        
        self.assertIsInstance(buffer, BytesIO)
        self.assertTrue(buffer.getbuffer().nbytes > 0)
        
        # Verify it starts with PDF signature %PDF
        buffer.seek(0)
        content = buffer.read(4)
        self.assertEqual(content, b'%PDF')

if __name__ == '__main__':
    unittest.main()

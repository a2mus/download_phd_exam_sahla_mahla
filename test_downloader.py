import unittest
from unittest.mock import patch, MagicMock
from download_exams import PhDExamDownloader
import os

class TestPhDExamDownloader(unittest.TestCase):
    
    def setUp(self):
        self.base_url = "https://lmd.sahla-dz.com/sujets-concours-doctorat-informatique/"
        self.destination_folder = "test_downloads"
        self.downloader = PhDExamDownloader(self.base_url, self.destination_folder)
    
    @patch('requests.Session')
    def test_get_exam_page_links(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <a href="/sujets-des-concours-doctorat-2023">Sujets 2023</a>
                <a href="https://lmd.sahla-dz.com/other-page">Other Page</a>
                <a href="/doctorat-informatique-page">Doctorat Info</a>
            </body>
        </html>
        '''
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        links = self.downloader.get_exam_page_links()
        
        # Assertions
        self.assertEqual(len(links), 2)  # Should find 2 relevant links
        self.assertTrue(any("sujets-des-concours-doctorat-2023" in link for link in links))
        self.assertTrue(any("doctorat-informatique-page" in link for link in links))
    
    @patch('requests.Session')
    def test_extract_pdf_url_from_iframe(self, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '''
        <html>
            <body>
                <iframe data-src="//docs.google.com/gview?embedded=true&amp;url=https://lmd.sahla-dz.com/oackoafa/2023/05/example.pdf"></iframe>
            </body>
        </html>
        '''
        mock_session.return_value.get.return_value = mock_response
        
        # Call the method
        pdf_url = self.downloader.extract_pdf_url_from_iframe("https://lmd.sahla-dz.com/test-page")
        
        # Assertions
        self.assertEqual(pdf_url, "https://lmd.sahla-dz.com/oackoafa/2023/05/example.pdf")
    
    @patch('requests.Session')
    @patch('os.path.join')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_download_pdf(self, mock_open, mock_join, mock_session):
        # Mock the response
        mock_response = MagicMock()
        mock_response.headers = {'Content-Type': 'application/pdf'}
        mock_response.iter_content.return_value = [b'PDF content']
        mock_session.return_value.get.return_value = mock_response
        
        # Mock os.path.join to return a predictable path
        mock_join.return_value = os.path.join(self.destination_folder, "example.pdf")
        
        # Call the method
        result = self.downloader.download_pdf(
            "https://lmd.sahla-dz.com/oackoafa/2023/05/example.pdf",
            "https://lmd.sahla-dz.com/test-page"
        )
        
        # Assertions
        self.assertTrue(result)  # Download should be successful
        mock_open.assert_called_once_with(os.path.join(self.destination_folder, "example.pdf"), 'wb')
        mock_open().write.assert_called_once_with(b'PDF content')

if __name__ == '__main__':
    unittest.main()
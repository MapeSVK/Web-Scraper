import unittest
import web_scraper
import fnmatch
import os

class TestWebScraper(unittest.TestCase):

    # check if removeAlreadyExistedFile removes the file from directory
    def test_removeAlreadyExistedFile(self):
        name_of_the_file = 'file.md'
        number_of_files_before = len(fnmatch.filter(os.listdir("/Users/Mape/Desktop/my_web_scraper_folder/my_web_scraper_project_folder"), name_of_the_file))
        web_scraper.removeAlreadyExistedFile()
        number_of_files_after = len(fnmatch.filter(os.listdir("/Users/Mape/Desktop/my_web_scraper_folder/my_web_scraper_project_folder"), name_of_the_file))
        self.assertTrue(2>number_of_files_before >= 0)
        self.assertTrue(number_of_files_after == 0)
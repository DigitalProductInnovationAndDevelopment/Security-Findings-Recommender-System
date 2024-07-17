import unittest
import json
from unittest.mock import patch, mock_open

class TestLicenseCompliance(unittest.TestCase):

    def setUp(self):
        self.mock_dependency_licenses = '''
        [
          {
            "License": "BSD License",
            "Name": "Jinja2",
            "Version": "3.1.4"
          },
          {
            "License": "MIT License",
            "Name": "Mako",
            "Version": "1.3.5"
          },
          {
            "License": "BSD License",
            "Name": "MarkupSafe",
            "Version": "2.1.5"
          },
          {
            "License": "GPL-3.0",
            "Name": "SomeRestrictedPackage",
            "Version": "1.0.0"
          }
        ]
        '''

    def test_parse_dependency_licenses(self):
        with patch('builtins.open', mock_open(read_data=self.mock_dependency_licenses)):
            with open('dependency_licenses.json', 'r') as f:
                data = json.load(f)
                self.assertEqual(len(data), 4)
                self.assertEqual(data[0]['Name'], 'Jinja2')
                self.assertEqual(data[1]['License'], 'MIT License')

    def test_compare_dependency_licenses(self):
        permitted_licenses = ["MIT", "MIT License", "Apache-2.0", "BSD", "BSD License"]
        
        with patch('builtins.open', mock_open(read_data=self.mock_dependency_licenses)):
            with open('dependency_licenses.json', 'r') as f:
                data = json.load(f)
                
                for package in data:
                    license = package['License']
                    package_name = package['Name']
                    with self.subTest(package=package_name):
                        if license not in permitted_licenses:
                            print(f"Error: Package {package_name} has an unrecognized license: {license}")
                        self.assertIn(license, permitted_licenses, f"Package {package_name} has an unrecognized license: {license}")

if __name__ == '__main__':
    unittest.main()

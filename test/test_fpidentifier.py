import unittest
import os
from src.main import main
from utils import check_file_exists, validate_fasta_format

class TestFPIdentifier(unittest.TestCase):

    def setUp(self):
        # Set up the paths for input and output files for the test
        self.input_file = "tests/test_data.fasta"
        self.output_dir = "tests/output/"
        self.output_file = os.path.join(self.output_dir, "hmmer_results.txt")

        # Ensure the output directory is clean before each test
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def test_input_file_exists(self):
        # Test that the input file exists
        self.assertTrue(check_file_exists(self.input_file))

    def test_validate_fasta_format(self):
        # Test that the input file is in the correct FASTA format
        self.assertTrue(validate_fasta_format(self.input_file))

    def test_main_pipeline(self):
        # Test the entire FPIdentifier pipeline
        main()  # You can add argument parsing here for main()
        self.assertTrue(os.path.exists(self.output_file))  # Ensure output file is created

    def tearDown(self):
        # Clean up after the test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == '__main__':
    unittest.main()

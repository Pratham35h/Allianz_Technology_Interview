import pytest
import os
import shutil
from unittest.mock import patch
import zipfile
from Transform_and_Load import rename_and_zip_files  # Import the function to test

@pytest.fixture
def setup_raw_directory():
    raw_dir = "raw/hockey_pages"  # Correct directory path here
    os.makedirs(raw_dir, exist_ok=True)
    
    # Create HTML files with the table structure as requested
    html_data = '''
    <html>
        <body>
            <table class="table">
                <tr>
                    <th>Team Name</th>
                    <th>Year</th>
                    <th>Wins</th>
                    <th>Losses</th>
                    <th>OT Losses</th>
                    <th>Win %</th>
                    <th>Goals For (GF)</th>
                    <th>Goals Against (GA)</th>
                    <th>+ / -</th>
                </tr>
                <tr class="team">
                    <td class="name">Boston Bruins</td>
                    <td class="year">1990</td>
                    <td class="wins">44</td>
                    <td class="losses">24</td>
                    <td class="ot-losses"></td>
                    <td class="pct text-success">0.55</td>
                    <td class="gf">299</td>
                    <td class="ga">264</td>
                    <td class="diff text-success">35</td>
                </tr>
            </table>
        </body>
    </html>
    '''
    
    for i in range(1, 4):
        with open(os.path.join(raw_dir, f"file_{i}.html"), 'w') as f:
            f.write(html_data)
    
    yield raw_dir

    shutil.rmtree(raw_dir)

def test_rename_and_zip_files(setup_raw_directory):
    raw_dir = setup_raw_directory
    zip_filename = "test_files.zip"
    zip_path = os.path.join("transformed", zip_filename)
    
    if not os.path.exists("transformed"):  # Make sure the transformed directory exists
        os.makedirs("transformed")
    
    if os.path.exists(zip_path):
        os.remove(zip_path)
    
    rename_and_zip_files(raw_dir, zip_filename)

    assert os.path.exists(zip_path), "Zip file was not created"
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        file_names = zipf.namelist()
        assert len(file_names) == 3, "Not all files were zipped"
        assert file_names[0] == '1.html', "Files were not renamed correctly"
    
    os.remove(zip_path)

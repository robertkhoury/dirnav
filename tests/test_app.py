import json
import os
import pytest
import shutil
import tempfile

from app import app

ROOT_PATH = os.path.join(app.root_path, "user_path")
TMP_DIR_PATH = os.path.join(ROOT_PATH, "tmp_test")
TMP_FILE_PATH = os.path.join(TMP_DIR_PATH, "hello.txt")

# NOTE - You will need to update the OWNER_ID to match your system's user id for the tests to pass
OWNER_ID = 504
CONTENT = "content"


def teardown_function(function):
	if os.path.exists(TMP_DIR_PATH):
		shutil.rmtree(TMP_DIR_PATH)

def test_empty_root():
	response = app.test_client().get('/')
	data = json.loads(response.data)
	empty_response = {
		"name": "/",
		"object_type": "folder",
		"folder_contents": []
	}
	assert empty_response == data

def test_folder():
	os.mkdir(TMP_DIR_PATH)
	f = open(TMP_FILE_PATH, "w")
	f.write(CONTENT)
	f.close()
	response = app.test_client().get('/tmp_test')
	data = json.loads(response.data)
	expected_response = {
	  "folder_contents": [
	    {
	      "owner_id": OWNER_ID,
	      "size": "7B",
	      "object_type": "file",
	      "name": "hello.txt",
	      "permissions": 33188
	    }
	  ],
	  "object_type": "folder",
	  "name": "tmp_test"
	}
	assert data == expected_response

def test_file():
	os.mkdir(TMP_DIR_PATH)
	f = open(TMP_FILE_PATH, "w")
	f.write(CONTENT)
	f.close()
	response = app.test_client().get('/tmp_test/hello.txt')
	data = json.loads(response.data)
	expected_response = {
	  "name": "hello.txt",
	  "object_type": "file",
	  "owner_id": OWNER_ID,
	  "permissions": 33188,
	  "file_text": "content",
	  "size": "7B"
	}
	assert data == expected_response

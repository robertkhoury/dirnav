# dirnav
## Setup
First, specify your USER_PATH to be the absolute path (starting with `~`) of the directory you want to explore.
```
export USER_PATH=your_path_here
```
This path will be treated as the root path within the app.

Next, start the app. You will need to have Docker installed and running.
```
docker-compose up
```
If you want to set a different path, kill the app, update USER_PATH, and start the app again.

## API
The app will run on http://localhost:5000/. You can use the API either in a browser, or by curling from the command line:
```
curl http://localhost:5000/
```
`GET /` will return the contents of your configured directory. This will return a Folder object, with the following attributes:
```
{
  "folder_contents": [File/Folder], # list of File and Folder objects inside this Folder, omitting their contents
  "object_type": String, # will always be "folder"
  "name": String # folder name
}
```
`GET /<subpath>` will return the contents of the file or directory specified by the subpath. 
If <subpath>points to a directory, it will return a Folder object as outlined above. 
  If <subpath> points to a file, it will return a File object, with the following attributes:
```
{
  "name": String,
  "object_type": String # will always be "file",
  "owner_id": Int,
  "permissions": Int # octal representation,
  "file_text": String # contents of the file,
  "size": String # represented as <number of bytes>B"
}
  ```
If the app doesn't find anything at <subpath>, it will return an error.

## Run the tests
You'll need to update the OWNER_ID in `tests/test_app.py` for the tests to pass. 
`python -m pytest`

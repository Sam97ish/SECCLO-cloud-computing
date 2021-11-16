 
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Photo, Album
import json
from bson.objectid import ObjectId
import os
import urllib
import base64
import codecs
import string

app = Flask(__name__)

# database configs
app.config['MONGODB_SETTINGS'] = {
    # set the correct parameters here as required, some examples are give below
    'host': 'mongodb://mongo:27017/flask-database'
    #'host':'mongodb://localhost/<name of db>'
}
db = initialize_db(app)

## ------
# Helper functions to be used if required
# -------
def str_list_to_objectid(str_list):
    return list(
        map(
            lambda str_item: ObjectId(str_item),
            str_list
        )
    )

def object_list_as_id_list(obj_list):
    return list(
        map(
            lambda obj: str(obj.id),
            obj_list
        )
    )


# ----------
# PHOTO APIs
# ----------
# These methods are a starting point, implement all routes as defined in the specifications given in A+

@app.route('/listPhoto', methods=['POST'])
def add_photo():
    posted_image = request.files["file"]
    posted_data = request.form

    
    #print(posted_data)
    # Check for default album
    def_albums = Album.objects(name='Default').first()
    if not def_albums: 
        def_albums = Album(name='Default').save()
    photo = Photo(**posted_data)
    if(posted_data.get("tags")):
        tags = json.loads(posted_data["tags"])
        photo.tags = tags
    if(posted_data.get("albums")):
        albums = str_list_to_objectid(json.loads(posted_data["albums"]))
        photo.albums = albums

    photo.albums.append(def_albums)
    photo.image_file.replace(posted_image)
    photo.save()
    output = {'message': "Photo successfully created", 'id': str(photo.id)}
    status_code = 201
    return output, status_code

@app.route('/listPhoto/<photo_id>', methods=['GET', 'PUT', 'DELETE'])
def get_photo_by_id(photo_id):
    if request.method == "GET":
        photo = Photo.objects(id=photo_id).first()
        if photo:
            ## Photos should be encoded with base64 and decoded using UTF-8 in all GET requests with an image before sending the image as shown below
            base64_data = codecs.encode(photo.image_file.read(), 'base64')
            image = base64_data.decode('utf-8')
            ##########
            output =  {"name": photo.name, "tags": photo.tags, "location": photo.location, "albums": photo.albums, "file": image}
            status_code = 200
            return output, status_code
    elif request.method == "PUT":
        photo = Photo.objects(id=photo_id).first()
        body = request.get_json()
        keys = body.keys()
        if body and keys:
            if "albums" in keys:
                body["albums"] = [ObjectId(element) for element in body["albums"]]
            photo.update(**body)
            output = {'message': "Photo successfully updated", 'id': str(photo.id)}
            status_code = 200
            return output, status_code
    elif request.method == "DELETE":
       photo = Photo.objects(id=photo_id).first()
       photo.delete()
       output = {'message': "Photo successfully deleted", 'id': str(photo.id)}
       status_code = 200
       return output, status_code

@app.route('/listPhotos', methods=['GET'])
def get_photos():
    tag = request.args.get('tag')
    albumName = request.args.get('albumName')

    if albumName is not None:
        album = Album.objects(name=albumName).first()
        photo_objects = Photo.objects(albums=album.id)
    elif tag is not None:
        photo_objects = Photo.objects(tags=tag)
    else:
        album = Album.objects(name='Default').first()
        photo_objects = Photo.objects(albums=album.id)
    photos = []
    for photo in photo_objects:
        base64_data = codecs.encode(photo.image_file.read(), 'base64')
        image = base64_data.decode('utf-8')
        photos.append({'name': photo.name, 'location': photo.location, 'file': image})
    return jsonify(photos), 200

# ----------
# ALBUM APIs
# ----------
# Complete the album APIs similarly as per the instructions provided in A+
@app.route('/listAlbum', methods=['POST'])
def add_album():
    body = request.form
    album = Album(**body).save()
    print(album)
    output = {'message': "Album successfully created", 'id': str(album.id)}
    status_code = 201
    return output, status_code

@app.route('/listAlbum/<album_id>', methods=['GET', 'PUT', 'DELETE'])
def get_album(album_id):
    if request.method == "GET":
        album = Album.objects(id=album_id)[0]
        if album:
            output =  {"id": str(album.id),"name": album.name}
            status_code = 200
            return output, status_code
    elif request.method == "PUT":
        album = Album.objects(id=album_id).first()
        body = request.get_json()
        keys = body.keys()
        if body and keys:
            Album.objects(id=album_id).update(**body)
            output = {'message': "Album successfully updated", 'id': str(album.id)}
            status_code = 200
            return output, status_code
    elif request.method == "DELETE":
       album = Album.objects(id=album_id)[0]
       album.delete()
       output = {'message': "Album successfully deleted", 'id': str(album.id)}
       status_code = 200
       return output, status_code

# Only for local testing without docker
#app.run() # FLASK_APP=app.py FLASK_ENV=development flask run

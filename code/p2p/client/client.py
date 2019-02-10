import json
import os
import urllib.parse
import urllib.error
import urllib.request
from collections import defaultdict
from uuid import uuid1
from flask import Flask, flash, request, url_for, send_from_directory
from werkzeug import exceptions, utils
from util.torrent import Torrent
from flask_cors import CORS

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'local_file'
app.config['SEEDER'] = str(uuid1())
app.config['TRACKER'] = 'http://10.21.72.153:5000'   # 需要修改

seeders = defaultdict(dict)

CORS(app, supports_credentials=True, resources=r'/*')


# solve upload event
@app.route('/api/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash("Can't Get File")
        return json.dumps({'success': False})
    content = request.files['file']
    print(content)
    # if user does not select file, browser also
    # submit an empty part without filename
    if content.filename == '':
        flash("Can't Get File")
        return json.dumps({'success': False})

    # get the file from local
    name_file = utils.secure_filename(content.filename)

    # read content from file
    data = content.read()
    t = Torrent.create(name_file, data)

    # save the content in the folder
    content.stream.seek(0)
    content.save(os.path.join(app.config['UPLOAD_FOLDER'], name_file))

    # construct file name and dump to json
    t.dump(os.path.join(app.config['UPLOAD_FOLDER'], t.encryption))

    # notify the tracker
    try:
        notify = urllib.request.Request(urllib.parse.urljoin(app.config['TRACKER'], '/api/report'))
        notify.add_header('Content-Type', 'application/json; charset=utf-8')
        information = {
            'uuid': app.config['SEEDER'],
            'torrent': t.encryption,
            'slices': t.slice_encryption,
            'name': t.name,

            # construct urls
            'torrent_url': urllib.parse.urljoin(request.host_url, url_for('download', filename=t.encryption)),
            'file_url': urllib.parse.urljoin(request.host_url, url_for('download', filename=t.name))
        }

        json_data = json.dumps(information).encode('utf-8')  # needs to be bytes
        notify.add_header('Content-Length', len(json_data))
        urllib.request.urlopen(notify, json_data)

        # save the information about torrents
        _data = information
        print(_data)
        print(json_data)
        try:
            seeders[_data['torrent']][_data['uuid']] = _data
            print("Request succeeded.")
        except exceptions.BadRequestKeyError:
            print("Request failed.")

    except urllib.error.HTTPError:
        pass
    return json.dumps({'success': True})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)

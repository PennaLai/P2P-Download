import json
from flask import Flask, request
from werkzeug import exceptions
from collections import defaultdict
from util import crossdomain
from os.path import isfile

app = Flask(__name__)

# define the torrent-data dictionaries
# clients make queries according to the dictionaries
torrent_user_dict = defaultdict(list)
torrent_slice_dict = dict()
torrent_name_dict = dict()
torrent_urls_dict = defaultdict(list)


def init():
    """
    Read all torrent data from local tracker data
    """
    global torrent_user_dict, torrent_slice_dict, torrent_name_dict, torrent_urls_dict
    if isfile('tracker_data.txt'):
        with open('tracker_data.txt', 'r') as fp:
            line = fp.readline()
            if line:
                torrent_user_dict = json.loads(line)
            line = fp.readline()
            if line:
                torrent_slice_dict = json.loads(line)
            line = fp.readline()
            if line:
                torrent_name_dict = json.loads(line)
            line = fp.readline()
            if line:
                torrent_urls_dict = json.loads(line)


@app.route('/api/report', methods=['POST'])
@crossdomain(origin='*')
def report():
    """
    client report its information to tracker every time it uploads a file
    :return: success json
    """
    global torrent_user_dict, torrent_slice_dict, torrent_name_dict, torrent_urls_dict
    request_json = request.json
    try:
        info_data = {'uuid': request_json['uuid'],
                     'torrent_url': request_json['torrent_url'],
                     'file_url': request_json['file_url']}
        request_torrent = request_json['torrent']
        if request_torrent in torrent_user_dict.keys():
            if info_data in torrent_user_dict[request_torrent]:
                print('This file has been uploaded.')
                return json.dumps({'success': True})
            torrent_user_dict[request_torrent] += [info_data]
            torrent_urls_dict[request_torrent] += [request_json['file_url']]
        else:
            torrent_user_dict[request_torrent] = [info_data]
            torrent_slice_dict[request_torrent] = request_json['slices']
            torrent_name_dict[request_torrent] = request_json['name']
            torrent_urls_dict[request_torrent] = [request_json['file_url']]
        print('Report succeeded.')
        # store the data
        with open('tracker_data.txt', 'w') as fp:
            fp.write(json.dumps(torrent_user_dict) + '\n')
            fp.write(json.dumps(torrent_slice_dict) + '\n')
            fp.write(json.dumps(torrent_name_dict) + '\n')
            fp.write(json.dumps(torrent_urls_dict) + '\n')
    except exceptions.BadRequestKeyError:
        print('Bad request. Report failed.')
    return json.dumps({'success': True})


@app.route('/api/query')
@crossdomain(origin='*')
def query():
    """
    client makes a query with an argument of torrent id
    :return
    example: {name:, info:[{uuid:, torrent_url:, file_url:}, {}], slices:, download_urls:[]}
    """
    global torrent_user_dict, torrent_slice_dict, torrent_name_dict
    arguments = request.args
    if isfile('tracker_data.txt'):
        with open('tracker_data.txt', 'r') as fp:
            line = fp.readline()
            if line:
                torrent_user_dict = json.loads(line)
            line = fp.readline()
            if line:
                torrent_slice_dict = json.loads(line)
            line = fp.readline()
            if line:
                torrent_name_dict = json.loads(line)
    try:
        data = dict()
        request_torrent = arguments['torrent']
        data['slices'] = torrent_slice_dict[request_torrent]
        data['name'] = torrent_name_dict[request_torrent]
        data['info'] = torrent_user_dict[request_torrent]
        data['download_urls'] = torrent_urls_dict[request_torrent]
        print("Query succeeded.")
        return json.dumps(data)
    except KeyError:
        return json.dumps([])


if __name__ == '__main__':
    init()
    app.run(debug=True, host="0.0.0.0")

import socket
import select
from flask import Flask, jsonify

app = Flask(__name__)

def send_udp_data_and_receive_response(ip, port, header, data):
	byte_message = bytearray(bytes(data))
	byte_header = bytearray.fromhex('FFFFFFFF' + header)

	data = byte_header + byte_message

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(data, (ip, port))
	print('Sent data!')

	data = sock.recv(1400).decode(encoding="UTF-8", errors='replace')

	return data

@app.route('/get_info/<ip>/<port>')
def get_server_info(ip, port):
	with app.test_request_context('/'):
		print('Getting server info for: %s:%s' % (ip, port))

		data = send_udp_data_and_receive_response(ip, int(port), '54', 'Source Engine Query')
		# Ignore padding (4 bytes) + header (1 byte) + protocol (1 byte)
		info_array = data[6:].split('\x00')

		server_name = info_array[0]
		server_map = info_array[1]
		server_gamemode = info_array[3]

		print('Server Name: %s' % server_name)
		print('Server Map: %s' % server_map)
		print('Server Gamemode: %s' % server_gamemode)

		return jsonify({
			'server_name': server_name,
			'server_map': server_map,
			'server_gamemode': server_gamemode
		})

@app.route('/get_players/<ip>/<port>')
def get_server_players(ip, port):
	with app.test_request_context('/'):
		print('Getting server players for: %s:%s' % (ip, port))

		# Get challenge
		data = send_udp_data_and_receive_response(ip, int(port), '55', '\xFF\xFF\xFF\xFF')

		# After a player's name, we have the score (4 bytes) + duration (4 bytes) + index (1 bytes)
		names = []
		name = ''

		# Ignore headers
		data = data[7:]

		index = 0
		while index < len(data):
			character = data[index]
			if character != '\x00':
				name += str(character)
				index += 1
			else:
				names.append(name)
				name = ''
				index += 10

		print(names)
		print(len(names))
		return jsonify(names)
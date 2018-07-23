function getServerInfo(ip, port)
	http.Fetch( "http://127.0.0.1:5000/get_info/"..ip.."/"..port,
		function( body, len, headers, code )
			print("Server info:")
			print(body)
			return body
		end,
		function( error )
		end
	)

end

function getServerPlayers(ip, port)
	http.Fetch( "http://127.0.0.1:5000/get_players/"..ip.."/"..port,
		function( body, len, headers, code )
			print("Server players:")
			print(body)
			return body
		end,
		function( error )
		end
	)
end

getServerInfo("208.103.169.14", 27015)
getServerPlayers("208.103.169.14", 27015)
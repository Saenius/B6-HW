from bottle import route
from bottle import run
from bottle import HTTPError

import albums_search

@route('/albums/<artist>')
def albums(artist):
	albums_list = albums_search.find(artist)
	if not albums_list:
		message = 'Альбомов {} не найдено'.format(artist)
		result = HTTPError(404, message)
	else:
		album_names = [album.album for album in albums_list]
		result = 'Нашлось {} альбома(-ов) {}\n'.format(len(album_names), artist)
		result += '\n'.join(album_names)
	return result

@route("/albums", method="POST")
def post_album():
	new_album = album_search.Album(
		year = request.forms.get('year'),
		artist = request.forms.get('artist'),
		genre = request.forms.get('genre'),
		album = request.forms.get('album')
		)
	try:
		int_year = int(new_album.year)
		if int_year < 1800:
			return HTTPError(400, 'В этом году не могло быть альбомов')
	except Exception:
		return HTTPError(400, 'Некорректное значение для года!')
	if new_album.artist is '' or new_album.album is '' or new_album.artist is None or new_album.album is None:
		raise HTTPError(400, 'Это поле не может быть пустым')

	try:
		album_search.add_album(new_album)
		return 'Альбом успешно сохранен'
	except album_search.AlbumDublicationError:
		return HTTPError(409, 'Такой альбом уже есть!')
		
	
if __name__ == "__main__":
	run(host="localhost", port=8080, debug=True)
server:
	clear
	python TP1v1server.py SLIDES.ppt saida.ppt 127.0.0.1 51515 passivo
client:
	clear
	python TP1v1client.py SLIDES.ppt sa.ppt 127.0.0.1 51515 ativo
ativo:
	clear
	python TP1v4emulador.py Circuitos.pdf sa.pdf 127.0.0.1 52000 ativo

passivo:
	clear
	python TP1v4emulador.py Circuitos.pdf s.pdf 127.0.0.1 52000 passivo

##docker_zad1
Narzędzia: Python: 3.10, Flask: 2.x, Docker: 24.x

Aplikacja jest na porcie 5001
Komendy:

docker pull hubkap77/weather-app:latest

docker run -d --name weather-app \
  -e WEATHER_API_KEY=\
  -e AUTHOR="Hubert Kaproń" \
  -p 5001:5001 hubkap77/weather-app:latest

docker logs weather-app
lub docker desktop

http://localhost:5001

docker inspect weather-app

do sprawdzenia warstw


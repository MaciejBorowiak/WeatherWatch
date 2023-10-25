# WeatherWatch
Aplikacja służąca do sprawdzania aktualnej prognozy pogody na następne 12 godzin w dowolnym mieście na świecie

## Jak korzystać? ##
Programu można używać na dwa sposoby:

**1. Uruchomienie za pomocą kursora tak jak każdej innej standardowej aplikacji - wtedy uruchomi się wersja okienkowa widoczna na zrzucie ekranu**

<p align="center">
  <img src="https://github.com/MaciejBorowiak/WeatherWatch/blob/main/readme_img/WeatherWatch1.png"/>
</p>

**2. Uruchomienie poprzez wiesz polecenia za pomocą komendy python main.py -phonemode, która wyśle wiadomość SMS na wybrany przez nas numer telefonu**

<p align="center">
  <img src="https://github.com/MaciejBorowiak/WeatherWatch/blob/main/readme_img/WeatherWatch4.png"/>
</p>

Możemy wykorzystać tą opcję, żeby np. za pomocą narzędzia **PythonAnywhere** otrzymywać prognozę pogody na następne 12 godzin, codziennie o 7 rano

## Konfiguracja ##
W celu skonfigurowania aplikacji pod nasze potrzeby musimy uzupełnić przede wszystkim plik ze zmiennymi środowiskowymi (.env):

```
API_KEY=YOUR_API_KEY
ACCOUNT_SID=YOUR_ACCOUNT_SID
AUTH_TOKEN=YOUR_AUTH_TOKEN
TWILIO_NUMBER=YOUR_TWILIO_NUMBER
```
**API_KEY -** Klucz API naszego konta OpenWeather <br />
**ACCOUNT_SID -** Klucz identyfikacyjny naszego konta Twilio <br />
**AUTH_TOKEN -** Token autoryzacyjny naszego konta Twilio <br />
**TWILIO_NUMBER -** Numer naszego wirtualnego telefonu utworzonego w Twilio IP, z którego będą wysyłane SMS-y <br /><br />

Po uzupełnieniu powyższego pliku uruchamiamy aplikacje w trybie okienkowym i uzupełniamy pola interesującą nas miejscowością oraz numerem telefonu w formacie **+48123456789**, na który chcemy wysyłać powiadomienia, a następnie zatwierdzamy zmiany przyciskami

<p align="center">
  <img src="https://github.com/MaciejBorowiak/WeatherWatch/blob/main/readme_img/WeatherWatch5.png"/>
</p>

**Alternatywnie** możemy zamiast uruchamiania aplikacji okienkowej, otworzyć plik **data.json** i uzupełnić tam dane w identyczny sposób:

```json
{"phone": "+48123456789", "city": "Warszawa"}
```
**UWAGA! Numer na który chcemy wysyłać powiadomienie również musi być dodany jako zweryfikowany na naszym koncie Twilio API**

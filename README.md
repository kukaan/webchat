# WebChat
## Toiminnallisuudet alustavassa toteutusjärjestyksessä
1. Käyttäjä voi luoda itselleen salasanallisen tunnuksen ja kirjautua sillä.
1. Käyttäjä voi luoda julkisia viestiketjuja ja lähettää niihin viestejä.
1. Käyttäjä voi muokata viestiä tai poistaa sen (piilottaa kaikilta paitsi ylläpitäjiltä).
1. Käyttäjä voi olla peruskäyttäjän sijaan ylläpitäjä.
1. Viestiketjut ovat eri keskustelualueiden alla.
1. Käyttäjä voi hakea viestejä, ketjuja tai alueita.
1. Viestiketjut tai keskustelualueet voivat olla salaisia, jolloin niihin on pääsy vain tietyillä peruskäyttäjillä ja kaikilla ylläpitäjillä.

## Pohdintaa ja kysymys
Tietokantatauluja tulee olemaan varmaankin Kayttaja, Viesti, Ketju ja Alue, mutta tässähän ei ole vielä yhtäkään monen suhdetta moneen. Pitäisikö tämän puutteen korjaamiseksi muuttaa rakennetta esimerkiksi niin, että Alueen sijaan on Aihetunniste, joka voi liittyä useaan Ketjuun, joista jokainen voi liittyä useaan Aihetunnisteeseen?

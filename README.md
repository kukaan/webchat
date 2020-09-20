# WebChat

### A simple web-based chat/forum
- Create users, message threads and messages to interact with other users online.

---

## P2
### Nykytila
- Käyttäjätunnukset sekä yksinkertaiset viestiketjut ja profiilit ovat toiminnassa. Nykyinen index-sivun ratkaisu näyttää kaikkien ketjujen (ja muutoksessa ketjuttomaksi jääneet) viestit on väliaikainen.
- Viestin tai viestiketjun luoja voi poistaa tekeleensä näkyvistä, mutta ne ovat silti admin-käyttäjien nähtävissä. Adminit voivat myös yksinoikeudella katsoa muiden käyttäjätietoja profiileista, mutta toistaiseksi vain osoiterivin kautta. Admin-oikeudet voi antaa vain PostgreSQL-tulkin kautta.

### Heroku
- https://cryptic-dusk-65765.herokuapp.com/
- Admin-ominaisuudet käytössä seuraavalla tunnuksella ja salasanalla: a / aaaaaaaa

### Tulevaa
- Aion lisätä vielä uutena tietokantatauluna ainakin keskustelualueet. Viestien, ketjujen ja alueiden sekä käyttäjien muokkaaminen täysin tyylipuhtaasti saattaa osoittautua hieman monimutkaiseksi riippuvuussuhteiden myötä. Hakutoiminnon toteutan varmaan helpompana ensin.
- Alueiden tai ketjujen tekeminen salaiseksi/yksityiseksi lienee paras toteuttaa liittämällä niihin kutsuttuihin/lisättyihin käyttäjiin liittyvä liitostaulu. Samalla tarvitaan toiminto käyttäjien lisäämiseksi ainakin ketjun/alueen luojan käyttöön.
- Nykyinen ulkonäky on karu, joten jokin minimalistinen ulkoasukirjasto olisi kiva saada mukaan.

---

## P1
### Toiminnallisuudet alustavassa toteutusjärjestyksessä
1. Käyttäjä voi luoda itselleen salasanallisen tunnuksen ja kirjautua sillä.
1. Käyttäjä voi luoda julkisia viestiketjuja ja lähettää niihin viestejä.
1. Käyttäjä voi muokata viestiä tai poistaa sen (piilottaa kaikilta paitsi ylläpitäjiltä).
1. Käyttäjä voi olla peruskäyttäjän sijaan ylläpitäjä.
1. Viestiketjut ovat eri keskustelualueiden alla.
1. Käyttäjä voi hakea viestejä, ketjuja tai alueita.
1. Viestiketjut tai keskustelualueet voivat olla salaisia, jolloin niihin on pääsy vain tietyillä peruskäyttäjillä ja kaikilla ylläpitäjillä.

### Pohdintaa ja kysymys
Tietokantatauluja tulee olemaan varmaankin Kayttaja, Viesti, Ketju ja Alue, mutta tässähän ei ole vielä yhtäkään monen suhdetta moneen. Pitäisikö tämän puutteen korjaamiseksi muuttaa rakennetta esimerkiksi niin, että Alueen sijaan on Aihetunniste, joka voi liittyä useaan Ketjuun, joista jokainen voi liittyä useaan Aihetunnisteeseen?

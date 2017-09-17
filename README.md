# flowers_black_white

##################################################
# Daisyworld-henkinen planetta-kukkasimulaattori #
##################################################

---

Daisyworld:
https://en.wikipedia.org/wiki/Daisyworld

---

Projektin idea:
Katsoa tuleeko suhteellisen yksinkertaisista toimintasäännöistä emergenttiä käytöstä

---

Toteutus, toiminta:

Ohjelma simuloi planeettaa ja sen ilmastoa sekä sitä, miten heijastuvuuden (albedon) muutokset vaikuttavat
planeetan ilmastoon ja eri kukkalajien elinolosuhteisiin.

Alkuasetelma:
1) Aloituksessa luodaan määritetyn kokoinen ruudukko, joka simuloi planeettaa. Toistaiseksi ruudukko on neliömäinen,
   eli pallomaisuutta ei tässä oteta huomioon.

2) Ruudukko spawnataan täyteen satunnaisesti mustia ja valkoisia kukkia

Joka vuoro tapahtuu seuraavaa jokaiselle solulle (= ruudukon ruudulle):
1) Solu laskee lämpötilansa itsensä ja välittömien neljän naapurinsa lämpötiloista keskiarvona. Tämä simuloi
   lämpötilan tasaantumista ilmavirtojen yms. mukana.

2) Solun lämpötilaan lisätään auringon säteily kaavalla:
   self.temp += sun_power * (1 - self.albedo)
   Albedo on siis solun heijastuvuus. Jos albedo = 1 niin kaikki tuleva säteily heijastuu pois.

3) Solu säteilee pois lämpöenergiaa radiation-muuttujan verran.

Kohtiin 2 ja 3 tärkeä huomio: jos solussa on kukka niin albedo- ja radiation-arvot otetaan kukasta, ei solusta!

4) Jos solussa on kukka niin sen ikälaskuriin lisätään aikaa seuraavalla kaavalla:
   self.life_counter += 1 + int(temp_diff / 20)
   temp_diff on kukan optimilämpötilan ja solun lämpötilan erotus.
   Kukka siis elää sitä lyhempään mitä kauempana lämpötila on sen optimilämpötilasta.

5) Jos kukan elinikä ylitää maksimieliniän niin se kuolee

6) Lopuksi jos solussa ei ole kukkaa niin siihen spawnaa mahdollisesti uusi. Se, minkä värinen kukka tyhjään soluun
   spawnaa, menee seuraavasti:
   -lähtökohtana 50/50-mahdollisuudet
   -mitä kauempana solun lämpötila on kukan optimilämpötilasta, sen huonompi on mahdollisuus spawnata
   -jos lämpötilaerotus optimista on yli 50 asetetta, kukka ei spawnaa





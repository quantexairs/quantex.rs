# CLAUDE.md — Quantex.rs

## Projekat

Staticki sajt za Quantex, digitalnog partnera za samostalne i male biznise. Sajt je na srpskom i objavljuje se preko GitHub Pages sa domenom quantex.rs. Nema framework-a, build koraka, CMS-a ni package manager-a u samom repou.

## Pozicioniranje, ne menjati bez odluke korisnika

Quantex pomaze ljudima da rade, zaradjuju i zive od onoga sto vole. Bilo da se rade o zanatu, sportu, fotografiji, masazi, salonu, servisu, usluzi ili proizvodu, klijent ne mora da bude i marketinski tim.

Osnovna poruka: **Ti radiš svoj zanat. Mi preuzimamo digitalni deo.**

Ciljna publika:
- osobe koje imaju ideju, jos nemaju firmu i zele da pokrenu biznis
- novi samostalni biznisi
- postojeci mali biznisi kojima je potrebno digitalno preuredjenje
- saloni i rad po terminima, kreativci, strucnjaci, zanati, servisi i drugi samostalni rad
- Srbija i zemlje bivse Jugoslavije, odnosno Balkan

Ton je topao, ljudski, ambiciozan i konkretan. Ne obecavati zaradu, prvu poziciju, AI citiranje, broj klijenata niti rezultate koje ne mozemo da kontrolisemo. Koristiti samo stvarne projekte i proverljive rezultate.

## Ponuda i cene

Sajt je prvi proizvod. Sve ostalo je modularno i neobavezno.

- **Standardni poslovni sajt: €500 jednokratno.** Sadrzaj i struktura po dogovoru, mobilni prikaz, CMS, tehnicki SEO i AEO od prvog dana. Prva verzija za 7 dana od dogovorenog obima i prijema osnovnih informacija. Placanje 50% na pocetku i 50% pred lansiranje.
- **Sadrzaj: €12 po objavi.** Blog tekst napisan i postavljen na sajt klijenta, carousel od 5 do 7 slika i caption za Instagram, Facebook i LinkedIn. Preporuka je 2 do 4 objave mesecno, ali nema obaveze.
- **Vodjenje reklama: €100 mesecno.** Dogovorene Google ili Meta kampanje. Budzet za oglase je poseban i klijent ga placa direktno platformi.
- **Plan, osnovni identitet, foto, video, aplikacije i automatizacija:** opciono, cena i rok prema obimu.

Nema obaveznog mesecnog odrzavanja, paketa, broja objava ni dugorocnog ugovora. Klijent moze sve da prepusti timu ili da ucestvuje u odobravanjima koliko zeli.

Glavni CTA: **Pošalji svoju ideju**, forma na `/#ideja`. Ne traziti naziv firme kao obavezno polje.

## Struktura

- `index.html`: pocetna i kontakt forma
- `usluge/`: izrada sajta, SEO, AEO, sadrzaj, reklame, plan i identitet, aplikacije
- `cenovnik.html`: modularne cene i obim
- `case-studies.html`: stranica "Projekti" sa pet stvarnih projekata
- `vodic.html`: besplatan vodic dostupan odmah, bez lead forme
- `blog/`: novi prakticni tekstovi za male biznise
- `politika-privatnosti.html`, `uslovi-koriscenja.html`: pravne stranice
- `sitemap.xml`, `llms.txt`, `robots.txt`: indeksiranje i AEO osnove
- `assets/projects/`: stvarni screenshot-ovi portfolio sajtova
- `assets/og-image.jpg`: drustvena slika, 1200x630
- `css/style.css`, `pages.css`, `responsive.css`, `animations.css`: osnovni stilovi
- `css/brand.css`: aktuelni svetli identitet i novi home layout, ucitava se poslednji
- `js/main.js`: navigacija, FAQ, forma i slideri
- `tools/`: lokalni generator sadrzaja, git-ignored

## Vizuelni identitet

Svetli, cist studio izgled sa stvarnim projektima i ljudima, bez genericnih AI grafika. Osnovne boje su u `css/brand.css`: pozadina `#fbfbf8`, tekst `#182235`, akcent `#2859d7`, sekundarni akcent `#0c8e99`. Footer je taman.

Logo je `assets/quantex-logo.svg`, tagline "DIGITALNI PARTNER". Ne vracati "AI AUTOMATION AGENCY".

## Pisanje sadrzaja

- Srpski ekavski izgovor, gramaticki ispravni padezi.
- Bez em dash (`—`) i en dash (`–`) u vidljivom tekstu.
- Bez korporativnog zargona, floskula i generickih AI fraza.
- Pisati za vlasnika malog biznisa koji nema vremena da uci marketing.
- Konkretno objasniti obim, cenu, rok i sledeci korak gde je poznato.
- Bez izmisljenih statistika, klijenata, recenzija i rezultata.
- SEO i AEO objasnjavati jednostavno i bez garancija.
- Svaka stranica treba da ima jedinstven title, description, canonical, OG podatke i odgovarajuci JSON-LD.
- FAQ schema mora da odgovara vidljivom FAQ sadrzaju.

## Generator sadrzaja u tools/

Generator pravi jednu modularnu objavu: blog tekst za sajt, carousel od 5 do 7 slika i caption. Ne generisati stare teme o AI automatizaciji kao glavnoj ponudi. Teme treba da odgovaraju na stvarna pitanja malih biznisa o pokretanju, sajtu, SEO-u, AEO-u, sadrzaju, reklamama i digitalnom rastu.

Ne pokretati automatsko objavljivanje na drustvenim mrezama bez eksplicitne saglasnosti korisnika. Proveriti lokalno generisani sadrzaj pre objave.

## Provere pre zavrsetka izmene

- Proveriti lokalne linkove, slike, anchor-e i javne resurse.
- Proveriti JSON-LD sintaksu i poklapanje FAQ schema sa vidljivim tekstom.
- Proveriti desktop i mobilni prikaz u Playwright-u.
- Proveriti da kontakt forma radi sa imenom, email-om, fazom i opisom ideje.
- Proveriti da se cene i rokovi ne razlikuju izmedju stranica.
- Proveriti da nove stranice imaju `brand.css` posle `pages.css`.
- Ne dodavati englesku verziju dok korisnik ne zatrazi njen povratak.
- Ne raditi commit ni push bez eksplicitnog zahteva korisnika.

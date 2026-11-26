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

Teziste ponude, odluka korisnika od 15. novembra 2026: sajtovi sa punom analitikom (kako posetioci koriste sajt), najbolji moguci SEO i AEO, vodjenje drustvenih mreza, pravljenje i vodjenje reklama.

Ton je topao, ljudski, ambiciozan i konkretan. Ne obecavati zaradu, prvu poziciju, AI citiranje, broj klijenata niti rezultate koje ne mozemo da kontrolisemo. Koristiti samo stvarne projekte i proverljive rezultate.

## Ponuda i cene

Sajt je prvi proizvod. Sve ostalo je modularno i neobavezno.

- **Standardni poslovni sajt: €500 jednokratno.** Sadrzaj i struktura po dogovoru, mobilni prikaz, tehnicki SEO i AEO od prvog dana. Nema CMS-a: klijent javi izmenu, mi je uradimo, manje izmene (nekoliko minuta) su besplatne, vece se cene prema obimu. Besplatan hosting zauvek je ukljucen u cenu (domen se placa posebno registraru). Prva verzija za 7 dana od dogovorenog obima i prijema osnovnih informacija. Placanje 50% na pocetku i 50% pred lansiranje.
- **Sadrzaj: €12 po objavi.** Blog tekst napisan i postavljen na sajt klijenta, carousel od 5 do 7 slika i caption za Instagram, Facebook i LinkedIn. Preporuka je 2 do 4 objave mesecno, ali nema obaveze.
- **Vodjenje reklama: €100 mesecno.** Dogovorene Google ili Meta kampanje. Budzet za oglase je poseban i klijent ga placa direktno platformi.
- **Plan, osnovni identitet, foto, video, aplikacije i automatizacija:** opciono, cena i rok prema obimu.

Nema obaveznog mesecnog odrzavanja, paketa, broja objava ni dugorocnog ugovora. Klijent moze sve da prepusti timu ili da ucestvuje u odobravanjima koliko zeli.

Glavni CTA: **Pošalji svoju ideju**, forma na `/#ideja`. Ne traziti naziv firme kao obavezno polje.

## Struktura

- `index.html`: pocetna i kontakt forma
- `usluge/`: izrada sajta, SEO, AEO, sadrzaj, reklame, plan i identitet, aplikacije
- `cenovnik.html`: modularne cene i obim
- `case-studies.html`: stranica "Projekti" sa osam stvarnih projekata
- `vodic.html`: besplatan vodic dostupan odmah, bez lead forme
- `blog/`: novi prakticni tekstovi za male biznise
- `politika-privatnosti.html`, `uslovi-koriscenja.html`: pravne stranice
- `sitemap.xml`, `llms.txt`, `robots.txt`: indeksiranje i AEO osnove
- `assets/projects/`: stvarni screenshot-ovi portfolio sajtova
- `assets/og-image.jpg`: drustvena slika, 1200x630
- `css/style.css`, `pages.css`, `responsive.css`, `animations.css`: osnovni stilovi
- `css/brand.css`: aktuelni svetli identitet i novi home layout, ucitava se poslednji
- `js/main.js`: navigacija, FAQ, forma i slideri
- `js/analytics.js`: baner za pristanak, GA4 i PostHog, svi dogadjaji. Ucitan na svakoj stranici pre `animations.js`
- `social/`: slike i video odobrenih Instagram objava, javno jer ih Meta preuzima sa sajta
- `tools/`: interni alati, git-ignored. Remotion studio za carousel i reels, Instagram objava, provera sajta, nedeljni izvestaj. Pocni od `tools/README.md`

## Vizuelni identitet

Svetli, cist studio izgled sa stvarnim projektima i ljudima, bez genericnih AI grafika. Osnovne boje su u `css/brand.css`: pozadina `#fbfbf8`, tekst `#182235`, akcent `#2859d7`, sekundarni akcent `#0c8e99`. Footer je taman.

Logo je `assets/quantex-logo.svg`, tagline "DIGITALNI PARTNER". Ne vracati "AI AUTOMATION AGENCY".

Puni brand guidelines su u `tools/docs/brand.md`, a boje i fontovi za objave u `tools/brand/tokens.json`. Kada se promeni boja u `css/brand.css`, promeniti je i tamo.

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

## Analitika

Nista se ne ucitava pre pristanka posetioca (Google Consent Mode v2, baner iz `js/analytics.js`). Ne vracati inline GA4 kod u `<head>`. Novi dogadjaj ide kroz `window.qxTrack` ili `data-track`. Spisak dogadjaja i podesavanje PostHog-a su u `tools/docs/runbooks/analytics.md`. Kada se promeni sta se meri, azurirati `politika-privatnosti.html`.

## Sadrzaj za mreze i automatizacija u tools/

Sadrzaj objava je u `tools/studio/src/content/carousels.js` i `reels.js`, pise ga Claude u sesiji, bez LLM poziva iz skripti. `node render.mjs` pravi slike i video u novom identitetu i stavku u redu objava sa `"approved": false`. Stari Python generator je u `tools/legacy/`.

Teme treba da odgovaraju na stvarna pitanja malih biznisa o pokretanju, sajtu, analitici, SEO-u, AEO-u, sadrzaju, reklamama i digitalnom rastu. Ne vracati teme o AI automatizaciji kao glavnoj ponudi.

Objava ide samo preko zvanicnog Instagram API-ja, nikad kroz automatizaciju pregledaca. Nista se ne objavljuje bez `"approved": true`, a to postavlja samo korisnik. Posle promene cene, roka ili obima na sajtu ponovo renderovati neobjavljene stavke.

Zakazani poslovi (autopost, provera sajta, nedeljni izvestaj, ntfy obavestenja) rade na Kali serveru u Tailscale mrezi, `~/Projects/quantex.rs/tools`. Posle izmene u `tools/` pokrenuti `bash tools/scripts/ops/sync-server.sh`. Cron se ne instalira na laptopu. Uputstvo: `tools/docs/runbooks/automation.md`.

## Provere pre zavrsetka izmene

- Proveriti lokalne linkove, slike, anchor-e i javne resurse.
- Proveriti JSON-LD sintaksu i poklapanje FAQ schema sa vidljivim tekstom.
- Proveriti desktop i mobilni prikaz u Playwright-u.
- Proveriti da kontakt forma radi sa imenom, email-om, fazom i opisom ideje.
- Proveriti da se cene i rokovi ne razlikuju izmedju stranica.
- Proveriti da nove stranice imaju `brand.css` posle `pages.css` i `js/analytics.js` pre `js/animations.js`.
- Ne dodavati englesku verziju dok korisnik ne zatrazi njen povratak.
- Ne raditi commit ni push bez eksplicitnog zahteva korisnika.

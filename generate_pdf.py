"""
Quantex — Interni vodič kroz usluge
Generisanje PDF-a za interne potrebe
"""

from fpdf import FPDF
from fpdf.enums import XPos, YPos

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", FONT_DIR + "DejaVuSans.ttf")
        self.add_font("DejaVu", "B", FONT_DIR + "DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", FONT_DIR + "DejaVuSans-Oblique.ttf")
        self.add_font("DejaVu", "BI", FONT_DIR + "DejaVuSans-BoldOblique.ttf")

    def header(self):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "Quantex — Interni vodič kroz usluge  |  Poverljivo", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def footer(self):
        self.set_y(-14)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Strana {self.page_no()}", align="C")

    def chapter_title(self, num, title, subtitle=""):
        self.set_fill_color(12, 18, 40)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 12, f"{num}. {title}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if subtitle:
            self.set_fill_color(30, 40, 80)
            self.set_font("DejaVu", "I", 10)
            self.cell(0, 8, f"   {subtitle}", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_text_color(30, 30, 30)
        self.ln(4)

    def section(self, title):
        self.set_font("DejaVu", "B", 12)
        self.set_text_color(20, 60, 160)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_draw_color(20, 60, 160)
        self.set_line_width(0.4)
        self.line(self.get_x(), self.get_y(), self.get_x() + 170, self.get_y())
        self.ln(3)
        self.set_text_color(30, 30, 30)

    def body(self, text):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def bullet(self, items, bold_prefix=False):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(40, 40, 40)
        for item in items:
            self.set_x(self.l_margin + 4)
            if isinstance(item, tuple):
                # (bold_part, normal_part)
                self.set_font("DejaVu", "B", 10)
                self.cell(0, 5.5, f"  \u2022  {item[0]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                if item[1]:
                    self.set_font("DejaVu", "", 10)
                    self.set_x(self.l_margin + 14)
                    self.multi_cell(0, 5, item[1], new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            else:
                self.cell(0, 5.5, f"  \u2022  {item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def box(self, label, text, color=(240, 245, 255)):
        self.set_fill_color(*color)
        self.set_draw_color(180, 200, 230)
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(30, 30, 30)
        self.set_line_width(0.3)
        x = self.get_x()
        y = self.get_y()
        # measure height
        lines = self.multi_cell(0, 5, text, dry_run=True, output="LINES")
        h = len(lines) * 5 + 12
        self.rect(x, y, 170, h, style="DF")
        self.set_xy(x + 4, y + 3)
        self.cell(0, 5, label, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_x(x + 4)
        self.set_font("DejaVu", "", 9)
        self.set_text_color(50, 50, 50)
        self.multi_cell(162, 5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)

    def warning(self, text):
        self.box("  Paznja:", text, color=(255, 245, 235))

    def tip(self, text):
        self.box("  Savet:", text, color=(235, 250, 240))

    def price_row(self, paket, setup, monthly, opis):
        self.set_font("DejaVu", "B", 10)
        self.set_fill_color(245, 247, 252)
        self.set_draw_color(200, 210, 230)
        self.set_line_width(0.2)
        self.cell(35, 7, paket, border=1, fill=True)
        self.cell(35, 7, setup, border=1, fill=True)
        self.cell(30, 7, monthly, border=1, fill=True)
        self.set_font("DejaVu", "", 9)
        self.cell(70, 7, opis, border=1, fill=False, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ─────────────────────────────────────────────
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=16)
pdf.set_margins(18, 18, 18)
pdf.add_page()

# ── NASLOVNA ──────────────────────────────────────────────────
pdf.set_font("DejaVu", "B", 28)
pdf.set_text_color(12, 18, 40)
pdf.ln(20)
pdf.cell(0, 14, "Quantex", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DejaVu", "", 14)
pdf.set_text_color(80, 80, 80)
pdf.cell(0, 8, "Interni vodic kroz usluge", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(6)
pdf.set_font("DejaVu", "I", 10)
pdf.set_text_color(120, 120, 120)
pdf.cell(0, 6, "Za internu upotrebu — pre prvog klijentskog razgovora", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(30)

pdf.set_font("DejaVu", "", 10)
pdf.set_text_color(40, 40, 40)
pdf.multi_cell(0, 6, (
    "Ovaj dokument postoji da biste mogli da udjete u svaki prodajni razgovor bez "
    "improvizacije. Svaka od cetiri usluge koje Quantex nudi opisana je tehnickim "
    "jezikom ali i prakticnim uputstvima: sta tacno radite, kojim alatima, sta "
    "predajete klijentu i sta moze da krene naopako.\n\n"
    "Preporuka: prodjite kroz svaku sekciju jednom pre prvog sastanka sa potencijalnim "
    "klijentom iz te oblasti. Nemate da znate sve napamet, ali treba da razumete "
    "procese i da znate sta pitati klijenta."
), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.ln(16)
pdf.set_font("DejaVu", "B", 11)
pdf.set_text_color(20, 20, 20)
pdf.cell(0, 7, "Sadrzaj:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("DejaVu", "", 10)
sadrzaj = [
    "1.  Automatizacija zakazivanja",
    "2.  Generisanje lidova (Lead Generation)",
    "3.  AI agent za firmu",
    "4.  Interni AI sistemi",
    "5.  Kako prodati — pitanja koja postaviti klijentu",
    "6.  Tehnicka osnova — alati i platforme",
]
for s in sadrzaj:
    pdf.cell(0, 6.5, f"     {s}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


# ══════════════════════════════════════════════════════════════════
# 1. AUTOMATIZACIJA ZAKAZIVANJA
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("1", "Automatizacija zakazivanja",
                  "Sistem koji prima, potvrdjuje i podseca na termine — automatski")

pdf.section("Sta je to, konkretno?")
pdf.body(
    "Automatizacija zakazivanja je sistem koji preuzima sve sto inace treba covek da uradi "
    "kad neko hoce da zaduzi termin: odgovori na poruku, proveri slobodne termine u kalendaru, "
    "potvrdi zakazivanje, poslje podsetnike dan pre i sat pre, i obradi otkazivanje.\n\n"
    "Primer: Klijent poslje WhatsApp poruku 'Mogu li da zakazu pregled za sredu?' — "
    "sistem automatski odgovori, ponudi slobodne termine, potvrdi izbor, unese u Google Calendar "
    "i poslje SMS podsetnike. Bez ijednog klika sa vase strane."
)

pdf.section("Kome ovo prodajete?")
pdf.bullet([
    "Zubar, fizioterapeut, psiholog, frizerski salon — bilo ko ko radi na termine",
    "Advokati i konsultanti koji imaju intake pozive sa novim klijentima",
    "Prodajni timovi koji zakazuju demo pozive ili terenske posete",
    "Servisi, automehanicari — zakazivanje dolaska vozila",
    "Agenti za nekretnine — zakazivanje obilazaka",
])

pdf.section("Kako to izgleda tehnicke strane?")
pdf.body("Postoje dva pristupa, zavisno od budzeta i sloztenosti:")
pdf.bullet([
    ("Make (ranije Integromat) + Calendly/Cal.com",
     "Najbrze za izgraditi. Calendly prima termin, Make poveze sa Google Calendarom klijenta, "
     "poslje email i SMS podsetnike. Calendly ima besplatni plan, Make ima 1000 operacija/mesecno besplatno."),
    ("Custom resenje (N8N + Google Calendar API)",
     "Kada klijent vec ima svoj sistem (npr. clinic management software) koji treba integrisati. "
     "N8N je self-hosted workflow alat koji se moze postaviti na VPS-u za ~5 EUR/mesecno."),
    ("WhatsApp Business API + webhook",
     "Za klijente koji zakazuju iskljucivo kroz WhatsApp. Koristi Twilio ili 360Dialog kao "
     "gateway, a Make/N8N za logiku."),
])

pdf.section("Korak po korak — kako izgraditi Starter paket")
pdf.bullet([
    "Korak 1: Klijent vam da pristup svom Google Calendar-u (ili Outlook-u). Dodajte servisni nalog.",
    "Korak 2: Podesite Calendly nalog za klijenta — tipovi termina, trajanje, buffer izmedju termina.",
    "Korak 3: U Make napravite scenario: okidac = novi Calendly termin, akcija = potvrda emailom + SMS.",
    "Korak 4: Za SMS koristite Twilio (1 SMS = ~0.008 EUR, prakticki besplatno za male volumene).",
    "Korak 5: Podesite podsetnike — 24h pre i 2h pre termina.",
    "Korak 6: Testirajte zakazivanje od pocetka do kraja sa test nalogom.",
    "Korak 7: Predajte klijentu link za zakazivanje i prodjite kroz sistem zajedno.",
])

pdf.section("Pro paket — sta se dodaje?")
pdf.bullet([
    "Vise zaposlenih: svaki zaposleni ima vlastiti kalendar, sistem diriguje termin ka slobodnom",
    "Vise tipova termina: inicijalni pregled (60 min), kontrola (30 min), hitni termin (15 min)",
    "CRM integracija: svaki novi termin kreira ili azurira kontakt u HubSpot/Pipedrive CRM-u",
    "Otkazivanje: klijent klikne link u podsetiku, odabere novi termin — sistem azurira automatski",
    "Analitika: nedeljni email izvestaj klijentu (broj termina, no-show rate, najpopularnije vreme)",
])

pdf.tip(
    "Za analitiku koristite Google Sheets + Make: svaki termin ide u Sheet, a vi napravite "
    "jednostavan dashboard sa COUNTIF formulama. Klijentu izgleda impresivno, a traje 2 sata da se postavi."
)

pdf.section("Sta dostaviti klijentu (deliverables)")
pdf.bullet([
    "Link za zakazivanje (Calendly stranica sa brendingom klijenta)",
    "Google Calendar integrisan i testiran",
    "Email/SMS sabloni podeseni po zeluji klijenta",
    "Kratko uputstvo (1 strana PDF) kako da dodaju novi tip termina ili zaposle",
    "Make scenario exportovan (backup)",
])

pdf.section("Sta moze da krene naopako?")
pdf.bullet([
    ("Dvostruko zakazivanje (double booking)",
     "Desava se ako klijent ima i Calendly i rucno zakazivanje u kalendaru. Resenje: "
     "sve zakazivanje mora ici kroz isti sistem ili blokirati vreme rucno."),
    ("Klijent ne zeli da da pristup Google Calendar-u",
     "Dosta malih firmi je osetljivo oko ovoga. Alternativa: koristite Calendly kao zasebni "
     "kalendar i neka klijent sam sinhronizuje u svom kalendaru."),
    ("SMS ne stize",
     "Twilio zahteva verifikaciju broja u nekim zemljama. Alternativa: email podsetniciili "
     "WhatsApp notifikacije kroz Make."),
    ("Klijent promeni radno vreme ili zaposlene",
     "Objasnite klijentu da su ove promene jednostavne i u domenu 2h mesecnog odrzavanja."),
])

pdf.section("Vreme izgradnje i cene")
pdf.body("Starter paket: 2-3 radna dana. Pro paket: 5-7 radnih dana.")
pdf.price_row("PAKET", "SETUP", "MESECNO", "STA UKLJUCUJE")
pdf.price_row("Starter", "290 EUR", "59 EUR", "1 tip termina, 1 lokacija, email+SMS")
pdf.price_row("Pro", "590 EUR", "99 EUR", "5 lokacija, vise tipova, CRM, analitika")
pdf.price_row("Enterprise", "po dogovoru", "po dogovoru", "custom integracije, SLA")
pdf.ln(4)

pdf.warning(
    "Mesecna naknada od 59-99 EUR pokriva: Make plan (~9 EUR), Twilio krediti (~3 EUR), "
    "vas sat odrzavanja i profit. Ne nudite besplatni trial — sistem treba odrzavanje."
)


# ══════════════════════════════════════════════════════════════════
# 2. GENERISANJE LIDOVA
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("2", "Generisanje lidova (Lead Generation)",
                  "Automatizovano pronalazenje i kontaktiranje potencijalnih klijenata")

pdf.section("Sta je to?")
pdf.body(
    "Lead generation automatizacija znaci da sistem svaki dan ili nedelju trazi ljude koji "
    "odgovaraju profilu idealnog klijenta vase firme, kontaktira ih personalizovanom porukom, "
    "i prati odgovore — bez da ijedan covek to rucno radi.\n\n"
    "Primer: Prodajete softver za restorane. Sistem svake nedelje nadje 200 restorana na "
    "LinkedInu i Google Maps-u koji nemaju vas softver, poslje im personalizovani email, "
    "prati ko je otvorio i ko je kliknuo, i stavlja zainteresovane u CRM kao topao lid."
)

pdf.section("Razlika izmedju hladnog kontakta (cold) i toplog (warm)")
pdf.body(
    "Ovo je kljucno da razumete pre svakog razgovora sa klijentom:\n"
    "HLADNI KONTAKT: Osoba vas ne zna, nikad nije bila na vasem sajtu. Stopa odgovora je "
    "1-3% ako je poruka dobra. Kvantitet je kljucan.\n"
    "TOPLI KONTAKT: Osoba je bila na vasem sajtu, pratila vas na LinkedInu, komentarisala post. "
    "Stopa odgovora moze biti 15-30%. Mnogo manji broj ali mnogo bolji kvalitet."
)

pdf.section("Sta sistem tacno radi?")
pdf.bullet([
    ("Pronalazenje kontakata (scraping/enrichment)",
     "Apollo.io, Hunter.io ili LinkedIn Sales Navigator daju email adrese i LinkedIn profile. "
     "Apollo ima besplatni plan sa 50 kontakata/mesecno, placeni plan krece od 49 USD/mesecno. "
     "Za email vas klijent mora imati Custom Domain email (ne Gmail!) da bi stopa dostave bila dobra."),
    ("Personalizacija poruka",
     "Svaka poruka mora biti personalizovana da ne zvuci kao spam. Minimum: ime, firma, jedna "
     "konkretna stvar o firmi ('Video sam da otvarate drugu lokaciju...'). Vise personalizacije = veci odgovor."),
    ("Email sekvenca",
     "Tipicno: Email 1 (dan 1) -> Cekanje 3 dana -> Email 2 follow-up -> Cekanje 5 dana -> "
     "Email 3 (poslednja sansa). Ukupno 3-5 emailova. Koristite Instantly.ai ili Lemlist."),
    ("LinkedIn sekvenca",
     "Connection request (bez poruke) -> Prihvatanje -> Poruka -> Follow-up posle 5 dana. "
     "LinkedIn dozvoljava ~100 connection request-a nedeljno pre nego sto pocne da limitira nalog."),
    ("Pracenje i CRM",
     "Ko je otvorio email, ko je kliknuo, ko je odgovorio — sve ide u CRM (HubSpot besplatni plan). "
     "Toplim lidovima (otvorio 3+ puta bez odgovora) prodajni tim salje rucnu personalizovanu poruku."),
])

pdf.section("Tehnicka arhitektura — Starter paket")
pdf.bullet([
    "Apollo.io za pronalazenje emailova (placeni plan klijenta ili vas reseller nalog)",
    "Instantly.ai za email sekvence (29 USD/mesecno, neograniceni emailovi)",
    "Google Workspace email klijenta (OBAVEZNO custom domain, ne Gmail.com)",
    "Make za automatizaciju toka: novi odgovor -> HubSpot kontakt",
    "HubSpot besplatni CRM za pracenje lidova",
])

pdf.section("Tehnicka arhitektura — Pro paket")
pdf.bullet([
    "Sve iz Starter-a +",
    "Phantombuster za LinkedIn scraping i automatizovane connection request-e",
    "A/B testiranje: 2-3 varijante subject linije i poruke, pobednik dobija veci deo kampanje",
    "Lead scoring: Apollo taguje kontakte po senioritetu, velicini firme, industiji",
    "Dedikacni email domain (npr. outreach.klijentovafirma.com) za bolju isporuku",
])

pdf.section("BITNO: Email deliverability (isporucivost)")
pdf.body(
    "Ovo je 80% uspeha kampanje. Ako emailovi idu u Spam, sve ostalo je beskorisno."
)
pdf.bullet([
    "Domain mora biti star minimum 2 nedelje pre slanja (bolje 4+) — nova domena ide u spam",
    "Podesite SPF, DKIM i DMARC zapise — bez ovoga gotovo sigurno Spam folder",
    "Warmup period: prve 2 nedelje saljite 10-20 emailova dnevno, polako povecavajte",
    "Instantly i Lemlist imaju automatski warmup — to je jedna od kljucnih prednosti",
    "Nikad ne saljite vise od 50-80 emailova dnevno po domenu u pocetku",
    "Pratite bounce rate (treba biti ispod 2%) i spam rate (ispod 0.1%)",
])

pdf.warning(
    "Nikad ne koristite klijentov glavni poslovni email (marko@firma.com) za cold outreach. "
    "Napravite zasebni domen (outreach.firma.com ili getfirma.com) koji ne steti reputaciji "
    "glavnog domena ako Campaign bude markirana kao spam."
)

pdf.section("Sta dostaviti klijentu")
pdf.bullet([
    "Postavljenu i tesiranu email sekvencu (3-4 emaila) sa aprobovanim tekstom",
    "Konfigurisan Apollo/LinkedIn profil za scraping",
    "SPF/DKIM/DMARC podeseni na domenima klijenta",
    "HubSpot ili alternativni CRM sa pipeline-om za lidove",
    "Izvestaj prve nedelje: broj poslatih, otvorenih, odgovora",
    "Mesecni izvestaj: stopa otvaranja, odgovora, konverzije u sastanak",
])

pdf.section("Realne ocekivane performanse")
pdf.bullet([
    "Stopa otvaranja emaila: 30-55% (ako je subject dobar)",
    "Stopa odgovora: 1.5-5% (hladni kontakt — ovo je normalno, ne lose)",
    "Konverzija u sastanak: 0.5-2% ukupno",
    "Za 500 kontakata mesecno: realnih 2-10 novih sastanaka/poziva",
])
pdf.tip(
    "Objasnite klijentu pre pocetka kampanje da je hladni kontakt igra brojeva. "
    "500 emailova da bi dobili 3 razgovora je dobar rezultat. Klijenti cesto ocekuju "
    "da ce svaki email dobiti odgovor — postavite realna ocekivanja od pocetka."
)

pdf.section("Vreme izgradnje")
pdf.body("Starter: 4-5 dana (uglavnom konfig i domain warmup koji traje 2 nedelje).\nPro: 7-10 dana.\nNapomena: warmup period znaci da prva prava kampanja krece posle 2-3 nedelje od pocetka posla.")
pdf.price_row("PAKET", "SETUP", "MESECNO", "STA UKLJUCUJE")
pdf.price_row("Starter", "390 EUR", "99 EUR", "500 kontakata/mes, 1 kanal, osnovna kvalifikacija")
pdf.price_row("Pro", "790 EUR", "179 EUR", "2000 kontakata, multichannel, A/B test, scoring")
pdf.price_row("Enterprise", "po dogovoru", "po dogovoru", "custom, veci volumen, account manager")
pdf.ln(4)


# ══════════════════════════════════════════════════════════════════
# 3. AI AGENT ZA FIRMU
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("3", "AI agent za firmu",
                  "Sistem koji odgovara na pitanja klijenata i zaposlenih — 24/7")

pdf.section("Sta je to?")
pdf.body(
    "AI agent za firmu je chatbot obucen isljkucivo na dokumentima i podacima klijenta. "
    "Za razliku od ChatGPT-a koji zna sve ali nista specificno o firmi, ovaj agent zna samo "
    "ono sto mu je dato (cenovnik, pravilnik, FAQ, opisi usluga) ali to zna savrseno.\n\n"
    "Tehnicko ime za ovu arhitekturu je RAG — Retrieval-Augmented Generation. Sistem "
    "pretrazuje vase dokumente vektorskim pretragivanjem i koristi LLM (GPT-4o, Claude, Gemini) "
    "da formulise odgovor. Rezultat: precizni odgovori specifici za firmu, ne genericki sadrzaj."
)

pdf.section("Tipicne primene — sta zaista prodajete klijentima?")
pdf.bullet([
    ("Korisnicki servis chatbot na sajtu",
     "Agent koji odgovara na pitanja posetilaca o uslugama, cenama, rokovima isporuke. "
     "Radi 24/7, odgovara za sekunde, eskalira komplikovane slucajeve na coveka."),
    ("Interni Q&A za zaposlene",
     "Zaposleni pitaju agenta o procedurama, beneficijama, pravilnicima. Agent pretrazuje "
     "interni wiki/Google Drive i daje konkretan odgovor sa linkom na izvor."),
    ("Sales qualifier bot",
     "Agent na sajtu koji vodi razgovor sa potencijalnim klijentom, kvalifikuje potrebe "
     "i prosljedjuje toplim lidovima prodajnom timu sa sazetkom razgovora."),
    ("Podrska za real estate agente",
     "Agent koji zna sve detalje nekretnina u portfoliju i odgovara potencijalnim kupcima "
     "o kvadraturi, cetvi, cenama, terminima obilazaka."),
])

pdf.section("Tehnicka arhitektura — kako se to gradi?")
pdf.body("Postoje tri nivoa sloztenosti:")

pdf.bullet([
    ("Nivo 1 — No-code (Chatbase, Botpress, Voiceflow)",
     "Najbrze za izgraditi (1-2 dana). Uploadujete dokumente, platforma sama pravi RAG. "
     "Chatbase: besplatni plan do 1 chatbota sa 400k karaktera. Placeni: od 19 USD/mes. "
     "Dobar za Starter paket. Ogranicenje: manje kontrole nad ponasanjem agenta."),
    ("Nivo 2 — Low-code (n8n + OpenAI API + Pinecone)",
     "Vise kontrole, prilagodljivije, jeftiniji API troskovi. n8n workflow hvatqa pitanje, "
     "salje u Pinecone (vektor baza za pretragu dokumenata), uzima relevantne delove, "
     "salje GPT-4o-u za formulaciju odgovora. Postavljanje: 3-5 dana."),
    ("Nivo 3 — Custom kod (Python + LangChain/LlamaIndex)",
     "Za slozene slucajeve: vise izvora podataka, custom logika, fine-tuning. "
     "Potrebno znanje programiranja. Ovo je Enterprise nivo."),
])

pdf.section("Konkretni alati — Starter paket (Chatbase)")
pdf.bullet([
    "Nalog na Chatbase.co (placeni plan 19 USD/mes ili klijentov nalog)",
    "Prikupite dokumente: FAQ, opisi usluga, cenovnik, pravilnici (PDF, Word, TXT)",
    "Uploadujte u Chatbase, chatbot je spreman za testiranje za <30 min",
    "Customizujte: ime agenta, ton, boja, logo klijenta",
    "Ugradite na sajt: Chatbase daje embed kod (2 linije HTML-a)",
    "Podesite escalation: kada agent ne zna odgovor, trazi email korisnika",
    "Mesecno: proverite tacnost odgovora, dodajte nova dokumenta po potrebi",
])

pdf.section("Konkretni alati — Pro paket (n8n + OpenAI + Pinecone)")
pdf.bullet([
    "n8n instanca na VPS-u (DigitalOcean/Hetzner, ~6 EUR/mes za server)",
    "OpenAI API kljuc (troskovi: ~0.005 USD po razgovoru za GPT-4o-mini, ~0.05 za GPT-4o)",
    "Pinecone besplatni plan (do 1 indeks, dovoljno za vecinu klijenata)",
    "Workflow: primljeno pitanje -> embedding -> Pinecone pretraga -> GPT formulacija -> odgovor",
    "Whatsapp integracija: Twilio ili 360dialog kao gateway, n8n webhook",
    "Email integracija: Zapier/n8n cita dolazne emailove, agent odgovara",
    "Logging svih razgovora u Google Sheet za analizu i izvestaje",
])

pdf.section("Kljucni korak: priprema dokumentacije")
pdf.body(
    "Ovo je cesto podzenijena faza i kljucna je za kvalitet agenta:\n"
    "Trening agenta je samo tako dobar kao sto su dobra dokumenta koja mu dajete. "
    "Ako klijent ima lose napisani FAQ ili zastarjeli pravilnik, agent ce davati netacne odgovore."
)
pdf.bullet([
    "Trazite od klijenta: sva dokumenta u PDF/Word formatu, FAQ ako postoji, opis svakog tipa usluge",
    "Pre treninga, pregledajte dokumenta — netacnosti u dokumentima = netacni odgovori agenta",
    "Napravite 'Ground Truth' dokument: 20-30 pitanja i tacnih odgovora za testiranje",
    "Posle treninga, prodjite kroz sva pitanja i proverite tacnost pre isporuke klijentu",
    "Definisijte 'granice': sta agent TREBA da radi i sta NECE raditi (politika eskalacije)",
])

pdf.tip(
    "Recite klijentu da je agent 'trener koji zavisi od gradiva koje mu date'. "
    "Sto bolja dokumentacija, to bolji agent. Ovo takodjer pravda mesecnu naknadu: "
    "vi odrzavate dokumentaciju azurnom i pratite tacnost u produkciji."
)

pdf.section("Merenje tacnosti i kvaliteta")
pdf.bullet([
    "Accuracy: procenat odgovora koji su tacni (cilj: >90%)",
    "Hallucination rate: koliko puta agent izmislja odgovor (cilj: <5%)",
    "Escalation rate: koliko puta agent ne moze da pomogne (cilj: zavisi od slucaja, tipicno 10-20%)",
    "Customer satisfaction: kratka ocena 1-5 posle svakog razgovora (Chatbase to ima ugradjeno)",
    "Mesecni izvestaj klijentu: ove metrike + preporuke za poboljsanje",
])

pdf.section("Sta moze da krene naopako?")
pdf.bullet([
    ("Hallucinations — agent izmislja cinjenice",
     "Desava se kada dokument ne pokriva odredjeno pitanje a agent pokusava da nagradit odgovor. "
     "Resenje: definisajte sistem prompt koji kaze 'Ako ne znas odgovor, reci to i predlozi kontakt.'"),
    ("Agent daje pogresne cene",
     "Ako klijent promeni cene a ne azurira dokument. Mesecno odrzavanje je kljucno."),
    ("Klijent unese poverljive podatke u chat",
     "Ovo je GDPR pitanje. Uverite se da su razgovori enkriptovani i da nema logovanje "
     "korisnickih podataka bez saglasnosti."),
    ("Klijent ocekuje da agent obavlja transakcije",
     "Agent Starter paketa samo odgovara na pitanja — ne moze da zakazuje, placa, naruci. "
     "To je funcionalnost viseg nivoa i treba dodatno vreme za razvoj."),
])

pdf.section("Vreme izgradnje")
pdf.body("Starter (Chatbase): 2-3 radna dana ukljucujuci pripremu dokumenta.\nPro (n8n): 7-10 radnih dana.\nNapomena: klijent mora dostaviti sva dokumenta pre pocetka — zakljucajte rok.")
pdf.price_row("PAKET", "SETUP", "MESECNO", "STA UKLJUCUJE")
pdf.price_row("Starter", "490 EUR", "79 EUR", "50 dok, 1 kanal, 1000 razgovora/mes")
pdf.price_row("Pro", "990 EUR", "149 EUR", "neograniceno, 3 kanala, CRM, 5000 razg.")
pdf.price_row("Enterprise", "po dogovoru", "po dogovoru", "vise agenata, lokalno resenje")
pdf.ln(4)


# ══════════════════════════════════════════════════════════════════
# 4. INTERNI AI SISTEMI
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("4", "Interni AI sistemi",
                  "Baza znanja i automatizovani izvestaji za timove")

pdf.section("Sta je to i cime se razlikuje od AI agenta?")
pdf.body(
    "Interni AI sistem je slican AI agentu ali je INTERNOG karaktera — namenjen je zaposlenima "
    "a ne klijentima. Fokus je na:\n\n"
    "1. Interna baza znanja (Knowledge Base Q&A): Zaposleni postavljaju pitanja o internim "
    "procesima, pravilnicima, procedurama i dobijaju tacne odgovore sa referencama na izvorni dokument.\n\n"
    "2. Automatizovani izvestaji: Sistem povlaci podatke iz razlicitih izvora (CRM, Google Sheets, "
    "baza podataka) i generise izvestaj automatski — nedeljni prodajni pregled, mesecni HR izvestaj...\n\n"
    "3. Uvodzenje novih zaposlenih: Novi clan tima moze da pita sve sto zeli bez da uznemiri kolege."
)

pdf.section("Kome ovo prodajete?")
pdf.bullet([
    "Firme od 10+ zaposlenih gde HR/menadzer trosi >2h nedeljno na odgovaranje na ista pitanja",
    "Firme sa kompleksnim procedurama: advokatura, racunovodstvo, konsalting, klinikje",
    "Firme koje imaju visoki turnover zaposlenih — uvodzenje novog clanovima je skupo",
    "Firme koje prave rucne Excel izvestaje koji traju sate — automatizacija izvestavanja",
])

pdf.section("Tehnicka arhitektura — Starter paket")
pdf.body("Koristimo isti RAG pristup kao za AI agenta, ali za interni pristup:")
pdf.bullet([
    "Notion ili Google Drive klijenta kao izvor dokumentacije (API integracija)",
    "Chatbase ili custom RAG sistem postavljen samo za interne korisnike (ne javno)",
    "Pristup samo za zaposlene: autentikacija putem email domene klijenta",
    "Slack bot integracija: zaposleni pitaju @bot direktno u Slack kanalu",
    "Maksimalno 20 korisnika u Starter paketu (Chatbase plan limit)",
])

pdf.section("Tehnicka arhitektura — Pro paket")
pdf.bullet([
    "n8n + Pinecone + GPT-4o (ista arhitektura kao AI Agent Pro, ali za interni pristup)",
    "Automatska sinhronizacija sa Google Drive/Notion: novi dokument = automatski dodat u bazu znanja",
    "Do 5 razlicitih integracija: Drive, Notion, SharePoint, Confluence, HubSpot...",
    "Automatizovani izvestaji: n8n svake nedelje prikuplja podatke i salje PDF izvestaj emailom",
    "Modul za uvodzenje: novi zaposleni dobija 10-dnevni onboarding niz emailova sa zadacima",
])

pdf.section("Automatizovani izvestaji — kako to izgleda?")
pdf.body("Ovo je cesto najlakoce za prodati jer klijent odmah vidi vrednost:")
pdf.bullet([
    "Nedeljni prodajni pregled: n8n povlaci podatke iz HubSpot/Pipedrive, GPT formatira u pregled, salje email",
    "Mesecni HR izvestaj: broj odsustava, prekovremenih, novih zaposlenih — iz Google Calendar/HR sistema",
    "Finansijska analiza: uvoz bankovnih izvoda, GPT kategorise transakcije, generise pregled",
    "Customer satisfaction summing: GPT cita NPS odgovore i pravi tematski pregled problematika",
])

pdf.tip(
    "Pitajte klijenta: 'Koji izvestaj pravite rucno svake nedelje/meseca koji vam oduzme "
    "vise od sat vremena?' Taj izvestaj je vas prvi projekat. Automatizujte ga, impresionujte "
    "klijenta i onda predlozite siru implementaciju."
)

pdf.section("Onboarding modul — zasto je ovo vredan add-on?")
pdf.body(
    "Uvodzenje novog zaposlenog u proseku kosta firmu 3-6 mesecnih plata tog zaposlenog "
    "(vreme kolega, greske, sporo ucenje). Automatizovani onboarding smanjuje ovo za 30-50%."
)
pdf.bullet([
    "Dan 1: Email sa pristupima sistemima, pravilnikom, uputstvima za prvu nedelju",
    "Dan 2-5: Dnevni emailovi sa zadacima i ciljevima za taj dan",
    "Nedelja 2-4: Nedeljni check-in emailovi sa napretkom i sledecu koracima",
    "Pristup knowledge base botu: novi zaposleni pita agenta umesto kolega",
    "Automatska eskalacija ka manageru ako zaposleni ne otvori email 2 dana zaredom",
])

pdf.section("GDPR i bezbednost — sto ce klijenti pitati")
pdf.bullet([
    "Svi razgovori su enkriptovani u prenosu (HTTPS) i u bazi (AES-256)",
    "Podaci klijenta NE idu u trening OpenAI modela (API pozivi su eksluzivni)",
    "Za strictno poverljive podatke: koristite lokalni LLM (Ollama + Llama 3) umesto OpenAI API",
    "Pravo na brisanje: korisnik moze da zatrazi brisanje svih razgovora",
    "Data residency: Pinecone EU region ili self-hosted Qdrant na EU serveru",
])

pdf.section("Vreme izgradnje")
pdf.body("Starter: 4-6 dana (ukljucujuci API pristup dokumentima).\nPro: 8-12 dana.\nNapomena: najduzi deo je cesto cekanje na IT odeljenje klijenta da da API pristup sistemima.")
pdf.price_row("PAKET", "SETUP", "MESECNO", "STA UKLJUCUJE")
pdf.price_row("Starter", "590 EUR", "89 EUR", "20 korisnika, 1 integracija, osnovna KB")
pdf.price_row("Pro", "1190 EUR", "169 EUR", "neograniceno, 5 integracija, izvestaji, onboarding")
pdf.price_row("Enterprise", "po dogovoru", "po dogovoru", "custom workflow, lokalno resenje")
pdf.ln(4)


# ══════════════════════════════════════════════════════════════════
# 5. KAKO PRODATI — PITANJA ZA KLIJENTA
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("5", "Kako prodati — pitanja za klijenta",
                  "Discovery poziv: sta pitati pre nego sto ponudite bilo sta")

pdf.section("Zlatno pravilo")
pdf.body(
    "Ne prodajete tehnologiju. Prodajete resenje konkretnog problema koji klijent vec ima "
    "i vec ga boli. Tehnologija (n8n, Chatbase, Make) je nebitna klijentu — bitan je rezultat.\n\n"
    "Pre nego sto imate bilo kakvu prezentaciju, postavite ova pitanja:"
)

pdf.section("Pitanja za discovery")
pdf.bullet([
    ("'Koji zadatak vasi zaposleni rade svaki dan koji ih najvise frustrira?'",
     "Ovo otvara razgovor o automatizaciji. Cesti odgovori: odgovaranje na iste emailove, "
     "rucno unoszenje podataka, pravljenje izvestaja, zakazivanje."),
    ("'Koliko vremena nedeljno trosiste na [taj zadatak]?'",
     "Kvantifikujte problem. 5 sati nedeljno x 4 = 20 sati mesecno x prosecna satnica = EUR value."),
    ("'Da li imate klijente koji cekaju >24h na odgovor?'",
     "Otvara razgovor o AI agentu i zakazivanju."),
    ("'Koliko novih klijenata mesecno dolazi iz hladnog kontakta?'",
     "Ako je nula ili neznatno — lead gen je potencijalna usluga."),
    ("'Koji softver vec koristite? (CRM, kalendar, email)',",
     "Vitalin pitanje za procenu sloztenosti integracije."),
    ("'Da li ste vec probali nesto da automatizujete? Sta se desilo?'",
     "Klijenti koji su vec imali lose iskustvo sa automatizacijom imaju vise ocekivanje — treba ih pazljivo voditi."),
    ("'Koji bi bio idealan rezultat posle 3 meseca?'",
     "Definisijte sta je uspeh. Ovo ce biti metrika kojom meriti performanse."),
])

pdf.section("Crvene zastavice — kada odbiti klijenta ili biti oprezan")
pdf.bullet([
    "Klijent hoce 'sve i odmah' za 100 EUR — nerealna ocekivanja vode ka nezadovoljnim klijentima",
    "Klijent nema jasno definisan problem — ne zna sta hoce da automatizuje",
    "Klijent ne zeli da da pristup systemima (Google Calendar, CRM) — bez pristupa nema integracije",
    "Klijent ocekuje da sistem radi bez ikakvih izmena posle prvog meseca — nerealno, treba odrzavanje",
    "Klijent uporeduje vase cene sa Fiverr frilenseri od 50 EUR — nije pravi klijent za vas",
])

pdf.section("Kako postavljati cenu u razgovoru")
pdf.body(
    "Preporuka: ne govorite cenu odmah u prvom razgovoru. Prvo shvatite problem, "
    "zatim procenite vrednost ustedljenog vremena, i cenu uvek predstavite u kontekstu te vrednosti:"
)
pdf.bullet([
    "Primer: 'Rekli ste da vam zakazivanje uzme 3 sata nedeljno. To je 12 sati mesecno. "
    "Ako je vas sat vredan 50 EUR, to je 600 EUR mesecno. Nase resenje kosta 59 EUR mesecno "
    "plus jednokratno 290 EUR postavljanje. Povrat investicije: mesec i po dana.'",
    "Uvek predstavite ukupan godisnji trosak: 290 + 59*12 = 998 EUR/godisnje. "
    "Klijentu zvuci manje od mesecnih troskova."
    "Ponudite besplatni demo ili pilot projekat (2 nedelje) za klijente koji su u nedoumici.",
])

pdf.tip(
    "Kalkulator na quantex.rs je tu upravo za ovo — otvorite ga sa klijentom tokom razgovora "
    "i ukucajte njihove brojeve zajedno. Vizuelizacija meseci do povrata investicije je "
    "mnogo ubedljvija od verbalne argumentacije."
)


# ══════════════════════════════════════════════════════════════════
# 6. ALATI I PLATFORME — TEHNICKA OSNOVA
# ══════════════════════════════════════════════════════════════════
pdf.add_page()
pdf.chapter_title("6", "Tehnicka osnova",
                  "Alati koje koristite i njihovi troskovi")

pdf.section("Workflow automatizacija")
pdf.bullet([
    ("Make (Integromat) — make.com",
     "Vizuelni no-code alat za povezivanje servisa. Besplatni plan: 1000 operacija/mes. "
     "Starter: 9 EUR/mes (10k operacija). Koristi za zakazivanje, lead gen, notifikacije."),
    ("n8n — n8n.io",
     "Open-source alternativa Make-u, self-hosted. Server: 5-10 EUR/mes (Hetzner). "
     "Neogranicene operacije. Vise tehnicko ali mnogo jeftinije za visoke volume."),
    ("Zapier — zapier.com",
     "Skuplje od Make ali ima vise integracija. Izbegavajte za nove projekte osim ako klijent vec koristi."),
])

pdf.section("AI i jezicki modeli")
pdf.bullet([
    ("OpenAI API (GPT-4o, GPT-4o-mini) — platform.openai.com",
     "GPT-4o-mini: 0.15 USD / 1M input tokena (ekstremno jeftino). "
     "GPT-4o: 5 USD / 1M input tokena. Za vecinu klijenata mini je dovoljan."),
    ("Anthropic Claude API (claude-3-5-haiku, claude-3-7-sonnet)",
     "Alternativa OpenAI. Haiku je brz i jeftin (0.25 USD/1M tokena), Sonnet je kvalitetniji."),
    ("Ollama — ollama.com",
     "Za lokalne LLM-ove bez slanja podataka u cloud. Llama 3.1, Mistral. "
     "Zahteva jaci server (min 16GB RAM). Za Enterprise sa GDPR zahtevima."),
])

pdf.section("Chatbot platforme (no-code)")
pdf.bullet([
    ("Chatbase — chatbase.co",
     "Najlaksi RAG chatbot. Besplatni: 1 bot, 400k karaktera. Placeni: 19 USD/mes. "
     "Embed na sajt, WhatsApp, Slack integracije. Preporuka za Starter pakete."),
    ("Botpress — botpress.com",
     "Besplatni plan, vise kontrole od Chatbase. Kompleksniji za podesiti ali mocniji. "
     "Dobar za Pro paket."),
    ("Voiceflow — voiceflow.com",
     "Za glasovne agente (IVR sistemi). Niche ali vredan znati."),
])

pdf.section("Vektor baze (za RAG sisteme)")
pdf.bullet([
    ("Pinecone — pinecone.io",
     "Najlaksi managed servis. Besplatni plan: 1 indeks, 100k vektora (dovoljno za vecinu klijenata). "
     "Starter placeni: 70 USD/mes. Koristite za Pro pakete."),
    ("Qdrant — qdrant.tech",
     "Open-source, self-hosted. Besplatno za hostovanje. Za Enterprise i GDPR slucajeve."),
    ("Supabase + pgvector",
     "PostgreSQL sa vektorskim pretrazivanjem. Ako vec koristite Supabase, jednostavno dodati."),
])

pdf.section("Email i outreach alati")
pdf.bullet([
    ("Instantly.ai — instantly.ai",
     "29 USD/mes. Neograniceni emailovi, automatski warmup, A/B test, analitika. "
     "Preporuka za sve lead gen kampanje."),
    ("Lemlist — lemlist.com",
     "Skuplje (59 USD/mes) ali ima LinkedIn integraciju i personalizovane slike/videe u emailu. "
     "Za Pro kampanje."),
    ("Apollo.io — apollo.io",
     "Baza kontakata + email sekvence. Besplatni plan: 50 emailova/mes. "
     "Placeni: 49 USD/mes. Dobro za pronalazenje emailova."),
    ("Hunter.io — hunter.io",
     "Za pronalazenje emailova po imenu i domenu. Besplatni: 25 pretrage/mes."),
])

pdf.section("Kalendar i zakazivanje")
pdf.bullet([
    ("Calendly — calendly.com",
     "Standard u industriji. Besplatni: 1 tip termina. Placeni: 10 USD/mes po korisniku. "
     "Klijent placa Calendly, vi samo integriste."),
    ("Cal.com — cal.com",
     "Open-source alternativa Calendly-u, self-hosted. Za klijente koji ne zele trosak Calendly-a."),
    ("Google Calendar API",
     "Za direktnu integraciju sa Google Calendar-om bez Calendly-a. Vise koda, vise kontrole."),
])

pdf.section("SMS i poruke")
pdf.bullet([
    ("Twilio — twilio.com",
     "Standard za SMS. 0.007-0.009 EUR po SMS-u u Srbiji. Lako API. Preporuka."),
    ("WhatsApp Business API",
     "Kroz Twilio ili 360dialog. Kompleksnije za podesiti (Meta mora da odobri biznis nalog). "
     "Traje 1-2 nedelje da se dobije pristup."),
])

pdf.section("Hosting i serveri")
pdf.bullet([
    ("Hetzner Cloud — hetzner.com",
     "Najjeftiniji quality VPS. CX22 (2 core, 4GB RAM): 3.79 EUR/mes. "
     "CX32 (4 core, 8GB RAM): 6.77 EUR/mes. EU datacenter, dobar za GDPR."),
    ("DigitalOcean — digitalocean.com",
     "Malo skuplje ali jednostavniji UI. Droplet od 4 EUR/mes za pocetnike."),
    ("Railway / Render",
     "Za brzi deploy Node.js/Python aplikacija. Besplatni plan postoji. Za testiranje."),
])

pdf.section("Troskovni kalkulator za jedan tipican projekat")
pdf.body("Primer: AI agent Pro paket za malog klijenta (mesecni troskovi):")
pdf.bullet([
    "Hetzner server (n8n + Qdrant): 6.77 EUR",
    "OpenAI API (procena 1000 razgovora x 500 tokena): ~5-15 EUR",
    "Twilio SMS (100 notifikacija): ~1 EUR",
    "Backup i monitoring (Uptime Robot besplatni): 0 EUR",
    "UKUPNO VAS TROSAK: ~15-25 EUR mesecno",
    "NAPLATA KLIJENTU: 149 EUR mesecno",
    "MARZA: ~120-130 EUR mesecno po klijentu"
])

pdf.tip(
    "Sa 10 Pro klijenata: 1490 EUR prihoda - 250 EUR troskova = ~1240 EUR neto mesecno "
    "od odrzavanja, bez novog rada. Ovo je cilj — izgraditi portfolio odrzavanja."
)


# ── FINALNA STRANA ────────────────────────────────────────────────
pdf.add_page()
pdf.set_font("DejaVu", "B", 14)
pdf.set_text_color(12, 18, 40)
pdf.cell(0, 10, "Checklist pre prvog klijentskog razgovora", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(4)
pdf.set_font("DejaVu", "", 10)
pdf.set_text_color(40, 40, 40)

checklist = [
    "Znate razliku izmedju hladnog i toplog kontakta i realne stope odgovora",
    "Znate sta je RAG i zasto je bolji od generickog ChatGPT-a za firme",
    "Mozete da objasnite SPF/DKIM/DMARC klijentovom IT odeljenju (1 recenica)",
    "Znate cenu svakog paketa napamet i mozete da je opravdate vrednoscu",
    "Imate spreman kalkulator (quantex.rs/#kalkulator) za discovery poziv",
    "Znate koje pitanje da postavite da biste nasli problem klijenta",
    "Razumete troskovnu strukturu svakog projekta i znate vasu marzu",
    "Znate sta pitati o GDPR-u ako klijent to pomene",
    "Imate jasan onboarding proces: sta treba od klijenta, koji su rokovi",
    "Znate kada da kazete 'to nije za vas' i preusmerite klijenta",
]

for item in checklist:
    pdf.set_x(pdf.l_margin)
    pdf.set_draw_color(20, 60, 160)
    pdf.rect(pdf.get_x(), pdf.get_y() + 1, 4, 4)
    pdf.set_x(pdf.get_x() + 8)
    pdf.cell(0, 6, item, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)

pdf.ln(10)
pdf.set_font("DejaVu", "I", 9)
pdf.set_text_color(120, 120, 120)
pdf.multi_cell(0, 5,
    "Dokument generisan za internu upotrebu. Azurirajte ga kada dodjete do novih znanja "
    "ili kad promenite cenovnik. Dobar posao.",
    new_x=XPos.LMARGIN, new_y=YPos.NEXT
)


# ── SACUVAJ ───────────────────────────────────────────────────────
out = "/home/aceman/Documents/quantex.rs/usluge.pdf"
pdf.output(out)
print(f"PDF sacuvan: {out}")
print(f"Strana: {pdf.page}")

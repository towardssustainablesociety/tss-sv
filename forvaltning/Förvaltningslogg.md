# Förvaltningslogg för TSS

Version 2026-10-31. Den här filen är skriven för att lämnas till en AI-assistent (vilken som helst) eller till en ny förvaltare, så att arbetet kan fortsätta utan tidigare chattar.

**Till AI-assistenten:** läs den här filen, `README.md` och `forvaltning/Skrivregler.md` innan du gör något. Om något i en äldre text krockar med det som står här, gäller den här filen.

## 1. Vad TSS är

- **TSS – Mot ett hållbart samhälle** (*Towards Sustainable Society*) är en kunskapswebbplats om ett hållbart samhälle, grundad av Rolf Thorsell.
- **Visionen:** ett gott liv för alla, inom planetens gränser. Den säger vart vi ska, men inte hur. Den har stöd i FN:s hållbarhetsområden (SDGs, Agenda 2030) och, i Sverige, i regeringsformen 1 kap. 2 §.
- **Ramverket:** FN:s SDGs, Doughnut Economics (Kate Raworth) och de planetära gränserna (Stockholm Resilience Centre).
- **Samhällskartan:** människan i mitten, fyra samhällssystem runt omkring – det demokratiska, det ekologiska, det ekonomiska och det sociala och kulturella – och planetens gränser ytterst. Samma fyra system finns på alla samhällsnivåer, från hushållet till världen.
- **Formen:** varje samhällssystem beskrivs med frågor och svar, skrivna för en läsare som tror på fortsatt ekonomisk tillväxt.
- **Hållning:** TSS är ingen organisation, har ingen finansiering och tar inte ställning för något parti. TSS föreslår en gemensam vision för alla partier; partierna konkurrerar om vägen dit.
- **Licens:** CC BY-SA 4.0. Vem som helst får använda och bygga vidare på texterna. Förvaltaren bestämmer över innehållet på webbplatsen.

## 2. Var allt finns

| Vad | Var |
|---|---|
| Svenska webbplatsen TSS-sv | https://sv.towardssustainablesociety.org – förrådet `towardssustainablesociety/tss-sv` |
| Engelska webbplatsen TSS-en | https://en.towardssustainablesociety.org – förrådet `towardssustainablesociety/tss-en` |
| Språkvalet TSS-www, med korta startsidor på tio språk | https://www.towardssustainablesociety.org – förrådet `towardssustainablesociety/tss-www` |
| Adressen utan www | Vidarebefordras till www (hos Loopia) |

**tss-sv** är navet:
- `texter/` – de 50 sidorna i markdown, en mapp per sida, och `Sidordning.md`.
- `bygg/` – `bygg.py` (gör om texterna till en webbplats), `mall.html`, `stil.css` och `kolla-externa-lankar.sh`.
- `forvaltning/` – den här loggen, `Skrivregler.md`, `Ordlista svenska-engelska.md` (namntabellen och termerna) och `Objektregister Samhällskartan.md`.
- `.github/workflows/publicera.yml` – bygger och publicerar vid varje ändring i `main`.

**tss-en** har bara de engelska texterna och hämtar bygget och namntabellen från tss-sv vid varje bygge.

**tss-www** har `site/` (språkvalet och språksidorna, färdig HTML) och `sprak/<kod>.html` med `bygg-sprak.py`, som bygger språksidorna. Skriptet körs lokalt och resultatet läggs i förrådet.

Konton (GitHub, domänen hos Loopia, Search Console) hanteras av förvaltaren och beskrivs inte här.

## 3. Så görs en ändring

1. Ändra sidfilen i `texter/` i tss-sv. Följ `forvaltning/Skrivregler.md`.
2. Bygg och läs problemlistan:
   `python3 bygg/bygg.py texter _site --sprak`
   Bygget varnar för länkar som inte hittar sin sida, bilder som saknas, fel i `Sidordning.md`, sidor som saknas i namntabellen och "tillväxt" utan bestämning.
3. Visa ändringen för förvaltaren (system, sida, nuvarande text och ny text) och vänta på OK.
4. Skicka till `main`. GitHub bygger och publicerar automatiskt inom några minuter. Kontrollera att körningen lyckades (fliken *Actions*, eller `gh run list`).
5. För över samma ändring till tss-en (bygg med `python3 ../tss-sv/bygg/bygg.py texter _site --lang en --sprak`). Om det inte går i samma omgång: anteckna "väntar på EN" i avsnitt 6.

**En ny sida:** föreslå sidstrukturen först. När förvaltaren har godkänt: skapa mappen och filen, lägg in sidan i `Sidordning.md`, ge den ett engelskt namn i namntabellen och skapa den engelska sidan i tss-en.

**Externa länkar:** kör `bygg/kolla-externa-lankar.sh` i Terminal ibland. 403 är oftast robotspärrar och inget fel; 404 ska rättas.

**Förvaltaren skriver inte själv i git.** AI-assistenten gör ändringarna och skickar dem efter förvaltarens OK.

## 4. Beslut som gäller

Utöver det som står i Skrivregler.md:

**Innehåll**
- **Grundbehov och ömsesidighet:** den som kan förväntas bidra till grunden – det alla behöver – på många sätt, inte bara genom lönearbete. Ingen är skyldig att arbeta för andras extra livskvalitet. Ansvaret för att det finns hållbara arbeten ligger på samhället, inte på den enskilde.
- **Summan avgör, inte varje köp:** helheten ska rymmas inom planetens gränser. Verktygen är tak, priser och regler, som redan finns. Det är inte planekonomi.
- **Ekonomin:** TSS står eller faller med att ekonomin går att förklara. Två frågor ska kunna besvaras: Hur får medborgarna grundtrygghet? Hur hindras pengarna från att användas ohållbart? Principerna "Grundbehov till självkostnad" och "Konkurrens där det är lätt att byta, ägande där det är svårt att byta". Ekonomitexterna ska vara begripliga utan ekonomutbildning, realistiska på lång sikt och hålla mot ekonomers invändningar.
- **Demokratin:** demokratin är bra på att byta ledning, men saknar ett sätt att bestämma riktningen och hålla den. TSS föreslår hur riktningen kan bli synlig och granskbar, aldrig vad politiken ska innehålla.
- **Samhällsnivåerna:** hushållet, föreningar och grannskap, verksamheten, kommunen, regionen, staten, EU och världen. Ingen nivå räcker ensam.

**Webbplatsen**
- Svenska är originalspråket. Engelskan är en likvärdig version.
- Navigeringen byggs av mallen. Sidfilerna innehåller bara texten och de två listorna sist.
- Länkar är mörkblå och understrukna, utom logotypen och namnen i Samhällskartan.
- Samhällskartan är en SVG med riktiga länkar: `texter/Vårt samhälle/Samhällskartan/Samhällskartan.svg`. Den ändras enligt `forvaltning/Objektregister Samhällskartan.md`, i båda språken.
- Bygget ska fungera med Python 3.10 och kräver pandoc.

## 5. Läge 2026-10-31

- Alla 50 sidor är skrivna, granskade och publicerade på svenska och engelska. Språksidorna på tio språk är publicerade på www. Alla tre webbplatserna är öppna för sökmotorer.
- Webbplatsen flyttade från Google Sites till GitHub 2026-10-26–28. Den gamla Sites-versionen och föregångaren *Mot ett hållbart samhälle* (MHS) på Google Sites ska avvecklas.

## 6. Öppet

- **Om TSS** får mogna; förvaltaren kan vilja ändra den.
- **Språksidorna** är inte lästa av någon med språket som modersmål (främst arabiska och hindi).
- **hreflang:** sv och en pekar ännu inte på språksidorna på www (kan läggas in i `bygg.py` med `--sprak`).
- **Visionen** har kvar "Läs vidare" i stället för Kopplingar och Externa källor, och skriver "TSS:s kärna".
- **Domänen:** plan för flerårig betalning och en person till med åtkomst.
- **Medförvaltare:** finns det någon? Ingen brådska.
- **Väntar på EN:** inget.

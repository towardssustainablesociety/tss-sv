# Skrivregler för TSS

Version 2026-10-31. Reglerna gäller alla sidor i TSS-sv och, genom översättningen, i TSS-en. De används både när en sida skrivs och när den granskas.

Reglerna är av två slag:
- **Skrivregler** är fria. De beskriver hur en sida brukar se ut, men får frångås när det gör texten bättre.
- **Kontrollregler** är precisa, så att det går att avgöra om något är fel. En avvikelse är ett **säkert fel**.

Vid granskning skiljs säkra fel från förslag, och det anges var felet finns: system, sida, nuvarande text och vad som ska stå i stället.

## 1. Webbplatsens delar

- **Startsidan** Hållbart samhälle, och under den Vårt samhälle (med Visionen och Samhällskartan), Samhällsutforskaren, Om TSS och Kontakt.
- **Samhällsutforskaren** har de fyra samhällssystemen – Demokratiska, Ekologiska, Ekonomiska och Sociala o kulturella systemet – och dessutom Människan och Ramverk.
- Sidornas ordning står i `texter/Sidordning.md`. Navigeringen (toppmenyn, raden Du är här och listan "Sidorna i …" sist på sidan) byggs automatiskt och skrivs inte i sidfilerna.

## 2. Ett samhällssystem

Varje samhällssystem har tre delar:

1. **Rotsidan** är ingången: 2–3 korta stycken om vad systemet är, några exempelfrågor som punktlista och en uppmaning att välja en fråga i listan sist på sidan. Rotsidan har inga egna frågor med svar.
2. **6–7 frågegrupper**, en sida per grupp, direkt under rotsidan.
3. **En avslutande grupp "[Systemet] o det hållbara samhället"**, som alltid står sist och knyter systemet till visionen. Typfrågor: Vad betyder det att systemet ska bidra till ett hållbart samhälle? Hur hänger det ihop med de andra delarna? Vad behöver förändras? Vem bestämmer riktningen?

Ekonomiska systemet har medvetet åtta grupper plus den avslutande. Det rapporteras inte som avvikelse.

**Ramverkets fyra sidor** (Ramverk, FNs SDGs, Doughnut Economics, Planetära gränser) skrivs beskrivande, inte som frågor och svar, eftersom Ramverket inte är något samhällssystem. Slutlistorna, källprincipen och formatreglerna gäller ändå.

## 3. En frågegruppssida

1. Sidans titel sätts av bygget och skrivs inte i filen (ingen `#`-rubrik).
2. **5–8 frågor**, var och en som underrubrik (`##`). Hela sidan består av frågor; inga stycken före första frågan.
3. **Sista frågan är alltid "Så vad är egentligen svaret?"** Den knyter ihop sidan och slutar med ett kärnbudskap i fetstil, högst en mening, gärna i formen "Frågan är inte X, utan Y."
4. Sist två listor, i den här ordningen, båda som `##`-rubriker:
   - **Kopplingar till andra delar av samhället**
   - **Externa källor** (bara om sidan har sakpåståenden)

## 4. Frågorna

- Skrivs som läsaren själv skulle fråga, gärna utifrån en vanlig föreställning ("Varför måste ekonomin växa?").
- Varje rubrik är en riktig fråga och slutar med frågetecken. Rubriker som "Bakgrund" används inte.
- Ordningen följer: Hur är det? – Varför är det så? – Måste det vara så? – Vad kan bli annorlunda?
- **Den tänkte läsaren** tror på fortsatt ekonomisk tillväxt. Hans bästa invändning tas upp som en egen fråga och besvaras ärligt, med belägg.
- Formen gäller utan undantag på frågegruppssidorna. Texter som frångår den diskuteras med förvaltaren innan de skrivs.

## 5. Svaren

- 2–4 korta stycken. Svaret på "Så vad är egentligen svaret?" får vara något längre.
- Första meningen svarar direkt: "Ja, i princip.", "Nej.", "Delvis, men mindre än det ser ut."
- Sedan nyansen, sist den systemiska poängen.
- Vardagsspråk. Vardagsexempel först, begreppet efteråt. En fackterm förklaras första gången.
- Punktlistor bara när en uppräkning verkligen behövs. Tabeller får användas för siffror som ska jämföras.
- **Ton:** saklig och respektfull. TSS beskriver hur samhället fungerar och vilka vägar som finns, aldrig vilken väg som är rätt. Ideologier beskrivs efter vad de vaktar, utan partinamn och utan förakt.
- Reformer som nämns ska finnas och ha prövats någonstans, och både det som fungerar och kritiken redovisas.

## 6. Källor

- Definitioner och värderingar behöver ingen källa.
- Mätbara sakpåståenden har källa i listan Externa källor.
- Siffror kontrolleras mot källan innan de skrivs in.
- För ekonomitexterna: bygg på källor som kritikerna respekterar (Riksbanken, Bank of England, IMF, OECD, statliga utredningar). Skilj det säkra från det omdiskuterade. Bygg inte på omstridda teorier som MMT.
- MHS-rapporterna (TSS föregångare) är bakgrund och länkas inte.

## 7. Länkar

**Kontrollregler**
- En intern länk går till sidfilen med relativ sökväg inom vinkelparenteser: `[Planetära gränser – Ramverk](<../../Ramverk/Planetära gränser/Planetära gränser.md>)`. Aldrig en full webbadress till den egna webbplatsen.
- I **Kopplingar** är hela raden "Sida – System" länken, med tankstreck (–). Huvudsidor (systemen, Människan, Ramverk, Vårt samhälle, Samhällsutforskaren) skrivs bara med sitt namn. Visionen och Samhällskartan skrivs "Visionen – Vårt samhälle" och "Samhällskartan – Vårt samhälle".
- Kopplingar länkar till andra system, Ramverk och Människan, inte till sidor i samma system.
- I **Externa källor** är visningstexten (källa, titel, år) själva länken. URL:en skrivs aldrig ut. Rätt: `[IPBES, Global Assessment Report (2019)](https://…)`.

**Skrivregler**
- Länkar till sidor i samma system får stå i brödtexten men behövs inte; de finns i listan "Sidorna i …".
- "o" och "och" får blandas i länktexter.

## 8. Ordval (kontrollregler)

- **"Tillväxt" står aldrig ensamt.** Det ska framgå vad som växer: ekonomisk tillväxt (BNP), BNP-tillväxt, befolkningstillväxt, ökad materialanvändning. Undantag: sidnamnet Tillväxt och utveckling. Bygget varnar.
- **SDGs kallas FN:s hållbarhetsområden (SDGs)**, inte mål, eftersom de saknar tydlig leverans, ansvarig och tidpunkt. De 169 *targets* heter delområden ("punkt 8.1"). Sidan FNs SDGs förklarar ordvalet.
- **Agenda 2030** är FN:s handlingsplan till 2030.
- **Vision** är en riktning som man inte kan säga nej till (som nollvisionen). **Mål** används bara om något med leverans och tidpunkt, eller när källan själv använder ordet.
- **Grundbehov** är det alla människor behöver för att leva värdigt (den sociala grunden i Doughnut Economics). Det som går utöver grundbehoven får inget motsatsbegrepp ("krydda", "lyx" används inte); det beskrivs med vanliga ord.
- "den sociala grunden" (inte "det sociala golvet"), "Samhällskartan" (inte "systemkartan").
- "i stället", inte "istället". "TSS:s" undviks.

## 9. Format

- Rubriker är `##`. Fetstil på en rad i stället för rubrik är ett säkert fel.
- **Fetstil:** nyckelbegrepp första gången det förklaras på sidan, och kärnbudskapet. Aldrig hela stycken, aldrig på frågor, aldrig samtidigt med kursiv.
- **Kursiv:** titlar på böcker och rapporter, engelska termer inom parentes, betoning av enstaka ord.
- Bilder skrivs i ett eget stycke: `![Beskrivning](<Filnamn 2026-10-21.png>)`. Beskrivningen blir alt-text. En ny version får nytt datum i filnamnet. Förklarande bilder görs i 1600 × 1000 pixlar med typsnittet Inter.

## 10. Sidnamn

- Sidans namn = mappens namn = filens namn (`Sida/Sida.md`). Helst högst 30 tecken och unikt. Avslutningsgruppernas namn får vara längre.
- Mappnamnet ger adressen på webbplatsen. Ett namnbyte görs på mappen, filen, `Sidordning.md`, namntabellen i `forvaltning/Ordlista svenska-engelska.md` och alla länkar, i båda språken, samtidigt. Bygget varnar för det som glöms.

## 11. Engelska (TSS-en)

- Svenskan ändras först. Samma ändring förs över till engelskan i samma omgång.
- Termer, sidnamn och principer för översättningen står i `forvaltning/Ordlista svenska-engelska.md`. Brittisk engelska.
- Svenska exempel får stå kvar och ramas in ("In Sweden, …"). Svensk lag görs till ett exempel bland flera.
- Belopp i kronor med euro inom parentes. Svenska källor får engelsk visningstext och "(in Swedish)".

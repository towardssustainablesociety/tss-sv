# Mot ett hållbart samhälle (TSS)

TSS (*Towards Sustainable Society*) är en kunskapswebbplats om ett hållbart samhälle: **ett gott liv för alla, inom planetens gränser**. Den bygger på FN:s globala mål (Agenda 2030), de planetära gränserna och Doughnut Economics, och beskriver samhället som fyra samhällssystem – det ekologiska, det ekonomiska, det sociala och kulturella och det demokratiska – med människan i mitten.

Webbplatsen: <https://sv.towardssustainablesociety.org>

## Ett öppet förråd

TSS är en plattform som vem som helst får använda och bygga vidare på. Visionen är en inbjudan, inte ett juridiskt villkor. TSS är ingen organisation, har ingen finansiering och tar inte ställning för något parti.

## Licens

Texterna och bilderna får användas enligt [Creative Commons Erkännande-DelaLika 4.0 Internationell (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/deed.sv). Ange att materialet kommer från TSS (*Mot ett hållbart samhälle*, sv.towardssustainablesociety.org), länka till licensen, ange om du har ändrat något och dela det du gör av det på samma villkor. Hela licenstexten finns i [LICENSE](LICENSE).

Byggskripten i `bygg/` omfattas av samma licens.

## Vad som finns här

| Mapp | Innehåll |
|---|---|
| `texter/` | Webbplatsens sidor, en mapp per sida. Filen heter som mappen. `Navigera i samhället.docx` anger tills vidare i vilken ordning sidorna under huvudsidan visas. Navigeringen på webbplatsen (toppmenyn, raden som visar var man är och listan över sidorna sist) byggs av mallen. Bilder ligger som PNG i sidans mapp. |
| `bygg/` | `bygg.py` gör om texterna till en statisk webbplats. `mall.html` är sidmallen och `stil.css` utseendet. |
| `.github/workflows/publicera.yml` | Bygger och publicerar webbplatsen på GitHub Pages vid varje ändring i `main`. |

Texterna är i dag docx. De ska bli markdown (förvaltningsplanen, steg 4).

## Hur bygget fungerar

1. Varje docx görs om till HTML med pandoc.
2. Länkar mellan sidorna kommer från den gamla Google Sites-versionen. Bygget känner igen dem på länktexten och gör om dem till webbplatsens egna adresser, till exempel `/samhallsutforskaren/ekologiska-systemet/naturens-kretslopp/`.
3. En rad `[BILD: Namn, beskrivning]` ersätts med den senaste bilden i sidmappen vars filnamn börjar med *Namn*.
4. Bygget skriver också sitemap, robots.txt och CNAME, och listar problem (länkar som inte hittar sin sida, saknade bilder) i loggen för körningen.

Bygga själv (kräver pandoc och python-docx):

```
python3 bygg/bygg.py texter _site               # som på GitHub, skarp version
python3 bygg/bygg.py texter _site --preview     # för att öppna filerna direkt i webbläsaren
python3 bygg/bygg.py texter _site --noindex     # ber sökmotorer att inte indexera
```

## Föreslå en ändring

- Hittar du ett fel, en fråga som saknas eller en bättre källa: öppna ett *issue* här, eller skriv till towards.sustainable.life@gmail.com. Ange sidan och gärna källan.
- Vill du ändra själv: gör en *fork*, ändra och skicka en *pull request*. Förvaltaren granskar varje ändring innan den publiceras.

### Principer för texterna (i korthet)

- Varje samhällssystem beskrivs med frågor och svar. Varje rubrik är en fråga, och sista frågan är "Så vad är egentligen svaret?".
- Mätbara sakpåståenden har källa i listan *Externa källor* sist på sidan. Definitioner och värderingar behöver ingen källa.
- Sidans slut har listan *Kopplingar till andra delar av samhället* och sedan *Externa källor*.
- Tonen är saklig. TSS beskriver hur samhället fungerar och vilka vägar som finns, inte vilken väg som är rätt.

## Förvaltning

TSS grundades och förvaltas av Rolf Thorsell. Förrådet ligger i en GitHub-organisation så att fler kan bli förvaltare och så att arbetet kan lämnas över.

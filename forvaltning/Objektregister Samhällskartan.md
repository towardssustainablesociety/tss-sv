# Objektregister – Samhällskartan

Version 2026-10-29. Ersätter BO-001, som beskrev den gamla rasterbilden.

Kartan är filen [`texter/Vårt samhälle/Samhällskartan/Samhällskartan.svg`](<../texter/Vårt samhälle/Samhällskartan/Samhällskartan.svg>). SVG-filen är originalet. Den visas på startsidan Hållbart samhälle, på Samhällskartan och i sista steget på Vårt samhälle.

## Så ändras kartan

- Ändra i SVG-filen. Texterna är vanlig text och kan bytas direkt. Varje objekt har ett `id`, som står i tabellerna nedan.
- Grundstrukturen ändras inte utan särskilt beslut: Människan i mitten, ringen runt henne, Ekologiska överst, Ekonomiska till vänster, Demokratiska till höger, Sociala och kulturella nederst, planetens gränser runt om och Ramverk längst ner.
- Färgerna och ikonerna hör till systemen och byts inte mellan dem.
- Länkarna skrivs relativt till SVG-filens mapp, som länkarna i sidfilerna. Bygget gör om dem till webbplatsens adresser och larmar om en länk inte hittar sin sida.
- Bågtexterna (gränserna och ringen) följer en osynlig båge, `bage-…`. En längre text kan behöva en längre båge eller mindre text.
- Äldre versioner finns i förrådets historik.
- Den engelska versionen görs genom att texterna byts mot kolumnen Engelska (förslag) nedan, när ordlistan är godkänd.

## Färger

| System | Linje och text | Bakgrund |
|---|---|---|
| Ekologiska, Planetens gränser, Ramverk | #2f6b4f | #e4efe6 (gränsringen #d6e8d6) |
| Ekonomiska | #1f5fae | #e6eef8 |
| Demokratiska | #5b3a8f | #eee8f5 |
| Sociala och kulturella | #d9590f | #fcece2 |
| Människan | #2f6b4f | #fff4d6 |
| Utanför gränserna / innanför gränserna | | #e9f1f6 / #fbf7ee |

## Objekt

### Bakgrund och planetens gränser

| Id | Svenska | Engelska (förslag) | Länk till |
|---|---|---|---|
| `bakgrund` | (ytorna utanför och innanför gränserna) | | |
| `planetens-granser` | PLANETENS GRÄNSER | PLANETARY BOUNDARIES | Planetära gränser – Ramverk |
| `grans-klimat` | Klimatförändring | Climate change | |
| `grans-mangfald` | Förlust av biologisk mångfald | Loss of biodiversity | |
| `grans-mark` | Förändrad markanvändning | Land-system change | |
| `grans-sotvatten` | Sötvatten | Freshwater | |
| `grans-kvave-fosfor` | Kväve- och fosforflöden | Nitrogen and phosphorus flows | |
| `grans-kemiska` | Nya kemiska ämnen | Novel entities | |
| `grans-havsforsurning` | Havsförsurning | Ocean acidification | |
| `grans-ozon` | Ozonskiktet | Ozone layer | |
| `grans-partiklar` | Luftens partiklar | Atmospheric aerosols | |

### De fyra systemen

| Id | Svenska | Engelska (förslag) | Länk till |
|---|---|---|---|
| `system-ekologiska` | EKOLOGISKA SYSTEMET / Livets förutsättningar | THE ECOLOGICAL SYSTEM / The basis of life | Ekologiska systemet |
| `system-ekonomiska` | EKONOMISKA SYSTEMET / Försörjning och resursflöden | THE ECONOMIC SYSTEM / Livelihoods and resource flows | Ekonomiska systemet |
| `system-demokratiska` | DEMOKRATISKA SYSTEMET / Styrning, makt och legitimitet | THE DEMOCRATIC SYSTEM / Governance, power and legitimacy | Demokratiska systemet |
| `system-sociala` | SOCIALA OCH KULTURELLA SYSTEMET / Behov, värderingar och relationer | THE SOCIAL AND CULTURAL SYSTEM / Needs, values and relationships | Sociala o kulturella systemet |
| `samband` | (fyra dubbelriktade pilar mellan systemen) | | |

Ikoner, ritade i filen: träd (Ekologiska), staplar (Ekonomiska), grupp (Demokratiska), hjärta (Sociala och kulturella), tre personer (Människan).

### Mitten

| Id | Svenska | Engelska (förslag) | Länk till |
|---|---|---|---|
| `doughnut` | Det ekologiska taket – planetens gränser / Den sociala grunden – alla människors grundbehov | The ecological ceiling – planetary boundaries / The social foundation – everyone's basic needs | Doughnut Economics – Ramverk |
| `manniskan` | MÄNNISKAN / i det hållbara samhället | PEOPLE / in the sustainable society | Människan |

### Ramverk

| Id | Svenska | Engelska (förslag) | Länk till |
|---|---|---|---|
| `ramverk` | RAMVERK | FRAMEWORK | Ramverk |
| `ramverk-sdgs` | FN:s SDGs | The UN SDGs | FNs SDGs – Ramverk |
| `ramverk-doughnut` | Doughnut Economics | Doughnut Economics | Doughnut Economics – Ramverk |
| `ramverk-planetara` | Planetära gränser | Planetary boundaries | Planetära gränser – Ramverk |

De engelska termerna för gränserna, *social foundation* och *ecological ceiling* följer originalkällorna (Stockholm Resilience Centre och Kate Raworth). Övriga engelska texter är förslag som godkänns i ordlistan för TSS-en.

## Delningsbilden

`texter/Hållbart samhälle/Hållbart samhälle delningsbild 1200x630.png` är bilden som visas när en sida delas i sociala medier. Den görs från SVG-kartan och ska göras om när kartan ändras.

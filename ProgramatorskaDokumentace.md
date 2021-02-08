# Qournal

## Struktura

Soubory `main.py` a `Models.py`.

V `Models.py` jsou definice pomocných tříd.

V `main.py` jsou definice příkazů a hlavní cyklus programu.

Stav aplikace se ukládá do proměnné state v main.py, stav je dict objektů Area přičemž klíčem je jméno Area.

Data jsou ve formě vnořených dictů, aby se zpřímočařila serializace do JSONu, která se však ukázala příliš složitá a
neflexibilní, takže jsem použil knihovnu jsonpickle.

### `Models.py`

`AreaTypes`

- konstanty druhů Area 1->checklist, 2->strukturovaná data, 3-> volný text (klasický deník)

`Area`

- jméno
- typ
- dict objektů ItemTemplate, kde klíč je název
- dict objektů Day, kde klíčem je datum. ve kterém jsou klíče enabled, kde je uloženo jestli se má ItemTemplate
  zaznamovat a zobrazovat; Area

`Day`

- datum
- dict itemů, kde klíč je jméno itemu

`ItemTemplate`

- jméno
- dict metainformací, kde klíče jsou 'enabled': jestli je item zobrazen a zaznamenáván, 'question': jak se progam ptá
  při záznamu dat

`Item`

- jméno
- zaznamenaná data

`Command`

- pomocná třída na zprcování příkazů

`ArgumentError(ValueError)`

- vyjímky na míru

### `main.py`

`MainLoop`

- parsuje a vyvolává příkazové funkce, když nastane výjimka, tak ji odchytí a vypíše a když jinak chybuje

Většina příkazových funkcí je přímočará a jsou vystiženy docstringem. Většinou se v nich nachází validace vstupu a
samotná akce, která pracuje se stavem.

`DisplayArea`

- je nutné spočitat šířky sloupců jako maximum z délek jména a odpovědí, pak se vypíší data do tabulky, ve které se musí
  použít správná šířka mezer. Také se ošetří přeskočení sloupců, které nejsou enabled.

`ChangeArea`

- obsahuje příkazové funkce ChangeItemTemplate a AddItemTemplate
- tvoří podprogram s vlastním cyklem příkazů na přidání nebo změnu ItemTemplate, odstranění se řeší metadatem 'enabled'
  v měnění

`SaveState` a `RecoverState`

- používají jsonpickle na uložení/načtení stavu
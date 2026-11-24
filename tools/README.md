# tools — инструменты разработки (для ИИ, не для студии)
Работают из папки `tools/`. Нужны: Python 3 + Pillow, Node + Playwright (`/opt/npm-tools`), Chrome. Сеть для установки не нужна.

| Файл | Что делает |
|---|---|
| `sh serve.sh &` | запускает сервер на :8765 (корень репозитория). Остановить: `pkill -f "http.server 8765"` |
| `LANGF=lang/story_11.ru.json python3 cs.py story_11_s03 1,5,9,14` | контактный лист кадров сцены → `shots/cs_<сцена>.png` (печатает errors/warnings/dur) |
| `node rs.js <сцена> <lang.json> <t1,t2> [префикс]` | отдельные кадры PNG в `shots/` |
| `node hashes.js out.json demo_01 demo_02 ep01_s01 …` | хэши кадров для регрессии; сравнить с `baseline_hashes.json` — старые сцены должны совпасть 1 в 1 |
| `gen/*.py` | генераторы реквизита и сцен сюжетов 4–11 (`sNlib.py` — предметы в library.json, `sNscenes.py` — сцены, тексты в `lang/`). Запускать из `tools/gen/`: `python3 s11lib.py && python3 s11scenes.py` |

Порядок работы над сюжетом: lib → scenes → cs.py по каждой сцене → hashes.js (diff 0) → manifest → docs → commit.
Генераторы переписывают library.json и сцены целиком, поэтому повторный запуск безопасен.

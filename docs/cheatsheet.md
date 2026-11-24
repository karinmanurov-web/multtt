# Шпаргалка аниматора (читать первой, ~2 минуты)
Подробности: `ai2_animator.md`. Ловушки движка: `gotchas.md`. Реквизит: `props_index.md`.

**Кадр** 1080×1920, земля y=1250. В сцене нет слов: реплики `say` берут текст из `lang/*.json` по ключу. Закадровый голос — скрытый статист `narr` (`{"type":"extra","x":540,"face":"left","hidden":true}`) и `say who:"narr"`.
**Герои:** `eng` Инженер, `bld` Строитель, `arch` Архитекторша (`{"type":"arch"}` у статиста, id любой, в портрете только боковой вид). Остальные — статисты `extra` с `defs.characters`.

**Минимальная сцена**
```json
{"id":"story_NN_s01","duration":12,"start":{"location":"field","chars":{"eng":{"x":170,"face":"right"}}},"defs":{},
 "beats":[{"t":0.3,"do":"say","who":"eng","line":"n01","dur":2.4}]}
```
**Бит** = `{"t":сек,"do":…}`. Главные: `place walk face pose emote say spawn hold release move remove camera portrait shake fx title marker location view outfit angle`.
**Предметы:** `spawn` (id, prop, x, y мировой, scale, rot°, layer back|front) → `hold` в руку (`who`, `hand`) → `release` / `move` / `remove`. Крупный план эскиза: `spawn` с `scale≈2.6` на `back`.
**Камера:** `{"do":"camera","x":540,"y":850,"zoom":0.8,"dur":1}`; zoom<1 — свободный, zoom≥1 прижат к краям мира.
**Реплика:** `dur` в `say` можно не писать — время = символов/cps + 0,15 с (cps в языковом файле, на нужном языке). Следующие действия по-прежнему стоят на фиксированных `t`: после реплики сдвигай их сам. Если `dur` задан и короче речи — предупреждение.

**Порядок работы над сюжетом:** реквизит (`tools/gen/sNlib.py` → library.json) → сцены (`sNscenes.py`) → `tools/cs.py` по каждой сцене → `tools/hashes.js` (старые сцены diff 0) → manifest.json (`id`,`title` «Сюжет №N · Название · sNN · Сцена»,`file`,`langs`) → docs → commit → push → проверить деплой. После правок `engine.js` повысить `?v=` в `index.html`.

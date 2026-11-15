# Operación Extracción – FPS 3D (Three.js)

Curso: Computación Gráfica y Visual – UPN · Evaluación T3
Autor: Marlon Aguero (completar nombre y código)

Videojuego de disparos en primera persona. Sobrevives a una zona infestada de zombis, administras tu munición y llegas a la **zona de extracción** (cilindro verde con haz de luz) al final del recorrido.

## Ejecutar
El juego carga archivos `.glb`, por lo que **debe abrirse desde un servidor local** (no con doble clic en `index.html`). Se necesita internet (Three.js se carga desde CDN).

**Opción A – VS Code (recomendada):** abrir la carpeta con *File → Open Folder*, instalar la extensión **Live Server** (Ritwick Dey) y pulsar **Go Live**.

**Opción B – Windows:** doble clic en `iniciar_juego.bat` (requiere Python) y abrir `http://localhost:8000`.

**Opción C – Terminal:** `python -m http.server 8000` y abrir `http://localhost:8000`.

*Opcional:* publicar con **GitHub Pages** (Settings → Pages → rama `main`, carpeta `/root`).

## Controles
| Tecla | Acción |
|---|---|
| W / S / A / D | Avanzar / retroceder / izquierda / derecha |
| Mouse | Orientar la cámara |
| Clic izquierdo | Un disparo por clic (no hay autofuego) |
| 1 / 2 | Pistola / Rifle |
| R | Reiniciar (tras Game Over o victoria) |

## Reglas
- Cada arma tiene su propio contador (Pistola 12, Rifle 20). Cada disparo consume 1; a 0 no se puede disparar.
- Las balas solo se recuperan con **cajas del escenario**: amarillas = pistola (+10), azules = rifle (+12).
- Cada zombi tiene 2 puntos de resistencia; muere con exactamente 2 impactos válidos.
- Los zombis están inactivos hasta que entras en su rango (16 m; corredores rojos 22 m y más veloces).
- Si un zombi te toca: **GAME OVER**. Si llegas a la zona verde: **¡MISIÓN COMPLETADA!**

## Dónde está cada requerimiento (`index.html`)
| RF | Implementación |
|---|---|
| RF01 armas GLB, teclas 1/2, 1 disparo por clic | `WEAPONS`, `select()`, evento `mousedown` + `shoot()` |
| RF02 / RF10 municiones y cajas | `ammo[]`, bloqueo en `shoot()`, `pickups` |
| RF03 / RF08 nivel (inicio, 7 tramos en zigzag, extracción) | sección *NIVEL*, `addBox()`, `goal` |
| RF04 / RF05 zombis GLB, estado idle/chase | `zombies`, bucle `update()` |
| RF06 cámara FPS | `yaw/pitch`, arma como hija de `camera` |
| RF07 colisiones de disparo | `Raycaster` desde el centro, `hit()`; las paredes bloquean el disparo |
| RF09 Game Over | `end('over')`, detección por distancia `catchDist` |
| RF11 dificultad | zombis distribuidos por tramo, corredores, munición limitada |

Colisiones jugador/zombi–paredes: AABB con deslizamiento por ejes (`blocked()`).

## Modelos 3D y fuentes de recursos externos
- **Modelos GLB (armas y zombis):** generados con el script propio `gen_models.py` (autoría propia, sin licencias externas). Se pueden reemplazar por modelos descargados con el mismo nombre en `models/`; el código los escala automáticamente (`len` para armas, `zombieHeight` para zombis; `rotY` en `WEAPONS` si salen girados).
- **Texturas:** generadas por código (canvas), sin archivos externos.
- **Sonidos:** sintetizados con la Web Audio API.
- **Librería:** [Three.js](https://threejs.org/) r160 (licencia MIT), cargada desde jsDelivr.
- *Si usas modelos de terceros, agrégalos aquí con autor, enlace y licencia (ej.: «Zombie Apocalypse Kit – Quaternius – CC0»).*

## Estructura
```
index.html  iniciar_juego.bat  gen_models.py  models/*.glb  README.md
```

## Guion sugerido para el video (≤ 3 min)
1. (0:00–0:20) Presentación y objetivo del juego.
2. (0:20–1:10) Explicación técnica: `shoot()` (raycasting + pared que bloquea) y `hit()` (2 impactos) o el estado idle/chase.
3. (1:10–2:40) Demo: WASD/mouse, cambio de arma, un disparo por clic, munición en 0, recoger caja, zombi inactivo vs activo, matar con 2 disparos, Game Over y victoria.

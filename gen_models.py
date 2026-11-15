"""Genera modelos .glb simples (cajas con color) para armas y zombis.
Uso: python gen_models.py   ->  crea la carpeta models/
Puedes reemplazar los .glb por modelos descargados (Quaternius, Kenney, Sketchfab...)."""
import json, struct, os

def box(sx, sy, sz, cx, cy, cz):
    h, c, P, N, I = (sx/2, sy/2, sz/2), (cx, cy, cz), [], [], []
    for a in range(3):
        u, v = (a+1) % 3, (a+2) % 3
        for s in (-1, 1):
            n = [0, 0, 0]; n[a] = s; b = len(P)
            for du, dv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                p = [0, 0, 0]; p[a] = s*h[a]; p[u] = du*h[u]; p[v] = dv*h[v]
                P.append([p[i]+c[i] for i in range(3)]); N.append(n)
            I += [b, b+1, b+2, b, b+2, b+3] if s > 0 else [b, b+2, b+1, b, b+3, b+2]
    return P, N, I

def glb(parts, path):
    blob, views, accs, prims, mats = bytearray(), [], [], [], []
    for k, (dims, col) in enumerate(parts):
        P, N, I = box(*dims)
        data = [(b''.join(struct.pack('<3f', *p) for p in P), 34962),
                (b''.join(struct.pack('<3f', *n) for n in N), 34962),
                (struct.pack('<%dH' % len(I), *I), 34963)]
        ids = []
        for d, t in data:
            views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": len(d), "target": t})
            blob += d; blob += b'\0' * ((4 - len(blob) % 4) % 4); ids.append(len(views)-1)
        a0 = len(accs)
        accs += [{"bufferView": ids[0], "componentType": 5126, "count": len(P), "type": "VEC3",
                  "min": [min(p[i] for p in P) for i in range(3)], "max": [max(p[i] for p in P) for i in range(3)]},
                 {"bufferView": ids[1], "componentType": 5126, "count": len(N), "type": "VEC3"},
                 {"bufferView": ids[2], "componentType": 5123, "count": len(I), "type": "SCALAR"}]
        rgb = [((col >> s) & 255)/255 for s in (16, 8, 0)]
        mats.append({"pbrMetallicRoughness": {"baseColorFactor": rgb+[1], "metallicFactor": .2, "roughnessFactor": .7}})
        prims.append({"attributes": {"POSITION": a0, "NORMAL": a0+1}, "indices": a0+2, "material": k})
    j = {"asset": {"version": "2.0", "generator": "gen_models.py"}, "scene": 0, "scenes": [{"nodes": [0]}],
         "nodes": [{"mesh": 0}], "meshes": [{"primitives": prims}], "materials": mats, "accessors": accs,
         "bufferViews": views, "buffers": [{"byteLength": len(blob)}]}
    js = json.dumps(j).encode(); js += b' ' * ((4 - len(js) % 4) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    with open(path, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total))
        f.write(struct.pack('<I4s', len(js), b'JSON') + js)
        f.write(struct.pack('<I4s', len(blob), b'BIN\0') + bytes(blob))

def zombie(shirt, skin, pants):  # mira hacia +Z, brazos extendidos
    parts = [((.2, .8, .22, -.13, .4, 0), pants), ((.2, .8, .22, .13, .4, 0), pants),
             ((.55, .7, .3, 0, 1.15, 0), shirt), ((.3, .3, .3, 0, 1.7, .03), skin),
             ((.14, .14, .7, -.38, 1.35, .4), skin), ((.14, .14, .7, .38, 1.35, .4), skin),
             ((.06, .05, .02, -.08, 1.73, .185), 0xffee33), ((.06, .05, .02, .08, 1.73, .185), 0xffee33)]
    return parts

os.makedirs('models', exist_ok=True)
# Armas: el cañón apunta hacia -Z
glb([((.05, .06, .26, 0, .05, -.13), 0x8a1c1c), ((.045, .04, .22, 0, 0, -.11), 0x5a1010),
     ((.05, .13, .07, 0, -.07, -.03), 0x2a8a3a)], 'models/pistol.glb')
glb([((.06, .09, .5, 0, 0, -.25), 0x8a1c1c), ((.025, .025, .35, 0, .02, -.675), 0x1a1a1a),
     ((.05, .12, .25, 0, -.02, .12), 0x5a1010), ((.04, .16, .07, 0, -.12, -.3), 0x2a8a3a),
     ((.045, .1, .05, 0, -.09, -.02), 0x222222), ((.03, .04, .1, 0, .065, -.3), 0xd9b400)], 'models/rifle.glb')
glb(zombie(0x4a4a3a, 0x6f8f5a, 0x2b3a55), 'models/zombie.glb')
glb(zombie(0x8a1f1f, 0x9a7a5a, 0x222222), 'models/zombie_runner.glb')
print('Modelos generados en ./models')

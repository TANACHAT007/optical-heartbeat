# Optical Heartbeat Detector — one-piece device: base tray + lid with finger pod (mm). Rebuilds in a new doc.
import adsk.core, adsk.fusion, os
app = adsk.core.Application.get()
P = os.path.expanduser('~/fusion-projects/optical-heartbeat/')
V = lambda x, y, z: adsk.core.Point3D.create(x/10, y/10, z/10)
bm = adsk.fusion.TemporaryBRepManager.get()
B = adsk.fusion.BooleanTypes

def box(x0, y0, z0, x1, y1, z1):
    bb = adsk.core.OrientedBoundingBox3D.create(V((x0+x1)/2, (y0+y1)/2, (z0+z1)/2),
        adsk.core.Vector3D.create(1, 0, 0), adsk.core.Vector3D.create(0, 1, 0), (x1-x0)/10, (y1-y0)/10, (z1-z0)/10)
    return bm.createBox(bb)
def cyl(x, y, z0, z1, d):
    return bm.createCylinderOrCone(V(x, y, z0), d/20, V(x, y, z1), d/20)
def add(b, c): bm.booleanOperation(b, c, B.UnionBooleanType); return b
def cut(b, c): bm.booleanOperation(b, c, B.DifferenceBooleanType); return b

# parameters
W, D, H = 172, 74, 30          # outer base
T = 2.5                        # wall / floor
UNO = (5, 10.35)               # UNO PCB origin (68.6 x 53.3)
HOLES = [(14, 2.5), (15.3, 50.7), (66.1, 7.6), (66.1, 35.5)]
CORN = [(5.5, 5.5), (166.5, 5.5), (5.5, 68.5), (166.5, 68.5)]
POST = 5
FP = (122, 37)                 # finger pod centre on lid
LED_DX = 5.5                   # LED / phototransistor offset from pod centre

doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
des = adsk.fusion.Design.cast(app.activeProduct)
des.designType = adsk.fusion.DesignTypes.DirectDesignType
root = des.rootComponent

# ---- base
base = box(0, 0, 0, W, D, H)
cut(base, box(T, T, T, W-T, D-T, H+1))
for x, y in CORN: add(base, cyl(x, y, T/2, H-3, 7))
for hx, hy in HOLES: add(base, cyl(UNO[0]+hx, UNO[1]+hy, T/2, T+POST, 7))
# breadboard retaining corners (assumed half-size 85 x 55)
for bx in (80, 163):
    for by in (9.5, 61.5):
        add(base, box(bx, by, T/2, bx+2, by+3, T+5))
for x, y in CORN: cut(base, cyl(x, y, H-9, H+1, 4.0))                 # M3 heat-set pilot
for hx, hy in HOLES: cut(base, cyl(UNO[0]+hx, UNO[1]+hy, T+POST-5, T+POST+1, 2.8))
# connector cut-outs on -X wall: USB-B and DC jack
cut(base, box(-1, UNO[1]+38.1-7.5, T+POST+1.6, T+1, UNO[1]+38.1+7.5, T+POST+1.6+12.5))
cut(base, box(-1, UNO[1]+7.5-5, T+POST+1.6, T+1, UNO[1]+7.5+5, T+POST+1.6+11))
# top face vents (+Y wall slots)
for i in range(6): cut(base, box(40+i*8, D-T-1, 10, 44+i*8, D+1, 22))

# ---- lid
LZ = H                         # lid sits on rim
lid = box(0, 0, LZ, W, D, LZ+T)
add(lid, box(T+0.3, T+0.3, LZ-3, W-T-0.3, D-T-0.3, LZ))              # locating lip
cut(lid, box(T+2.3, T+2.3, LZ-4, W-T-2.3, D-T-2.3, LZ-0.01))         # hollow lip
for x, y in CORN:
    add(lid, cyl(x, y, LZ-3, LZ, 8)) if False else None
    cut(lid, cyl(x, y, LZ-1, LZ+T+1, 3.4))
    cut(lid, cyl(x, y, LZ+T-1.2, LZ+T+1, 6.4))
# finger pod
fx, fy = FP
add(lid, box(fx-14, fy-13, LZ+T, fx+14, fy+13, LZ+T+5))
cut(lid, box(fx-10.5, fy-9.5, LZ+T+3, fx+10.5, fy+9.5, LZ+T+6))     # finger well
cut(lid, cyl(fx-LED_DX, fy, LZ-1, LZ+T+4, 5.2))                       # IR LED
cut(lid, cyl(fx+LED_DX, fy, LZ-1, LZ+T+4, 5.2))                       # phototransistor
add(lid, box(fx-0.7, fy-9, LZ-6, fx+0.7, fy+9, LZ))                   # light barrier rib under lid
add(lid, box(fx-14, fy-13, LZ-6, fx+14, fy-12, LZ)) if False else None
# OLED 0.96" module (27.3 x 27.8, holes 23.5 x 23.8 M2) seen through a window in the lid
DP = (52, 37)
for dx in (-11.75, 11.75):
    for dy in (-11.9, 11.9):
        add(lid, cyl(DP[0]+dx, DP[1]+dy, LZ-4, LZ, 5))
        cut(lid, cyl(DP[0]+dx, DP[1]+dy, LZ-4.5, LZ-0.5, 1.8))
cut(lid, box(DP[0]-12.5, DP[1]+1-6.5, LZ-1, DP[0]+12.5, DP[1]+1+6.5, LZ+T+1))
# beat indicator LED hole (3 mm)
cut(lid, cyl(fx+22, fy+8, LZ-1, LZ+T+1, 3.2))

def comp(name, brep, ox=0):
    c = root.occurrences.addNewComponent(adsk.core.Matrix3D.create()).component
    c.name = name
    b = c.bRepBodies.add(brep); b.name = name
    return c
cb = comp('print_base', base)
cl = comp('print_lid', lid)

# colours / lid exploded offset for preview (lid shown on top)
os.makedirs(P+'04_print_stl', exist_ok=True); os.makedirs(P+'06_cad_export', exist_ok=True)
em = des.exportManager
for c in (cb, cl):
    o = em.createSTLExportOptions(c, P+'04_print_stl/'+c.name+'.stl')
    o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
    em.execute(o)
em.execute(em.createSTEPExportOptions(P+'06_cad_export/optical_heartbeat.step'))
vp = app.activeViewport
vp.viewOrientation = adsk.core.ViewOrientations.IsoTopRightViewOrientation
vp.fit()
print('BUILD_OK', [b.volume for b in cb.bRepBodies], [b.volume for b in cl.bRepBodies])

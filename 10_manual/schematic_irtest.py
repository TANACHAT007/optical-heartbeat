import schemdraw, schemdraw.elements as e
from schemdraw import Drawing
D='/Users/tanachat.s/fusion-projects/optical-heartbeat/10_manual/'
d=Drawing(unit=3); d.config(fontsize=11,font='Thonburi')
# IR transmitter
d += e.Vdd().at((0,5)).label('+5V')
d += e.Resistor().down().label('R220','right',ofst=(0.1,-0.2))
d += e.LED().down().label('IR LED 940nm','right')
d += e.Line().down(0.3)
d += (Q1:=e.BjtNpn().anchor('collector').right().label('Q1 BC548','right',ofst=(0.1,0)))
d += e.Ground().at(Q1.emitter)
d += e.Resistor().at(Q1.base).left().label('R1k','top'); d += e.Dot(open=True).label('Arduino D9','left')
# receiver
d += e.Vdd().at((9,5)).label('+5V')
d += e.Line().down(0.4)
d += (PT:=e.NpnPhoto().anchor('collector').right().label('phototransistor\nขายาว = collector','left',ofst=(-0.1,0)))
d += e.Line().at(PT.emitter).down(0.8)
d += e.Dot(); n=d.here
d += e.Label().at((n[0]-1.0,n[1]-0.2)).label('NPT',fontsize=11)
d += e.Line().at(n).right(2.0); d += e.Dot(open=True).label('Arduino A0','right')
d += e.Resistor().at(n).down().label('R10k','right',ofst=(0.1,-0.3)); d += e.Ground()
d += e.Label().at((4.2,6.0)).label('แสง IR (หันหน้าเข้าหากัน ห่าง 1–2 ซม.)',fontsize=11,color='#c60')
d.save(D+'schematic_irtest.png',dpi=130); print('ok')

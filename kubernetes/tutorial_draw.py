"""Drawing primitives, custom flowables, and all diagram builders."""
import math
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon
from reportlab.graphics import renderPDF

W, H = A4
BLU = colors.HexColor("#326CE5"); DRK = colors.HexColor("#1A1A2E")
TEL = colors.HexColor("#00B4D8"); LIT = colors.HexColor("#E8F4FD")
GRN = colors.HexColor("#34A853"); ORG = colors.HexColor("#FBBC04")
RED = colors.HexColor("#EA4335"); GRY = colors.HexColor("#F1F3F4")
MID = colors.HexColor("#5F6368"); BOX = colors.HexColor("#DADCE0")
WHT = colors.white

def arw(d, x1, y1, x2, y2, c=MID, w=1.5):
    d.add(Line(x1,y1,x2,y2,strokeColor=c,strokeWidth=w))
    a=math.atan2(y2-y1,x2-x1); s=7
    d.add(Polygon([x2-s*math.cos(a-.4),y2-s*math.sin(a-.4),x2,y2,
                   x2-s*math.cos(a+.4),y2-s*math.sin(a+.4)],
                  fillColor=c,strokeColor=c,strokeWidth=0))

def bx(d,x,y,w,h,f=LIT,s=BLU,r=6,sw=1.5):
    d.add(Rect(x,y,w,h,rx=r,ry=r,fillColor=f,strokeColor=s,strokeWidth=sw))

def lbl(d,x,y,t,sz=9,c=DRK,bold=False,a='middle'):
    d.add(String(x,y,t,fontName='Helvetica-Bold' if bold else 'Helvetica',
                 fontSize=sz,fillColor=c,textAnchor=a))

def hex_pod(d,cx,cy,r=20,fill=BLU,text="Pod"):
    pts=[]
    for i in range(6):
        a=math.radians(60*i-30)
        pts+=[cx+r*math.cos(a),cy+r*math.sin(a)]
    d.add(Polygon(pts,fillColor=fill,strokeColor=WHT,strokeWidth=2))
    lbl(d,cx,cy-4,text,7,WHT,True)


class ChapterHeader(Flowable):
    def __init__(self,num,title,sub=""):
        super().__init__(); self.num=num; self.title=title; self.sub=sub
        self.width=W-4*cm; self.height=2.8*cm
    def draw(self):
        w,h=self.width,self.height
        self.canv.setFillColor(BLU)
        self.canv.roundRect(0,0,w,h,10,fill=1,stroke=0)
        self.canv.setFillColor(WHT)
        self.canv.circle(1.5*cm,h/2,.75*cm,fill=1,stroke=0)
        self.canv.setFillColor(BLU); self.canv.setFont('Helvetica-Bold',18)
        self.canv.drawCentredString(1.5*cm,h/2-7,str(self.num))
        self.canv.setFillColor(WHT); self.canv.setFont('Helvetica-Bold',20)
        self.canv.drawString(3*cm,h/2+4,self.title)
        if self.sub:
            self.canv.setFont('Helvetica',10)
            self.canv.setFillColor(colors.HexColor("#BDD7FF"))
            self.canv.drawString(3*cm,h/2-11,self.sub)


class CodeBlock(Flowable):
    def __init__(self,code,title="",width=None):
        super().__init__(); self.code=code; self.title=title
        self._w=width or (W-4*cm)
        self.height=len(code.split('\n'))*14+24+(20 if title else 0)
    def draw(self):
        w,h=self._w,self.height
        self.canv.setFillColor(colors.HexColor("#1E1E2E"))
        self.canv.roundRect(0,0,w,h,8,fill=1,stroke=0)
        if self.title:
            self.canv.setFillColor(colors.HexColor("#313244"))
            self.canv.roundRect(0,h-20,w,20,8,fill=1,stroke=0)
            self.canv.setFillColor(colors.HexColor("#CDD6F4"))
            self.canv.setFont('Helvetica-Bold',9)
            self.canv.drawString(10,h-14,self.title)
        for i,col in enumerate(["#FF5F56","#FFBD2E","#27C93F"]):
            self.canv.setFillColor(colors.HexColor(col))
            self.canv.circle(w-18+i*10,h-10,4,fill=1,stroke=0)
        KW={'apiVersion','kind','metadata','spec','name','namespace','labels',
            'selector','template','containers','image','ports','replicas',
            'strategy','type','resources','requests','limits','env',
            'volumeMounts','volumes','matchLabels','app','schedule',
            'restartPolicy','serviceName','completions','backoffLimit'}
        y=h-(28 if self.title else 16)
        for line in self.code.split('\n'):
            s=line.lstrip(); ind=len(line)-len(s); x=10+ind*6
            if ':' in s and not s.startswith('#') and not s.startswith('-'):
                k,_,v=s.partition(':')
                kc=colors.HexColor("#89B4FA") if k.strip() in KW else colors.HexColor("#CBA6F7")
                self.canv.setFillColor(kc); self.canv.setFont('Courier-Bold',8.5)
                self.canv.drawString(x,y,k+':')
                if v.strip():
                    self.canv.setFillColor(colors.HexColor("#A6E3A1"))
                    self.canv.setFont('Courier',8.5)
                    self.canv.drawString(x+self.canv.stringWidth(k+':','Courier-Bold',8.5)+3,y,v)
            elif s.startswith('#'):
                self.canv.setFillColor(colors.HexColor("#585B70"))
                self.canv.setFont('Courier-Oblique',8.5); self.canv.drawString(10,y,line)
            else:
                self.canv.setFillColor(colors.HexColor("#CDD6F4"))
                self.canv.setFont('Courier',8.5); self.canv.drawString(10,y,line)
            y-=14


class DiagramF(Flowable):
    def __init__(self,d): super().__init__(); self.d=d; self.width=d.width; self.height=d.height
    def draw(self): renderPDF.draw(self.d,self.canv,0,0)


def make_styles():
    b=getSampleStyleSheet(); S={}
    S['h1']=ParagraphStyle('H1',parent=b['Normal'],fontSize=22,textColor=BLU,fontName='Helvetica-Bold',spaceAfter=6,spaceBefore=12,leading=26)
    S['h2']=ParagraphStyle('H2',parent=b['Normal'],fontSize=14,textColor=DRK,fontName='Helvetica-Bold',spaceAfter=4,spaceBefore=8,leading=18)
    S['h3']=ParagraphStyle('H3',parent=b['Normal'],fontSize=11,textColor=BLU,fontName='Helvetica-Bold',spaceAfter=3,spaceBefore=6)
    S['body']=ParagraphStyle('Body',parent=b['Normal'],fontSize=10,textColor=DRK,leading=15,spaceAfter=6,alignment=TA_JUSTIFY)
    S['bullet']=ParagraphStyle('Bul',parent=b['Normal'],fontSize=10,textColor=DRK,leading=14,leftIndent=14,firstLineIndent=-10,spaceAfter=3)
    S['caption']=ParagraphStyle('Cap',parent=b['Normal'],fontSize=8.5,textColor=MID,alignment=TA_CENTER,fontName='Helvetica-Oblique',spaceAfter=8,spaceBefore=2)
    S['callout']=ParagraphStyle('Call',parent=b['Normal'],fontSize=9.5,textColor=colors.HexColor("#1B4332"),leading=14,backColor=colors.HexColor("#D8F3DC"),borderColor=GRN,borderWidth=1,borderPad=8,spaceAfter=8,spaceBefore=4,leftIndent=8,rightIndent=8)
    S['warn']=ParagraphStyle('Warn',parent=b['Normal'],fontSize=9.5,textColor=colors.HexColor("#7B2D00"),leading=14,backColor=colors.HexColor("#FFF3E0"),borderColor=ORG,borderWidth=1,borderPad=8,spaceAfter=8,spaceBefore=4,leftIndent=8,rightIndent=8)
    return S


# ── Diagrams ──────────────────────────────────────────────────────────────

def d_hierarchy():
    dw,dh=480,190; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    bx(d,8,8,464,174,f=colors.HexColor("#E3F2FD"),s=BLU,r=10,sw=2)
    lbl(d,240,170,"Cluster",10,BLU,True)
    bx(d,25,18,430,148,f=colors.HexColor("#FEF9E7"),s=ORG,r=8,sw=1.5)
    lbl(d,240,155,"Node  (VM / bare-metal)",9,ORG,True)
    bx(d,45,30,195,120,f=colors.HexColor("#EAF6FF"),s=TEL,r=6)
    lbl(d,142,140,"Pod",9,TEL,True)
    for cx,tag in [(95,"app :8080"),(185,"sidecar :9090")]:
        bx(d,cx-40,42,80,72,f=WHT,s=BLU,r=4)
        lbl(d,cx,95,tag.split()[0],9,DRK,True); lbl(d,cx,83,tag.split()[1],8,TEL)
    bx(d,265,30,170,120,f=colors.HexColor("#EAF6FF"),s=TEL,r=6)
    lbl(d,350,140,"Pod",9,TEL,True)
    bx(d,285,50,130,72,f=WHT,s=BLU,r=4)
    lbl(d,350,93,"nginx :80",9,DRK,True)
    return d

def d_pod_lifecycle():
    dw,dh=480,130; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    states=[(55,65,"Pending",ORG),(165,65,"Running",GRN),(285,65,"Succeeded",BLU),(400,65,"Failed",RED)]
    for x,y,n,c in states:
        bx(d,x-42,y-22,84,44,f=c,s=c,r=22); lbl(d,x,y-5,n,9,WHT,True)
    for i in range(3): arw(d,states[i][0]+44,65,states[i+1][0]-44,65)
    d.add(Line(165,43,165,15,strokeColor=RED,strokeWidth=1.5))
    d.add(Line(165,15,400,15,strokeColor=RED,strokeWidth=1.5))
    arw(d,400,15,400,43,c=RED); lbl(d,280,8,"container exits non-zero",8,RED)
    return d

def d_rolling():
    dw,dh=480,210; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,202,"Rolling Update — maxSurge:1 | maxUnavailable:0",10,DRK,True)
    steps=[("Step 1\nInitial",3,0),("Step 2\n+1 new",3,1),("Step 3\n-1 old",2,1),("Step 4\n+1 new",2,2),("Step 5\nFinal",0,3)]
    cw=480/5; r=13
    for ci,(title,v1,v2) in enumerate(steps):
        cx=ci*cw+cw/2; t1,t2=title.split('\n')
        lbl(d,cx,192,t1,8,DRK,True); lbl(d,cx,181,t2,7.5,MID)
        for i in range(v1):
            py=162-i*36; pts=[]
            for k in range(6): a=math.radians(60*k-30); pts+=[cx+r*math.cos(a),py+r*math.sin(a)]
            d.add(Polygon(pts,fillColor=BLU,strokeColor=WHT,strokeWidth=1.5)); lbl(d,cx,py-4,"v1",7,WHT,True)
        for i in range(v2):
            py=162-(v1+i)*36; pts=[]
            for k in range(6): a=math.radians(60*k-30); pts+=[cx+r*math.cos(a),py+r*math.sin(a)]
            d.add(Polygon(pts,fillColor=GRN,strokeColor=WHT,strokeWidth=1.5)); lbl(d,cx,py-4,"v2",7,WHT,True)
        if ci<4: arw(d,cx+cw/2-8,100,cx+cw/2+8,100)
    return d

def d_statefulset():
    dw,dh=480,200; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,193,"StatefulSet — stable identity + dedicated PVC per Pod",10,DRK,True)
    bx(d,30,10,420,24,f=BLU,s=BLU,r=5)
    lbl(d,240,19,"Headless Service → web-0.svc | web-1.svc | web-2.svc",9,WHT,True)
    pods=[(90,120,"web-0"),(240,120,"web-1"),(390,120,"web-2")]
    for cx,cy,n in pods:
        hex_pod(d,cx,cy,r=26,fill=TEL,text=n)
        arw(d,cx,34,cx,94,c=BLU)
        bx(d,cx-30,cy-88,60,34,f=colors.HexColor("#FFF8E1"),s=ORG,r=4)
        lbl(d,cx,cy-66,"PVC",8.5,ORG,True); lbl(d,cx,cy-77,f"data-{n}",7,MID)
        arw(d,cx,cy-26,cx,cy-54,c=ORG)
    arw(d,118,120,210,120); arw(d,268,120,360,120)
    lbl(d,165,128,"ordered →",8,MID); lbl(d,315,128,"ordered →",8,MID)
    return d

def d_daemonset():
    dw,dh=480,180; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,173,"DaemonSet — exactly one Pod per Node (auto on new nodes)",10,DRK,True)
    nodes=[(80,95),(240,95),(400,95)]
    for i,(nx,ny) in enumerate(nodes):
        bx(d,nx-62,ny-48,124,96,f=colors.HexColor("#FEF9E7"),s=ORG,r=8,sw=1.5)
        lbl(d,nx,ny+38,f"Node {i+1}",9,ORG,True)
        hex_pod(d,nx,ny,r=22,fill=colors.HexColor("#8B5CF6"),text="fluentd")
    bx(d,330,8,130,28,f=GRN,s=GRN,r=6); lbl(d,395,19,"Node 4 joins → Pod auto-added!",8,WHT)
    return d

def d_job():
    dw,dh=480,150; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,143,"Job — run-to-completion (retry on failure)",10,DRK,True)
    stgs=[(60,80,"Job Created",BLU),(160,80,"Pod Running",TEL),(275,80,"Pod Succeeded",GRN),(390,80,"Job Complete",GRN)]
    for x,y,n,c in stgs:
        bx(d,x-44,y-22,88,44,f=c,s=c,r=8)
        for li,ln in enumerate(n.split()[:2]): lbl(d,x,y+5-li*13,ln,8.5,WHT,True)
    for i in range(3): arw(d,stgs[i][0]+46,80,stgs[i+1][0]-46,80)
    bx(d,116,16,88,30,f=RED,s=RED,r=6); lbl(d,160,28,"Pod Failed",8.5,WHT,True)
    d.add(Line(160,58,160,46,strokeColor=RED,strokeWidth=1.5))
    lbl(d,220,44,"backoffLimit retry →",8,RED)
    return d

def d_hpa():
    dw,dh=480,185; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,178,"HorizontalPodAutoscaler — CPU-driven scale-up / scale-down",10,DRK,True)
    bx(d,10,95,100,50,f=TEL,s=TEL,r=6)
    lbl(d,60,128,"Metrics",9,WHT,True); lbl(d,60,115,"Server",9,WHT,True); lbl(d,60,103,"CPU: 78%",8,colors.HexColor("#E0FFFF"))
    bx(d,150,85,115,65,f=BLU,s=BLU,r=6)
    lbl(d,207,140,"HPA",11,WHT,True); lbl(d,207,126,"target: 60% CPU",8,colors.HexColor("#BDD7FF"))
    lbl(d,207,113,"min:2 | max:6",8,colors.HexColor("#BDD7FF")); lbl(d,207,100,"2 → 4 replicas",8,ORG)
    arw(d,112,120,148,120); arw(d,267,120,298,120)
    bx(d,300,85,95,65,f=colors.HexColor("#1B4332"),s=GRN,r=6)
    lbl(d,347,140,"Deployment",9,WHT,True); lbl(d,347,126,"replicas: 2",8,RED)
    lbl(d,347,113,"    ↓ scale up",8,ORG); lbl(d,347,100,"replicas: 4",8,GRN)
    r=13
    for i,(px,py) in enumerate([(418,152),(448,128),(418,104),(448,80)]):
        pts=[]
        for k in range(6): a=math.radians(60*k-30); pts+=[px+r*math.cos(a),py+r*math.sin(a)]
        d.add(Polygon(pts,fillColor=BLU if i<2 else GRN,strokeColor=WHT,strokeWidth=1.5))
        lbl(d,px,py-4,"old" if i<2 else "new",6.5,WHT,True)
        arw(d,397,120,px-r-1,py)
    lbl(d,240,38,"Scale-UP:   avg CPU > target  →  add pods",9,RED)
    lbl(d,240,24,"Scale-DOWN: avg CPU < target (after stabilization window)  →  remove pods",9,GRN)
    return d

def d_resources():
    dw,dh=480,175; d=Drawing(dw,dh)
    d.add(Rect(0,0,dw,dh,fillColor=GRY,strokeColor=BOX,strokeWidth=0))
    lbl(d,240,168,"Resource Requests vs Limits — Node CPU allocation",10,DRK,True)
    bx=_bx=lambda x,y,w,h,f,s=BOX: d.add(Rect(x,y,w,h,fillColor=f,strokeColor=s,strokeWidth=1))
    bx(30,110,420,32,colors.HexColor("#E0E0E0"))
    bx(30,110,150,32,colors.HexColor("#BDD7FF"),BLU); lbl(d,105,124,"Pod A  request=100m",8,DRK)
    bx(180,110,110,32,colors.HexColor("#D8F3DC"),GRN); lbl(d,235,124,"Pod B  req=70m",8,DRK)
    bx(290,110,160,32,colors.HexColor("#F5F5F5")); lbl(d,370,124,"Available (free)",8,MID)
    d.add(Rect(30,110,420,32,fillColor=colors.Color(0,0,0,0),strokeColor=DRK,strokeWidth=1.5))
    d.add(Line(230,105,230,145,strokeColor=RED,strokeWidth=2,strokeDashArray=[4,2]))
    lbl(d,230,100,"Pod A limit=200m",7.5,RED)
    lbl(d,240,80,"Scheduler uses REQUESTS to decide placement.",9,DRK)
    lbl(d,240,66,"Containers are THROTTLED at the cpu limit and OOMKilled at the memory limit.",9,RED)
    for i,(c,t) in enumerate([(BLU,"Request = guaranteed minimum"),(RED,"Limit = hard ceiling (throttle/OOMKill)")]):
        d.add(Rect(30,42-i*18,12,12,fillColor=c,strokeColor=c,strokeWidth=0,rx=2))
        lbl(d,52,46-i*18,t,8.5,DRK,False,'start')
    return d

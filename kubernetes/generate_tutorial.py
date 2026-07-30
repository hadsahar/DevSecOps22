"""Entry point — builds the full PDF tutorial."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate

from tutorial_draw import BLU, MID, BOX, WHT, W, H, cm
from tutorial_content import cover, toc, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10

OUT_DIR  = os.path.join(os.path.dirname(__file__), "materials")
OUT_FILE = os.path.join(OUT_DIR, "kubernetes-workloads-tutorial.pdf")

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BLU); canvas.setLineWidth(2)
    canvas.line(2*cm, H-1.7*cm, W-2*cm, H-1.7*cm)
    canvas.setFillColor(BLU); canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(2*cm, H-1.4*cm, "Kubernetes Workloads — Teacher's Guide")
    canvas.setFillColor(MID); canvas.setFont('Helvetica', 9)
    canvas.drawRightString(W-2*cm, H-1.4*cm, "DevSecOps Teaching Series")
    canvas.setStrokeColor(BOX); canvas.setLineWidth(1)
    canvas.line(2*cm, 1.7*cm, W-2*cm, 1.7*cm)
    canvas.setFillColor(MID); canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(W/2, 1.1*cm, f"Page {doc.page}")
    canvas.restoreState()

def build():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = SimpleDocTemplate(
        OUT_FILE, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
        title="Kubernetes Workloads — Teacher's Guide",
        author="DevSecOps Teaching Series",
        subject="Kubernetes Workload Resources"
    )
    story = []
    cover(story)
    toc(story)
    ch1(story); ch2(story); ch3(story); ch4(story); ch5(story)
    ch6(story); ch7(story); ch8(story); ch9(story); ch10(story)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✅  PDF saved → {OUT_FILE}")

if __name__ == "__main__":
    build()

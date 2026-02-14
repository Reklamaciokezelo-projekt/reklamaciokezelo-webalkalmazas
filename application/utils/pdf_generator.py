import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

def generate_report_pdf(labels, values, title):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # --- BETŰTÍPUS REGISZTRÁLÁSA (küzdelem az ő/ű betűkért) ---
    font_path = "C:/Windows/Fonts/arial.ttf"
    if not os.path.exists(font_path):
        font_path = os.path.join(os.getcwd(), "arial.ttf")

    try:
        pdfmetrics.registerFont(TTFont('Arial-Fixed', font_path))
        FONT_NAME = 'Arial-Fixed'
    except:
        FONT_NAME = 'Helvetica'

    styles = getSampleStyleSheet()
    styles['Title'].fontName = FONT_NAME
    styles['Normal'].fontName = FONT_NAME

    # --- CÍMSOR ---
    elements.append(Paragraph(f"Reklamációs Riport: {title}", styles['Title']))
    elements.append(Spacer(1, 20))

    # --- MATPLOTLIB GRAFIKON ---
    plt.figure(figsize=(7, 4))
    bar_color = (54/255, 162/255, 235/255, 0.7)
    edge_color = (54/255, 162/255, 235/255, 1.0)

    plt.bar(labels, values, color=bar_color, edgecolor=edge_color)

    # --- Matplotlib font beállítása (Arial-ra, ha elérhető) ---
    plt.title(title, fontname='Arial' if FONT_NAME != 'Helvetica' else 'sans-serif', fontsize=14)
    plt.xticks(rotation=30, ha='right', fontname='Arial' if FONT_NAME != 'Helvetica' else 'sans-serif')
    plt.yticks(fontname='Arial' if FONT_NAME != 'Helvetica' else 'sans-serif')

    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()

    # --- Kép mentése memóriába ---
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150)
    plt.close()
    img_buffer.seek(0)

    # --- A kép hozzáadása a PDF-hez ---
    chart_img = Image(img_buffer, width=480, height=260)
    elements.append(chart_img)
    elements.append(Spacer(1, 30))

    # --- TÁBLÁZAT ---
    is_cost = "költség" in title.lower()
    
    data = [[Paragraph("<b>Kategória / Időszak</b>", styles['Normal']), 
             Paragraph("<b>Érték</b>", styles['Normal'])]]

    for i in range(len(labels)):
        val = values[i]
        if is_cost:
            formatted_val = f"{val:,.0f}".replace(",", " ") + " Ft"
        else:
            formatted_val = f"{int(val)} db"
        data.append([labels[i], formatted_val])

    table = Table(data, colWidths=[350, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), FONT_NAME),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)

    # --- Dokumentum építése ---
    doc.build(elements)
    buffer.seek(0)
    return buffer
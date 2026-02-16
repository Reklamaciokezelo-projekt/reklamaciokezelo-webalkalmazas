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
import matplotlib.font_manager as fm
from flask import current_app

def generate_report_pdf(labels, values, title, chart_type='bar', use_log_scale=False):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # --- A Flask current_app.root_path megadja az 'application' mappa teljes útvonalát ---
    font_filename = 'arial.ttf' 
    font_path = os.path.join(current_app.root_path, 'static', 'fonts', font_filename)

    if not os.path.exists(font_path):
        FONT_NAME = 'Helvetica'
        custom_font_prop = None
    else:
        try:
            # --- ReportLab regisztráció ---
            pdfmetrics.registerFont(TTFont('CustomFont', font_path))
            FONT_NAME = 'CustomFont'
            
            # --- Matplotlib font tulajdonságok betöltése a fájlból ---
            custom_font_prop = fm.FontProperties(fname=font_path)
        except Exception as e:
            FONT_NAME = 'Helvetica'
            custom_font_prop = None

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

    # --- Színes paletta kördiagramhoz ---
    pie_colors = [
        (54/255, 162/255, 235/255, 0.6), (255/255, 99/255, 132/255, 0.6),
        (255/255, 206/255, 86/255, 0.6), (75/255, 192/255, 192/255, 0.6),
        (153/255, 102/255, 255/255, 0.6), (255/255, 159/255, 64/255, 0.6)
    ]

    # --- KÖRDIAGRAM ---
    if chart_type == 'pie':

        patches, texts, autotexts = plt.pie(
            values, 
            labels=labels, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=pie_colors
        )
        # --- Font beállítása a kördiagram feliratokhoz ---
        if custom_font_prop:
            for text in texts + autotexts:
                text.set_fontproperties(custom_font_prop)
        
        plt.axis('equal')

    # --- VONALDIAGRAM ---
    elif chart_type == 'line':
        plt.plot(labels, values, marker='o', color=edge_color, linewidth=2, linestyle='-')
        plt.grid(True, linestyle='--', alpha=0.5)
        
        plt.fill_between(labels, values, color=bar_color, alpha=0.3)

    # --- OSZLOPDIAGRAM (alapértelmezett) ---
    else:
        plt.bar(labels, values, color=bar_color, edgecolor=edge_color)
        plt.grid(axis='y', linestyle='--', alpha=0.3)

    # --- TENGELYEK ÉS LOGARITMIKUS SKÁLA ---
    if chart_type != 'pie':
        # --- Logaritmikus skála beállítása ---
        if use_log_scale:
            plt.yscale('log')
        
        # --- Cím és tengelyfeliratok fontja ---
        if custom_font_prop:
            plt.title(title, fontproperties=custom_font_prop, fontsize=14)
            plt.xticks(rotation=30, ha='right', fontproperties=custom_font_prop)
            plt.yticks(fontproperties=custom_font_prop)
        else:
            plt.title(title, fontsize=14)
            plt.xticks(rotation=30, ha='right')
        
        plt.tight_layout()
    else:
        if custom_font_prop:
            plt.title(title, fontproperties=custom_font_prop, fontsize=14)
        else:
            plt.title(title, fontsize=14)
        plt.tight_layout()

    # --- Kép mentése ---
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150)
    plt.close()
    img_buffer.seek(0)

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
    doc.build(elements)
    buffer.seek(0)
    return buffer
"""
Editorial Tema - Gazete / dergi tipografisi.
Beyaz fon, mürekkep siyah, editoryal kırmızı.
"""

RENKLER = {
    # Kağıt katmanları
    "paper": "#fdfdfb",          # ana arkaplan (kağıt beyazı)
    "paper_off": "#f6f5f0",      # alternatif yüzey, hover
    "paper_panel": "#ffffff",    # saf beyaz kart
    "paper_inset": "#f0eee8",    # input arkaplanı

    # Mürekkep
    "ink": "#0e0e0c",            # ana metin (mürekkep siyahı)
    "ink_dim": "#3d3d3a",        # ikincil metin
    "ink_muted": "#7a7a72",      # dipnot
    "ink_subtle": "#a5a59c",     # placeholder
    "ink_faint": "#d4d3cb",      # disabled

    # Çizgiler
    "rule": "#0e0e0c",           # kalın yatay çizgi (gazete kuralı)
    "rule_thin": "#cfcec5",      # ince ayraç
    "rule_hairline": "#e8e7df",  # çok ince ayraç

    # Editorial accent
    "red": "#c9302c",            # editoryal kırmızı (mühür/marker)
    "red_dark": "#9a1f1c",
    "red_pale": "#fbeae8",       # rozet bg
    "gold": "#a08145",           # ara accent (rozet)
    "gold_pale": "#f5ecd9",

    # Durum
    "success": "#1f6b3a",
    "success_pale": "#e6f0e8",
    "warning": "#a37004",
    "warning_pale": "#fbf3dc",
    "danger": "#c9302c",
    "danger_pale": "#fbeae8",

    # Tablo
    "table_header_bg": "#0e0e0c",
    "table_header_text": "#fdfdfb",
    "table_zebra": "#f9f8f3",
    "table_row_hover": "#f3f1ea",
}


ANA_STIL = f"""
/* GENEL ============================================================ */
QWidget {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    font-family: "Inter", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow {{
    background-color: {RENKLER['paper']};
}}

QToolTip {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
    border: none;
    padding: 7px 12px;
    border-radius: 0;
    font-size: 11px;
    font-weight: 500;
}}

/* SIDEBAR ========================================================== */
#Sidebar {{
    background-color: {RENKLER['paper']};
    border-right: 1px solid {RENKLER['rule_thin']};
}}

#MastheadBaslik {{
    color: {RENKLER['ink']};
    background: transparent;
    border: none;
    font-family: "Playfair Display", "Georgia", "Times New Roman", serif;
    font-weight: 900;
    font-size: 22px;
    letter-spacing: -0.5px;
}}

#MastheadAlt {{
    color: {RENKLER['ink_muted']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 9px;
    letter-spacing: 2.5px;
    font-weight: 700;
    text-transform: uppercase;
}}

#MastheadIssue {{
    color: {RENKLER['red']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}}

#MenuBaslik {{
    color: {RENKLER['ink_muted']};
    font-family: "Inter", sans-serif;
    font-size: 9px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2px;
    background: transparent;
    border: none;
}}

QPushButton#MenuButon {{
    background-color: transparent;
    color: {RENKLER['ink_dim']};
    text-align: left;
    padding-left: 24px;
    padding-right: 24px;
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

QPushButton#MenuButon:hover {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
}}

QPushButton#MenuButon:checked {{
    background-color: transparent;
    color: {RENKLER['ink']};
    font-weight: 700;
    border-left: 3px solid {RENKLER['red']};
}}

#KullaniciKart {{
    background-color: {RENKLER['paper_off']};
    border: 1px solid {RENKLER['rule_thin']};
    border-radius: 0;
}}

#KullaniciKart QLabel {{
    background: transparent;
    border: none;
}}

#KullaniciAd {{
    color: {RENKLER['ink']};
    font-weight: 700;
    font-size: 12px;
    font-family: "Inter", sans-serif;
}}

#KullaniciDurum {{
    color: {RENKLER['ink_muted']};
    font-size: 10px;
    font-family: "Inter", sans-serif;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
}}

#PlanRozet {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
    border: none;
    border-radius: 0;
    padding: 3px 9px;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.5px;
    font-family: "Inter", sans-serif;
    min-width: 50px;
}}

/* SAYFA BAŞLIKLARI ================================================ */
#SayfaBaslik {{
    color: {RENKLER['ink']};
    background: transparent;
    border: none;
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 38px;
    font-weight: 900;
    letter-spacing: -0.8px;
}}

#SayfaAltBaslik {{
    color: {RENKLER['ink_muted']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 400;
    font-style: italic;
}}

#KicekerBaslik {{
    color: {RENKLER['red']};
    background: transparent;
    border: none;
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 2.5px;
}}

#PullQuote {{
    color: {RENKLER['ink']};
    background: transparent;
    border: none;
    border-left: 3px solid {RENKLER['red']};
    padding-left: 16px;
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 16px;
    font-weight: 500;
    font-style: italic;
}}

/* KARTLAR ========================================================= */
#Kart {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-radius: 0;
}}

#Kart QLabel {{
    background: transparent;
    border: none;
}}

#KartBaslik {{
    color: {RENKLER['ink']};
    font-family: "Playfair Display", "Georgia", serif;
    font-size: 18px;
    font-weight: 800;
    background: transparent;
    border: none;
    letter-spacing: -0.3px;
}}

#KartAltBaslik {{
    color: {RENKLER['ink_muted']};
    font-family: "Inter", sans-serif;
    font-size: 12px;
    background: transparent;
    border: none;
    font-style: italic;
}}

/* BUTONLAR ======================================================== */
QPushButton {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['rule_thin']};
    padding-left: 18px;
    padding-right: 18px;
    border-radius: 0;
    font-family: "Inter", sans-serif;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
}}

QPushButton:hover {{
    background-color: {RENKLER['paper']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton:disabled {{
    background-color: {RENKLER['paper_inset']};
    color: {RENKLER['ink_faint']};
    border: 1px solid {RENKLER['rule_hairline']};
}}

QPushButton#PrimaryButon {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#PrimaryButon:hover {{
    background-color: {RENKLER['red']};
    border: 1px solid {RENKLER['red']};
}}

QPushButton#BasariButon {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#BasariButon:hover {{
    background-color: {RENKLER['red']};
    border: 1px solid {RENKLER['red']};
}}

QPushButton#IkincilButon {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#IkincilButon:hover {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
}}

QPushButton#HayaletButon {{
    background-color: transparent;
    color: {RENKLER['ink_dim']};
    border: 1px solid {RENKLER['rule_thin']};
}}

QPushButton#HayaletButon:hover {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
}}

QPushButton#TehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['rule_thin']};
}}

QPushButton#TehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
}}

QPushButton#KucukIkincilButon {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    border: 1px solid {RENKLER['ink']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QPushButton#KucukIkincilButon:hover {{
    background-color: {RENKLER['ink']};
    color: {RENKLER['paper']};
}}

QPushButton#KucukTehlikeButon {{
    background-color: transparent;
    color: {RENKLER['danger']};
    border: 1px solid {RENKLER['rule_thin']};
    padding-left: 12px;
    padding-right: 12px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
}}

QPushButton#KucukTehlikeButon:hover {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
}}

/* FORM ALANLARI =================================================== */
QLineEdit, QSpinBox, QDateTimeEdit, QComboBox, QTextEdit {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-bottom: 1px solid {RENKLER['ink']};
    border-radius: 0;
    padding-left: 12px;
    padding-right: 12px;
    color: {RENKLER['ink']};
    selection-background-color: {RENKLER['ink']};
    selection-color: {RENKLER['paper']};
    font-family: "Inter", sans-serif;
    font-size: 13px;
}}

QLineEdit:focus, QSpinBox:focus, QDateTimeEdit:focus,
QComboBox:focus, QTextEdit:focus {{
    border: 1px solid {RENKLER['ink']};
    border-bottom: 2px solid {RENKLER['red']};
    background-color: {RENKLER['paper']};
}}

QLineEdit:hover, QSpinBox:hover, QDateTimeEdit:hover,
QComboBox:hover, QTextEdit:hover {{
    border-bottom: 1px solid {RENKLER['red']};
}}

#AramaInput {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-bottom: 2px solid {RENKLER['ink']};
    padding-left: 16px;
    padding-right: 16px;
    border-radius: 0;
    font-family: "Inter", sans-serif;
    font-size: 13px;
    font-weight: 500;
}}

#AramaInput:focus {{
    border: 1px solid {RENKLER['ink']};
    border-bottom: 2px solid {RENKLER['red']};
}}

QSpinBox::up-button, QSpinBox::down-button,
QDateTimeEdit::up-button, QDateTimeEdit::down-button {{
    background-color: transparent;
    border: none;
    width: 16px;
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
    background: transparent;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid {RENKLER['ink']};
    margin-right: 12px;
    width: 0;
    height: 0;
}}

QComboBox QAbstractItemView {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['ink']};
    border-radius: 0;
    selection-background-color: {RENKLER['ink']};
    selection-color: {RENKLER['paper']};
    color: {RENKLER['ink']};
    padding: 4px;
    outline: 0;
}}

QComboBox QAbstractItemView::item {{
    padding: 8px 10px;
    border-radius: 0;
    min-height: 22px;
}}

QComboBox QAbstractItemView::item:hover {{
    background-color: {RENKLER['paper_off']};
}}

QLabel#FormEtiket {{
    color: {RENKLER['ink_dim']};
    font-family: "Inter", sans-serif;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    background: transparent;
    border: none;
}}

/* TABLOLAR ======================================================== */
QTableWidget {{
    background-color: {RENKLER['paper_panel']};
    border: 1px solid {RENKLER['rule_thin']};
    border-top: 2px solid {RENKLER['ink']};
    border-bottom: 2px solid {RENKLER['ink']};
    border-radius: 0;
    gridline-color: transparent;
    color: {RENKLER['ink']};
    selection-background-color: transparent;
    outline: 0;
    alternate-background-color: {RENKLER['table_zebra']};
}}

QTableWidget::item {{
    padding-left: 8px;
    padding-right: 8px;
    border: none;
    border-bottom: 1px solid {RENKLER['rule_hairline']};
    background-color: transparent;
    color: {RENKLER['ink']};
}}

QTableWidget::item:selected {{
    background-color: {RENKLER['paper_off']};
    color: {RENKLER['ink']};
}}

QTableWidget::item:hover {{
    background-color: {RENKLER['table_row_hover']};
}}

QHeaderView::section {{
    background-color: {RENKLER['paper']};
    color: {RENKLER['ink_muted']};
    padding-top: 14px;
    padding-bottom: 14px;
    padding-left: 14px;
    padding-right: 14px;
    border: none;
    border-bottom: 1px solid {RENKLER['ink']};
    font-family: "Inter", sans-serif;
    font-weight: 800;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 2px;
}}

QHeaderView::section:first {{
    border-top-left-radius: 0;
}}

QHeaderView::section:last {{
    border-top-right-radius: 0;
}}

QTableCornerButton::section {{
    background-color: {RENKLER['paper']};
    border: none;
}}

/* SCROLLBAR ======================================================= */
QScrollBar:vertical {{
    background: transparent;
    width: 8px;
    border: none;
    margin: 4px 2px 4px 2px;
}}

QScrollBar::handle:vertical {{
    background: {RENKLER['ink_faint']};
    border-radius: 0;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {RENKLER['ink']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 8px;
    border: none;
    margin: 2px 4px 2px 4px;
}}

QScrollBar::handle:horizontal {{
    background: {RENKLER['ink_faint']};
    border-radius: 0;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {RENKLER['ink']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

/* DİYALOG ========================================================= */
QDialog {{
    background-color: {RENKLER['paper']};
}}

QMessageBox {{
    background-color: {RENKLER['paper_panel']};
}}

QMessageBox QLabel {{
    color: {RENKLER['ink']};
    font-family: "Inter", sans-serif;
    font-size: 13px;
    background: transparent;
    border: none;
}}

QMessageBox QPushButton {{
    min-width: 90px;
}}

/* ROZETLER (chip / ribbon) ======================================== */
QLabel#RozetBasari {{
    background-color: transparent;
    color: {RENKLER['success']};
    border: 1px solid {RENKLER['success']};
    border-radius: 0;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
    
    letter-spacing: 1.5px;
}}

QLabel#RozetUyari {{
    background-color: transparent;
    color: {RENKLER['warning']};
    border: 1px solid {RENKLER['warning']};
    border-radius: 0;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
    
    letter-spacing: 1.5px;
}}

QLabel#RozetTehlike {{
    background-color: {RENKLER['danger']};
    color: {RENKLER['paper']};
    border: 1px solid {RENKLER['danger']};
    border-radius: 0;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
    
    letter-spacing: 1.5px;
}}

QLabel#RozetNotr {{
    background-color: transparent;
    color: {RENKLER['ink_muted']};
    border: 1px solid {RENKLER['rule_thin']};
    border-radius: 0;
    padding-left: 10px;
    padding-right: 10px;
    padding-top: 3px;
    padding-bottom: 3px;
    font-family: "Inter", sans-serif;
    font-size: 9px;
    font-weight: 800;
    min-width: 90px;
    
    letter-spacing: 1.5px;
}}

/* DİĞER =========================================================== */
QFrame#Ayirici {{
    background-color: {RENKLER['rule']};
    max-height: 2px;
    min-height: 2px;
    border: none;
}}

QFrame#AyiriciInce {{
    background-color: {RENKLER['rule_hairline']};
    max-height: 1px;
    min-height: 1px;
    border: none;
}}
"""

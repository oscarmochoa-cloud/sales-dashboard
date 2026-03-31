import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import StringIO
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0f1e;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --bg-card-hover: #1e2a40;
    --accent-green: #00d68f;
    --accent-blue: #3b82f6;
    --accent-purple: #8b5cf6;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: rgba(255,255,255,0.07);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0f172a 50%, #0a0f1e 100%) !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* Header */
.dashboard-header {
    background: linear-gradient(135deg, #1a2235 0%, #0f1929 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.dashboard-header::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,214,143,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    letter-spacing: -0.5px;
}

.header-subtitle {
    color: var(--text-secondary);
    font-size: 14px;
    margin-top: 4px;
}

.header-badge {
    display: inline-block;
    background: rgba(0,214,143,0.12);
    color: var(--accent-green);
    border: 1px solid rgba(0,214,143,0.25);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 12px;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.kpi-card:hover {
    background: var(--bg-card-hover);
    border-color: rgba(255,255,255,0.12);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.kpi-icon {
    font-size: 20px;
    margin-bottom: 12px;
    display: block;
}

.kpi-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: var(--text-secondary);
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
    margin-bottom: 10px;
}

.kpi-delta {
    font-size: 12px;
    font-weight: 500;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
}

.kpi-delta.positive {
    background: rgba(0,214,143,0.12);
    color: var(--accent-green);
}

.kpi-delta.negative {
    background: rgba(239,68,68,0.12);
    color: var(--accent-red);
}

.kpi-delta.neutral {
    background: rgba(148,163,184,0.12);
    color: var(--text-secondary);
}

.kpi-accent-bar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
}

/* Alert Cards */
.alert-card {
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid;
}

.alert-red {
    background: rgba(239,68,68,0.08);
    border-color: rgba(239,68,68,0.2);
    color: #fca5a5;
}

.alert-amber {
    background: rgba(245,158,11,0.08);
    border-color: rgba(245,158,11,0.2);
    color: #fcd34d;
}

.alert-green {
    background: rgba(0,214,143,0.08);
    border-color: rgba(0,214,143,0.2);
    color: #6ee7b7;
}

/* Section Headers */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.section-tag {
    background: rgba(59,130,246,0.12);
    color: #93c5fd;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    padding: 2px 8px;
    border-radius: 4px;
}

/* Risk Badges */
.risk-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.risk-high { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.risk-medium { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.risk-low { background: rgba(0,214,143,0.15); color: #34d399; border: 1px solid rgba(0,214,143,0.3); }

/* VIP Badges */
.vip-badge { background: linear-gradient(135deg, #7c3aed, #4f46e5); color: white; }
.a-badge { background: rgba(59,130,246,0.2); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
.b-badge { background: rgba(0,214,143,0.15); color: #34d399; border: 1px solid rgba(0,214,143,0.3); }
.c-badge { background: rgba(148,163,184,0.1); color: #94a3b8; border: 1px solid rgba(148,163,184,0.2); }

/* Score Bar */
.score-bar-container {
    background: rgba(255,255,255,0.05);
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
    margin-top: 4px;
}

.score-bar-fill {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #3b82f6, #00d68f);
    transition: width 1s ease;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}

.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}

/* Tables */
.stDataFrame {
    background: var(--bg-card) !important;
    border-radius: 12px !important;
    border: 1px solid var(--border) !important;
}

/* Inputs */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
}

.stDateInput > div > div > input {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* Divider */
.styled-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 20px 0;
}

/* Download Button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1e3a5f, #1e40af) !important;
    color: white !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.3s !important;
}

.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #1e40af, #2563eb) !important;
    box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
    transform: translateY(-1px) !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* Plotly Charts */
.js-plotly-plot .plotly .bg {
    fill: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
SHEET_ID = "1KyA_YyGN0veOcAh1nNy8gzIrrmB4Ji9mCXuexyXDIv4"
GID = "396308671"

@st.cache_data(ttl=300)
def load_data():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df, None
    except Exception as e:
        return None, str(e)

def clean_data(df):
    df.columns = df.columns.str.strip().str.upper()
    
    # Map common column name variations
    col_map = {}
    for col in df.columns:
        c = col.upper()
        if 'FECHA' in c or 'DATE' in c: col_map[col] = 'FECHA'
        elif 'CLIENTE' in c or 'CLIENT' in c: col_map[col] = 'CLIENTE'
        elif 'CANAL' in c or 'CHANNEL' in c: col_map[col] = 'CANAL'
        elif 'PRODUCTO' in c or 'PRODUCT' in c: col_map[col] = 'PRODUCTO'
        elif 'CANTIDAD' in c or 'QTY' in c or 'QUANTITY' in c: col_map[col] = 'CANTIDAD'
        elif 'PRECIO' in c and 'VENTA' in c: col_map[col] = 'PRECIO_VENTA'
        elif 'VENTA' in c and 'NETA' in c: col_map[col] = 'VENTA_NETA'
        elif 'VENTA' in c: col_map[col] = 'VENTA_NETA'
        elif 'COSTO' in c or 'COST' in c: col_map[col] = 'COSTO'
        elif 'COMISION' in c or 'COMMISSION' in c: col_map[col] = 'COMISION'
        elif 'PUBLICIDAD' in c or 'ADS' in c or 'ADVERTISING' in c: col_map[col] = 'PUBLICIDAD'
        elif 'ENVIO' in c or 'SHIPPING' in c or 'ENVÍO' in c: col_map[col] = 'ENVIO'
        elif 'NET PROFIT' in c or 'PROFIT' in c or 'GANANCIA' in c: col_map[col] = 'NET_PROFIT'
        elif 'NET MARGIN' in c or 'MARGIN' in c or 'MARGEN' in c: col_map[col] = 'NET_MARGIN'
    
    df = df.rename(columns=col_map)
    
    # Parse date
    for date_fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y']:
        try:
            df['FECHA'] = pd.to_datetime(df['FECHA'], format=date_fmt)
            break
        except:
            try:
                df['FECHA'] = pd.to_datetime(df['FECHA'])
                break
            except:
                pass
    
    # Numeric columns
    numeric_cols = ['CANTIDAD', 'PRECIO_VENTA', 'VENTA_NETA', 'COSTO', 'COMISION',
                    'PUBLICIDAD', 'ENVIO', 'NET_PROFIT', 'NET_MARGIN']
    for col in numeric_cols:
        if col in df.columns:
            vals = []
            for v in df[col].values:
                s = str(v).replace('$','').replace(',','').replace('%','').replace(' ','')
                try:
                    vals.append(float(s))
                except:
                    vals.append(0.0)
            df[col] = vals
    
    # Calculate missing columns
    if 'NET_PROFIT' not in df.columns and 'VENTA_NETA' in df.columns and 'COSTO' in df.columns:
        cost_cols = ['COSTO']
        for c in ['COMISION', 'PUBLICIDAD', 'ENVIO']:
            if c in df.columns:
                cost_cols.append(c)
        df['NET_PROFIT'] = df['VENTA_NETA'] - df[cost_cols].sum(axis=1)
    
    if 'NET_MARGIN' not in df.columns and 'NET_PROFIT' in df.columns and 'VENTA_NETA' in df.columns:
        df['NET_MARGIN'] = (df['NET_PROFIT'] / df['VENTA_NETA'].replace(0, np.nan) * 100).fillna(0)
    
    return df.dropna(subset=['FECHA'])

# Chart theme
CHART_THEME = {
    'bg': 'rgba(0,0,0,0)',
    'paper_bg': 'rgba(0,0,0,0)',
    'font_color': '#94a3b8',
    'grid_color': 'rgba(255,255,255,0.04)',
    'colors': ['#3b82f6', '#00d68f', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#ec4899'],
}

def apply_chart_theme(fig, title=None, height=380):
    fig.update_layout(
        paper_bgcolor=CHART_THEME['paper_bg'],
        plot_bgcolor=CHART_THEME['bg'],
        font=dict(color=CHART_THEME['font_color'], family='DM Sans'),
        title=dict(text=title, font=dict(size=14, color='#f1f5f9', family='Space Grotesk'), x=0.01) if title else None,
        height=height,
        margin=dict(l=16, r=16, t=40 if title else 16, b=16),
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            gridcolor=CHART_THEME['grid_color'],
            linecolor='rgba(255,255,255,0.06)',
            tickfont=dict(size=11),
            zerolinecolor='rgba(255,255,255,0.06)',
        ),
        yaxis=dict(
            gridcolor=CHART_THEME['grid_color'],
            linecolor='rgba(255,255,255,0.06)',
            tickfont=dict(size=11),
            zerolinecolor='rgba(255,255,255,0.06)',
        ),
        hoverlabel=dict(
            bgcolor='#1a2235',
            bordercolor='rgba(255,255,255,0.15)',
            font=dict(size=12, color='#f1f5f9'),
        ),
    )
    fig.update_layout(height=height)
    return fig

def fmt_currency(val):
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif abs(val) >= 1_000:
        return f"${val/1_000:.1f}K"
    return f"${val:,.0f}"

def fmt_pct(val):
    return f"{val:.1f}%"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 20px 0 16px;'>
        <div style='font-family: Space Grotesk; font-size: 18px; font-weight: 700; color: #f1f5f9;'>
            📊 Sales Intelligence
        </div>
        <div style='font-size: 11px; color: #64748b; margin-top: 4px;'>Powered by Google Sheets</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🔄 Actualizar datos", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("### 🔍 Filtros Globales")

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
raw_df, error = load_data()

if error:
    st.error(f"⚠️ Error cargando datos: {error}")
    st.info("Asegúrate de que el Google Sheet sea público (Compartir → Cualquier persona con el enlace).")
    st.stop()

if raw_df is None or raw_df.empty:
    st.warning("No se encontraron datos en el Google Sheet.")
    st.stop()

df_full = clean_data(raw_df.copy())

if df_full.empty:
    st.error("No se pudieron procesar los datos. Verifica el formato del sheet.")
    st.stop()

# Sidebar Filters
with st.sidebar:
    min_date = pd.Timestamp(df_full['FECHA'].min()).date()
    max_date = pd.Timestamp(df_full['FECHA'].max()).date()
    
    date_range = st.date_input(
        "📅 Rango de fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    clientes = ['Todos'] + sorted(df_full['CLIENTE'].dropna().unique().tolist()) if 'CLIENTE' in df_full.columns else ['Todos']
    selected_cliente = st.selectbox("👤 Cliente", clientes)
    
    canales = ['Todos'] + sorted(df_full['CANAL'].dropna().unique().tolist()) if 'CANAL' in df_full.columns else ['Todos']
    selected_canal = st.selectbox("🛒 Canal de venta", canales)
    
    productos = ['Todos'] + sorted(df_full['PRODUCTO'].dropna().unique().tolist()) if 'PRODUCTO' in df_full.columns else ['Todos']
    selected_producto = st.selectbox("📦 Producto", productos)
    
    st.markdown("---")
    st.markdown(f"""
    <div style='font-size:11px; color:#475569; text-align:center; padding:8px;'>
        Última actualización<br>
        <span style='color:#64748b;'>{datetime.now().strftime('%d/%m/%Y %H:%M')}</span><br>
        <span style='color:#00d68f; font-weight:600;'>{len(df_full):,} registros cargados</span>
    </div>
    """, unsafe_allow_html=True)

# Apply filters
df = df_full.copy()
if len(date_range) == 2:
    df = df[(df['FECHA'].dt.date >= date_range[0]) & (df['FECHA'].dt.date <= date_range[1])]
if selected_cliente != 'Todos' and 'CLIENTE' in df.columns:
    df = df[df['CLIENTE'] == selected_cliente]
if selected_canal != 'Todos' and 'CANAL' in df.columns:
    df = df[df['CANAL'] == selected_canal]
if selected_producto != 'Todos' and 'PRODUCTO' in df.columns:
    df = df[df['PRODUCTO'] == selected_producto]

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dashboard-header">
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px;">
        <div>
            <p class="header-title">📊 Sales Intelligence Dashboard</p>
            <p class="header-subtitle">Análisis en tiempo real · {date_range[0].strftime('%d %b %Y') if len(date_range)==2 else ''} → {date_range[1].strftime('%d %b %Y') if len(date_range)==2 else ''}</p>
            <span class="header-badge">🟢 Datos en vivo desde Google Sheets</span>
        </div>
        <div style="text-align:right;">
            <div style="font-size:32px; font-weight:700; font-family:Space Grotesk; color:#f1f5f9;">{len(df):,}</div>
            <div style="font-size:11px; color:#64748b; text-transform:uppercase; letter-spacing:0.5px;">Transacciones filtradas</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# COMPUTE GLOBAL METRICS
# ─────────────────────────────────────────────
total_ventas = df['VENTA_NETA'].sum() if 'VENTA_NETA' in df.columns else 0
total_profit = df['NET_PROFIT'].sum() if 'NET_PROFIT' in df.columns else 0
avg_margin = df['NET_MARGIN'].mean() if 'NET_MARGIN' in df.columns else 0
total_clientes = df['CLIENTE'].nunique() if 'CLIENTE' in df.columns else 0
total_ordenes = len(df)

# Month comparison
today = pd.Timestamp(df['FECHA'].max())
this_month = df[df['FECHA'].dt.month == today.month]
last_month = df[df['FECHA'].dt.month == (today.month - 1) % 12 + 1]
ventas_this = this_month['VENTA_NETA'].sum() if 'VENTA_NETA' in this_month.columns else 0
ventas_last = last_month['VENTA_NETA'].sum() if 'VENTA_NETA' in last_month.columns else 0
pct_change = ((ventas_this - ventas_last) / ventas_last * 100) if ventas_last > 0 else 0

# ─────────────────────────────────────────────
# ALERTS
# ─────────────────────────────────────────────
alerts = []
if 'CLIENTE' in df.columns and 'FECHA' in df.columns:
    last_purchase = df.groupby('CLIENTE')['FECHA'].max()
    at_risk = (today - last_purchase).dt.days
    n_risk = (at_risk > 45).sum()
    if n_risk > 0:
        alerts.append(('red', f"🚨 {n_risk} clientes sin comprar en +45 días"))

if avg_margin < 15:
    alerts.append(('amber', f"⚠️ Margen promedio bajo: {avg_margin:.1f}%"))

if pct_change < -10:
    alerts.append(('amber', f"📉 Ventas {abs(pct_change):.0f}% menores vs mes anterior"))

if pct_change > 10:
    alerts.append(('green', f"📈 Crecimiento de {pct_change:.0f}% vs mes anterior"))

if alerts:
    cols = st.columns(len(alerts))
    for i, (level, msg) in enumerate(alerts):
        with cols[i]:
            st.markdown(f'<div class="alert-card alert-{level}">{msg}</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tabs = st.tabs(["🏠 Dashboard", "👥 Clientes", "📦 Productos", "📈 Análisis Avanzado", "🎯 Métricas VIP"])

# ════════════════════════════════════════════
# TAB 1: DASHBOARD PRINCIPAL
# ════════════════════════════════════════════
with tabs[0]:
    
    # KPI Cards
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    
    kpi_data = [
        (kpi1, "💰", "Total Ventas", fmt_currency(total_ventas), f"{'▲' if pct_change>=0 else '▼'} {abs(pct_change):.1f}% vs mes ant.", 'positive' if pct_change>=0 else 'negative', '#3b82f6'),
        (kpi2, "📈", "Ganancia Neta", fmt_currency(total_profit), f"Margen: {avg_margin:.1f}%", 'positive' if total_profit>0 else 'negative', '#00d68f'),
        (kpi3, "🎯", "Margen %", fmt_pct(avg_margin), "Sobre ventas netas", 'positive' if avg_margin>=20 else ('neutral' if avg_margin>=10 else 'negative'), '#8b5cf6'),
        (kpi4, "👤", "Clientes", f"{total_clientes:,}", f"Activos en periodo", 'neutral', '#f59e0b'),
        (kpi5, "🧾", "Órdenes", f"{total_ordenes:,}", f"Promedio {fmt_currency(total_ventas/total_ordenes if total_ordenes>0 else 0)}/orden", 'neutral', '#06b6d4'),
    ]
    
    for col, icon, label, value, delta, delta_class, color in kpi_data:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-accent-bar" style="background:{color};"></div>
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                <span class="kpi-delta {delta_class}">{delta}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    
    # Charts row 1
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown('<div class="section-header">📉 Tendencia de Ventas <span class="section-tag">Interactivo</span></div>', unsafe_allow_html=True)
        if 'FECHA' in df.columns and 'VENTA_NETA' in df.columns:
            ts = df.groupby(df['FECHA'].dt.to_period('W').dt.start_time).agg(
                Ventas=('VENTA_NETA', 'sum'),
                Profit=('NET_PROFIT', 'sum') if 'NET_PROFIT' in df.columns else ('VENTA_NETA', 'sum')
            ).reset_index()
            ts.columns = ['Fecha', 'Ventas', 'Profit']
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts['Fecha'], y=ts['Ventas'],
                name='Ventas Netas', mode='lines+markers',
                line=dict(color='#3b82f6', width=2.5),
                marker=dict(size=5, color='#3b82f6'),
                fill='tonexty', fillcolor='rgba(59,130,246,0.05)',
                hovertemplate='<b>%{x|%d %b}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
            ))
            fig.add_trace(go.Scatter(
                x=ts['Fecha'], y=ts['Profit'],
                name='Ganancia', mode='lines',
                line=dict(color='#00d68f', width=2, dash='dot'),
                hovertemplate='<b>%{x|%d %b}</b><br>Profit: $%{y:,.0f}<extra></extra>'
            ))
            
            # Trend line
            if len(ts) > 3:
                x_num = np.arange(len(ts))
                z = np.polyfit(x_num, ts['Ventas'].fillna(0), 1)
                p = np.poly1d(z)
                fig.add_trace(go.Scatter(
                    x=ts['Fecha'], y=p(x_num),
                    name='Tendencia', mode='lines',
                    line=dict(color='#f59e0b', width=1.5, dash='dash'),
                    hoverinfo='skip'
                ))
            
            apply_chart_theme(fig, height=350)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col_right:
        st.markdown('<div class="section-header">🏆 Top Clientes</div>', unsafe_allow_html=True)
        if 'CLIENTE' in df.columns and 'VENTA_NETA' in df.columns:
            top5 = df.groupby('CLIENTE')['VENTA_NETA'].sum().nlargest(5).reset_index()
            top5.columns = ['Cliente', 'Ventas']
            
            fig = go.Figure(go.Bar(
                x=top5['Ventas'],
                y=top5['Cliente'],
                orientation='h',
                marker=dict(
                    color=top5['Ventas'],
                    colorscale=[[0, 'rgba(59,130,246,0.4)'], [1, '#3b82f6']],
                    line=dict(width=0)
                ),
                text=[fmt_currency(v) for v in top5['Ventas']],
                textposition='inside',
                textfont=dict(color='white', size=11, family='DM Sans'),
                hovertemplate='<b>%{y}</b><br>Ventas: $%{x:,.0f}<extra></extra>'
            ))
            apply_chart_theme(fig, height=350)
            fig.update_layout(yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Charts row 2
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.markdown('<div class="section-header">🛒 Ventas por Canal</div>', unsafe_allow_html=True)
        if 'CANAL' in df.columns and 'VENTA_NETA' in df.columns:
            canal_df = df.groupby('CANAL')['VENTA_NETA'].sum().reset_index()
            fig = px.pie(canal_df, values='VENTA_NETA', names='CANAL',
                        color_discrete_sequence=CHART_THEME['colors'],
                        hole=0.5)
            fig.update_traces(
                textinfo='label+percent',
                textfont=dict(size=11),
                hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>',
                marker=dict(line=dict(color='#0a0f1e', width=2))
            )
            apply_chart_theme(fig, height=280)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col_b:
        st.markdown('<div class="section-header">📅 Ventas Mensuales</div>', unsafe_allow_html=True)
        monthly = df.groupby(df['FECHA'].dt.to_period('M').dt.start_time)['VENTA_NETA'].sum().reset_index()
        monthly.columns = ['Mes', 'Ventas']
        fig = px.bar(monthly, x='Mes', y='Ventas',
                    color_discrete_sequence=['#3b82f6'])
        fig.update_traces(
            marker_line_width=0,
            hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'
        )
        apply_chart_theme(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col_c:
        st.markdown('<div class="section-header">💡 Semáforo de Salud</div>', unsafe_allow_html=True)
        
        health_items = []
        
        margin_color = "#00d68f" if avg_margin >= 20 else ("#f59e0b" if avg_margin >= 10 else "#ef4444")
        margin_status = "Excelente" if avg_margin >= 20 else ("Aceptable" if avg_margin >= 10 else "Crítico")
        health_items.append((margin_color, "Margen neto", f"{avg_margin:.1f}%", margin_status))
        
        growth_color = "#00d68f" if pct_change > 5 else ("#f59e0b" if pct_change > -5 else "#ef4444")
        growth_status = "Creciendo" if pct_change > 5 else ("Estable" if pct_change > -5 else "Decayendo")
        health_items.append((growth_color, "Crecimiento MoM", f"{pct_change:+.1f}%", growth_status))
        
        if 'CLIENTE' in df.columns and 'FECHA' in df.columns:
            last_p = df.groupby('CLIENTE')['FECHA'].max()
            risk_pct = ((today - last_p).dt.days > 45).mean() * 100
            retention_color = "#00d68f" if risk_pct < 20 else ("#f59e0b" if risk_pct < 40 else "#ef4444")
            health_items.append((retention_color, "Clientes en riesgo", f"{risk_pct:.0f}%", "Retención OK" if risk_pct < 20 else "Atención"))
        
        for color, label, value, status in health_items:
            st.markdown(f"""
            <div style='background: var(--bg-card); border: 1px solid var(--border); border-left: 3px solid {color};
                        border-radius: 10px; padding: 14px 16px; margin-bottom: 10px;
                        display: flex; justify-content: space-between; align-items: center;'>
                <div>
                    <div style='font-size:11px; color:#64748b; font-weight:600; text-transform:uppercase;'>{label}</div>
                    <div style='font-size:20px; font-weight:700; font-family:Space Grotesk; color:#f1f5f9; margin-top:2px;'>{value}</div>
                </div>
                <div style='background: {color}20; color: {color}; border: 1px solid {color}40;
                            padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;'>
                    {status}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.download_button("⬇️ Descargar datos completos (CSV)", df.to_csv(index=False).encode(), "sales_data.csv", "text/csv")


# ════════════════════════════════════════════
# TAB 2: ANÁLISIS DE CLIENTES
# ════════════════════════════════════════════
with tabs[1]:
    
    if 'CLIENTE' not in df.columns:
        st.warning("Columna CLIENTE no encontrada en los datos.")
    else:
        # ── Cadencia & Segmentation ──
        client_stats = df.groupby('CLIENTE').agg(
            Total_Ventas=('VENTA_NETA', 'sum'),
            Total_Ordenes=('FECHA', 'count'),
            Primera_Compra=('FECHA', 'min'),
            Ultima_Compra=('FECHA', 'max'),
            Profit=('NET_PROFIT', 'sum') if 'NET_PROFIT' in df.columns else ('VENTA_NETA', 'sum'),
            Margen=('NET_MARGIN', 'mean') if 'NET_MARGIN' in df.columns else ('VENTA_NETA', 'mean')
        ).reset_index()
        
        client_stats['Dias_Sin_Comprar'] = (today - client_stats['Ultima_Compra']).dt.days
        client_stats['Antiguedad_Dias'] = (client_stats['Ultima_Compra'] - client_stats['Primera_Compra']).dt.days
        client_stats['Cadencia_Dias'] = (client_stats['Antiguedad_Dias'] / client_stats['Total_Ordenes'].clip(lower=1)).round(1)
        client_stats['Proxima_Compra'] = client_stats['Ultima_Compra'] + pd.to_timedelta(client_stats['Cadencia_Dias'], unit='D')
        client_stats['Dias_Para_Proxima'] = (client_stats['Proxima_Compra'] - today).dt.days
        
        # Pareto Segmentation
        client_stats = client_stats.sort_values('Total_Ventas', ascending=False)
        client_stats['Ventas_Cum_Pct'] = client_stats['Total_Ventas'].cumsum() / client_stats['Total_Ventas'].sum() * 100
        
        def segment(pct):
            if pct <= 50: return 'VIP'
            elif pct <= 70: return 'A'
            elif pct <= 90: return 'B'
            return 'C'
        client_stats['Segmento'] = client_stats['Ventas_Cum_Pct'].apply(segment)
        
        # Riesgo
        def risk(days):
            if days > 60: return 'ALTO'
            elif days > 45: return 'MEDIO'
            return 'BAJO'
        client_stats['Riesgo'] = client_stats['Dias_Sin_Comprar'].apply(risk)
        
        # ── KPIs ──
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            vip_count = (client_stats['Segmento'] == 'VIP').sum()
            st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:#8b5cf6;"></div>
            <span class="kpi-icon">⭐</span><div class="kpi-label">Clientes VIP</div>
            <div class="kpi-value">{vip_count}</div>
            <span class="kpi-delta positive">Top 50% de ingresos</span></div>""", unsafe_allow_html=True)
        with c2:
            at_risk_n = (client_stats['Riesgo'] == 'ALTO').sum()
            st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:#ef4444;"></div>
            <span class="kpi-icon">🚨</span><div class="kpi-label">En Riesgo (60+ días)</div>
            <div class="kpi-value">{at_risk_n}</div>
            <span class="kpi-delta negative">Requieren contacto</span></div>""", unsafe_allow_html=True)
        with c3:
            avg_cadence = client_stats['Cadencia_Dias'].median()
            st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:#3b82f6;"></div>
            <span class="kpi-icon">🔄</span><div class="kpi-label">Cadencia Mediana</div>
            <div class="kpi-value">{avg_cadence:.0f}d</div>
            <span class="kpi-delta neutral">Entre compras</span></div>""", unsafe_allow_html=True)
        with c4:
            medium_risk = (client_stats['Riesgo'] == 'MEDIO').sum()
            st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:#f59e0b;"></div>
            <span class="kpi-icon">⚠️</span><div class="kpi-label">Atención (45+ días)</div>
            <div class="kpi-value">{medium_risk}</div>
            <span class="kpi-delta neutral">Monitorear</span></div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        col_seg, col_risk = st.columns(2)
        
        with col_seg:
            st.markdown('<div class="section-header">🏅 Segmentación Pareto</div>', unsafe_allow_html=True)
            seg_counts = client_stats['Segmento'].value_counts()
            seg_revenue = client_stats.groupby('Segmento')['Total_Ventas'].sum()
            
            fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'pie'}, {'type': 'pie'}]],
                               subplot_titles=['Clientes', 'Ingresos'])
            seg_colors = {'VIP': '#8b5cf6', 'A': '#3b82f6', 'B': '#00d68f', 'C': '#64748b'}
            
            for i, (data, title) in enumerate([(seg_counts, 'Clientes'), (seg_revenue, 'Ingresos')], 1):
                fig.add_trace(go.Pie(
                    labels=data.index, values=data.values,
                    name=title, hole=0.5,
                    marker=dict(colors=[seg_colors.get(s, '#666') for s in data.index],
                               line=dict(color='#0a0f1e', width=2)),
                    hovertemplate='<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>'
                ), 1, i)
            apply_chart_theme(fig, height=280)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col_risk:
            st.markdown('<div class="section-header">⏰ Cadencia de Compras</div>', unsafe_allow_html=True)
            cadence_data = client_stats.nlargest(10, 'Total_Ventas')[['CLIENTE', 'Cadencia_Dias', 'Riesgo']].copy()
            colors_risk = {'ALTO': '#ef4444', 'MEDIO': '#f59e0b', 'BAJO': '#00d68f'}
            
            fig = go.Figure(go.Bar(
                x=cadence_data['Cadencia_Dias'],
                y=cadence_data['CLIENTE'],
                orientation='h',
                marker=dict(
                    color=[colors_risk[r] for r in cadence_data['Riesgo']],
                    opacity=0.8,
                    line=dict(width=0)
                ),
                text=[f"{d:.0f}d" for d in cadence_data['Cadencia_Dias']],
                textposition='inside',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>Cadencia: %{x:.0f} días<extra></extra>'
            ))
            apply_chart_theme(fig, height=280)
            fig.update_layout(yaxis=dict(autorange='reversed'))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Tabla Interactiva
        st.markdown('<div class="section-header">📋 Tabla de Clientes <span class="section-tag">Filtrable</span></div>', unsafe_allow_html=True)
        
        seg_filter = st.multiselect("Segmento", ['VIP', 'A', 'B', 'C'], default=['VIP', 'A', 'B', 'C'])
        risk_filter = st.multiselect("Riesgo", ['ALTO', 'MEDIO', 'BAJO'], default=['ALTO', 'MEDIO', 'BAJO'])
        
        display_df = client_stats[
            (client_stats['Segmento'].isin(seg_filter)) &
            (client_stats['Riesgo'].isin(risk_filter))
        ].copy()
        
        display_df['Proxima_Compra'] = display_df['Proxima_Compra'].dt.strftime('%d/%m/%Y')
        display_df['Ultima_Compra'] = display_df['Ultima_Compra'].dt.strftime('%d/%m/%Y')
        
        show_cols = ['CLIENTE', 'Segmento', 'Riesgo', 'Total_Ventas', 'Total_Ordenes',
                    'Cadencia_Dias', 'Dias_Sin_Comprar', 'Ultima_Compra', 'Proxima_Compra']
        show_cols = [c for c in show_cols if c in display_df.columns]
        
        st.dataframe(
            display_df[show_cols].style.format({
                'Total_Ventas': '${:,.0f}',
                'Cadencia_Dias': '{:.0f}d',
                'Dias_Sin_Comprar': '{:.0f}d',
            }).background_gradient(subset=['Total_Ventas'], cmap='Blues')
             .background_gradient(subset=['Dias_Sin_Comprar'], cmap='Reds'),
            use_container_width=True,
            height=400
        )
        
        st.download_button("⬇️ Exportar análisis de clientes", 
                          display_df[show_cols].to_csv(index=False).encode(),
                          "clientes_analisis.csv", "text/csv")


# ════════════════════════════════════════════
# TAB 3: ANÁLISIS DE PRODUCTOS
# ════════════════════════════════════════════
with tabs[2]:
    
    if 'PRODUCTO' not in df.columns:
        st.warning("Columna PRODUCTO no encontrada.")
    else:
        prod_stats = df.groupby('PRODUCTO').agg(
            Total_Ventas=('VENTA_NETA', 'sum'),
            Total_Profit=('NET_PROFIT', 'sum') if 'NET_PROFIT' in df.columns else ('VENTA_NETA', 'sum'),
            Cantidad=('CANTIDAD', 'sum') if 'CANTIDAD' in df.columns else ('FECHA', 'count'),
            Margen=('NET_MARGIN', 'mean') if 'NET_MARGIN' in df.columns else ('VENTA_NETA', 'mean'),
            Ordenes=('FECHA', 'count')
        ).reset_index()
        prod_stats = prod_stats.sort_values('Total_Ventas', ascending=False)
        
        total_ventas_prod = prod_stats['Total_Ventas'].sum()
        prod_stats['Participacion'] = (prod_stats['Total_Ventas'] / total_ventas_prod * 100).round(1)
        prod_stats['Cum_Pct'] = prod_stats['Total_Ventas'].cumsum() / total_ventas_prod * 100
        
        def star_classify(row):
            if row['Margen'] >= prod_stats['Margen'].median() and row['Total_Ventas'] >= prod_stats['Total_Ventas'].median():
                return '⭐ Estrella'
            elif row['Margen'] >= prod_stats['Margen'].median():
                return '💎 Alta Rentabilidad'
            elif row['Total_Ventas'] >= prod_stats['Total_Ventas'].median():
                return '📦 Alto Volumen'
            return '⚠️ Problema'
        
        prod_stats['Clasificacion'] = prod_stats.apply(star_classify, axis=1)
        
        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        star_prods = (prod_stats['Clasificacion'] == '⭐ Estrella').sum()
        prob_prods = (prod_stats['Clasificacion'] == '⚠️ Problema').sum()
        best_margin = prod_stats.loc[prod_stats['Margen'].idxmax(), 'PRODUCTO'] if not prod_stats.empty else 'N/A'
        
        for col, icon, label, value, color in [
            (c1, "⭐", "Productos Estrella", str(star_prods), '#00d68f'),
            (c2, "⚠️", "Productos Problema", str(prob_prods), '#ef4444'),
            (c3, "📦", "Total Productos", str(len(prod_stats)), '#3b82f6'),
            (c4, "💎", "Mejor Margen", best_margin[:15] if len(best_margin) > 15 else best_margin, '#8b5cf6'),
        ]:
            with col:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:{color};"></div>
                <span class="kpi-icon">{icon}</span><div class="kpi-label">{label}</div>
                <div class="kpi-value" style="font-size:22px">{value}</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        # Charts
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="section-header">📊 Ranking por Ventas vs Margen</div>', unsafe_allow_html=True)
            top_prods = prod_stats.head(12)
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            fig.add_trace(go.Bar(
                x=top_prods['PRODUCTO'], y=top_prods['Total_Ventas'],
                name='Ventas', marker_color='#3b82f6', marker_line_width=0, opacity=0.85,
                hovertemplate='<b>%{x}</b><br>Ventas: $%{y:,.0f}<extra></extra>'
            ), secondary_y=False)
            
            fig.add_trace(go.Scatter(
                x=top_prods['PRODUCTO'], y=top_prods['Margen'],
                name='Margen %', mode='lines+markers',
                line=dict(color='#00d68f', width=2.5),
                marker=dict(size=8, color='#00d68f', line=dict(color='#0a0f1e', width=2)),
                hovertemplate='<b>%{x}</b><br>Margen: %{y:.1f}%<extra></extra>'
            ), secondary_y=True)
            
            apply_chart_theme(fig, height=360)
            fig.update_xaxes(tickangle=-45)
            fig.update_yaxes(secondary_y=True, ticksuffix='%', showgrid=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col_right:
            st.markdown('<div class="section-header">🎯 Matriz Estrella/Problema</div>', unsafe_allow_html=True)
            
            color_map = {'⭐ Estrella': '#00d68f', '💎 Alta Rentabilidad': '#8b5cf6',
                        '📦 Alto Volumen': '#3b82f6', '⚠️ Problema': '#ef4444'}
            
            fig = px.scatter(
                prod_stats, x='Total_Ventas', y='Margen',
                color='Clasificacion', size='Ordenes',
                text='PRODUCTO',
                color_discrete_map=color_map,
                hover_data={'Total_Ventas': ':$,.0f', 'Margen': ':.1f', 'Ordenes': True}
            )
            fig.update_traces(
                textposition='top center', textfont=dict(size=9, color='#94a3b8'),
                marker=dict(line=dict(color='#0a0f1e', width=1.5))
            )
            
            # Quadrant lines
            med_v = prod_stats['Total_Ventas'].median()
            med_m = prod_stats['Margen'].median()
            fig.add_vline(x=med_v, line_dash="dash", line_color="rgba(255,255,255,0.15)")
            fig.add_hline(y=med_m, line_dash="dash", line_color="rgba(255,255,255,0.15)")
            
            apply_chart_theme(fig, height=360)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Product Table
        st.markdown('<div class="section-header">📋 Detalle de Productos</div>', unsafe_allow_html=True)
        
        display_prod = prod_stats[['PRODUCTO', 'Clasificacion', 'Total_Ventas', 'Total_Profit', 'Margen', 'Cantidad', 'Participacion']].copy()
        
        st.dataframe(
            display_prod.style.format({
                'Total_Ventas': '${:,.0f}',
                'Total_Profit': '${:,.0f}',
                'Margen': '{:.1f}%',
                'Participacion': '{:.1f}%',
            }).background_gradient(subset=['Total_Ventas'], cmap='Blues')
             .background_gradient(subset=['Margen'], cmap='Greens'),
            use_container_width=True,
            height=350
        )


# ════════════════════════════════════════════
# TAB 4: ANÁLISIS AVANZADO
# ════════════════════════════════════════════
with tabs[3]:
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">🌡️ Heatmap de Actividad</div>', unsafe_allow_html=True)
        
        if 'CLIENTE' in df.columns and 'FECHA' in df.columns:
            top_clients = df.groupby('CLIENTE')['VENTA_NETA'].sum().nlargest(10).index
            heat_df = df[df['CLIENTE'].isin(top_clients)].copy()
            heat_df['Mes'] = heat_df['FECHA'].dt.strftime('%b %Y')
            heatmap_data = heat_df.groupby(['CLIENTE', 'Mes'])['VENTA_NETA'].sum().reset_index()
            heatmap_pivot = heatmap_data.pivot(index='CLIENTE', columns='Mes', values='VENTA_NETA').fillna(0)
            
            # Sort columns chronologically
            month_order = sorted(heatmap_pivot.columns, key=lambda x: pd.to_datetime(x, format='%b %Y'))
            heatmap_pivot = heatmap_pivot[month_order]
            
            fig = px.imshow(
                heatmap_pivot,
                color_continuous_scale=[[0, '#0a0f1e'], [0.3, '#1e3a5f'], [0.6, '#2563eb'], [1, '#00d68f']],
                aspect='auto',
                text_auto=False,
            )
            fig.update_traces(hovertemplate='<b>%{y}</b><br>%{x}<br>$%{z:,.0f}<extra></extra>')
            apply_chart_theme(fig, height=380)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown('<div class="section-header">📆 Estacionalidad Mensual</div>', unsafe_allow_html=True)
        
        monthly_avg = df.groupby(df['FECHA'].dt.month).agg(
            Ventas=('VENTA_NETA', 'sum'),
            Ordenes=('FECHA', 'count')
        ).reset_index()
        monthly_avg.columns = ['Mes_Num', 'Ventas', 'Ordenes']
        months_es = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        monthly_avg['Mes'] = monthly_avg['Mes_Num'].apply(lambda x: months_es[x-1] if 1 <= x <= 12 else str(x))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=monthly_avg['Mes'], y=monthly_avg['Ventas'],
            name='Ventas',
            marker=dict(
                color=monthly_avg['Ventas'],
                colorscale=[[0, 'rgba(59,130,246,0.4)'], [1, '#00d68f']],
                line=dict(width=0)
            ),
            hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
        ))
        apply_chart_theme(fig, height=380)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Month over Month
    st.markdown('<div class="section-header">📈 Comparativa Mes a Mes</div>', unsafe_allow_html=True)
    
    mom = df.groupby(df['FECHA'].dt.to_period('M').dt.start_time).agg(
        Ventas=('VENTA_NETA', 'sum'),
        Profit=('NET_PROFIT', 'sum') if 'NET_PROFIT' in df.columns else ('VENTA_NETA', 'sum'),
        Ordenes=('FECHA', 'count')
    ).reset_index()
    mom.columns = ['Periodo', 'Ventas', 'Profit', 'Ordenes']
    mom['MoM_Pct'] = mom['Ventas'].pct_change() * 100
    
    fig = make_subplots(rows=1, cols=2,
                       subplot_titles=['Ventas & Profit Mensual', 'Crecimiento % MoM'])
    
    fig.add_trace(go.Bar(x=mom['Periodo'], y=mom['Ventas'], name='Ventas',
                        marker_color='rgba(59,130,246,0.7)', marker_line_width=0,
                        hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'), 1, 1)
    fig.add_trace(go.Scatter(x=mom['Periodo'], y=mom['Profit'], name='Profit',
                            line=dict(color='#00d68f', width=2.5), mode='lines+markers',
                            hovertemplate='<b>%{x|%b %Y}</b><br>$%{y:,.0f}<extra></extra>'), 1, 1)
    
    colors_mom = ['#ef4444' if v < 0 else '#00d68f' for v in mom['MoM_Pct'].fillna(0)]
    fig.add_trace(go.Bar(x=mom['Periodo'], y=mom['MoM_Pct'],
                        name='Crecimiento %', marker_color=colors_mom, marker_line_width=0,
                        hovertemplate='<b>%{x|%b %Y}</b><br>%{y:.1f}%<extra></extra>'), 1, 2)
    
    apply_chart_theme(fig, height=360)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    # Projection
    st.markdown('<div class="section-header">🔮 Proyección Próximo Mes</div>', unsafe_allow_html=True)
    
    if len(mom) >= 3:
        recent = mom.tail(6)
        x = np.arange(len(recent))
        z = np.polyfit(x, recent['Ventas'], 1)
        p = np.poly1d(z)
        next_val = p(len(x))
        last_val = recent['Ventas'].iloc[-1]
        proj_pct = (next_val - last_val) / last_val * 100 if last_val > 0 else 0
        
        proj_color = '#00d68f' if proj_pct > 0 else '#ef4444'
        st.markdown(f"""
        <div style='background: var(--bg-card); border: 1px solid var(--border);
                    border-left: 4px solid {proj_color}; border-radius: 12px; padding: 20px 24px;
                    display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <div style='color: #64748b; font-size:12px; text-transform:uppercase; letter-spacing:0.5px; font-weight:600;'>
                    🔮 Proyección basada en tendencia lineal (últimos 6 meses)
                </div>
                <div style='font-family: Space Grotesk; font-size: 32px; font-weight: 700; color: #f1f5f9; margin-top: 8px;'>
                    {fmt_currency(max(0, next_val))}
                </div>
                <div style='color: {proj_color}; font-size: 14px; font-weight: 600; margin-top: 4px;'>
                    {'▲' if proj_pct >= 0 else '▼'} {abs(proj_pct):.1f}% vs mes actual
                </div>
            </div>
            <div style='font-size:64px;'>{'📈' if proj_pct >= 0 else '📉'}</div>
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════
# TAB 5: MÉTRICAS VIP & RECOMENDACIONES
# ════════════════════════════════════════════
with tabs[4]:
    
    if 'CLIENTE' not in df.columns:
        st.warning("Columna CLIENTE no encontrada.")
    else:
        # LTV & Advanced Metrics
        ltv_df = df.groupby('CLIENTE').agg(
            Total_Ventas=('VENTA_NETA', 'sum'),
            Total_Profit=('NET_PROFIT', 'sum') if 'NET_PROFIT' in df.columns else ('VENTA_NETA', 'sum'),
            Total_Ordenes=('FECHA', 'count'),
            Primera_Compra=('FECHA', 'min'),
            Ultima_Compra=('FECHA', 'max'),
        ).reset_index()
        
        ltv_df['Antiguedad_Meses'] = ((ltv_df['Ultima_Compra'] - ltv_df['Primera_Compra']).dt.days / 30).clip(lower=1)
        ltv_df['AOV'] = ltv_df['Total_Ventas'] / ltv_df['Total_Ordenes'].clip(lower=1)
        ltv_df['Frecuencia_Mensual'] = ltv_df['Total_Ordenes'] / ltv_df['Antiguedad_Meses']
        ltv_df['LTV'] = ltv_df['AOV'] * ltv_df['Frecuencia_Mensual'] * 12  # Annualized
        ltv_df['Dias_Sin_Comprar'] = (today - ltv_df['Ultima_Compra']).dt.days
        
        # Churn risk (0-100)
        max_dias = ltv_df['Dias_Sin_Comprar'].max() if ltv_df['Dias_Sin_Comprar'].max() > 0 else 1
        ltv_df['Churn_Risk'] = (ltv_df['Dias_Sin_Comprar'] / max_dias * 100).clip(0, 100).round(1)
        
        # VIP Score (0-100)
        def normalize(s):
            r = s.max() - s.min()
            return ((s - s.min()) / r * 100) if r > 0 else pd.Series([50]*len(s), index=s.index)
        
        ltv_df['Score'] = (
            normalize(ltv_df['Total_Ventas']) * 0.35 +
            normalize(ltv_df['Total_Ordenes']) * 0.20 +
            normalize(ltv_df['Frecuencia_Mensual']) * 0.25 +
            normalize(ltv_df['Total_Profit']) * 0.20
        ).round(1)
        
        # KPIs
        c1, c2, c3, c4 = st.columns(4)
        avg_ltv = ltv_df['LTV'].median()
        avg_aov = ltv_df['AOV'].mean()
        high_churn = (ltv_df['Churn_Risk'] > 70).sum()
        avg_score = ltv_df['Score'].mean()
        
        for col, icon, label, value, color in [
            (c1, "💰", "LTV Mediano Anual", fmt_currency(avg_ltv), '#00d68f'),
            (c2, "🛒", "AOV Promedio", fmt_currency(avg_aov), '#3b82f6'),
            (c3, "💔", "Alto Churn Risk", str(high_churn), '#ef4444'),
            (c4, "⭐", "Score VIP Prom.", f"{avg_score:.0f}/100", '#8b5cf6'),
        ]:
            with col:
                st.markdown(f"""<div class="kpi-card"><div class="kpi-accent-bar" style="background:{color};"></div>
                <span class="kpi-icon">{icon}</span><div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div></div>""", unsafe_allow_html=True)
        
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="section-header">💡 LTV por Cliente</div>', unsafe_allow_html=True)
            top_ltv = ltv_df.nlargest(10, 'LTV')
            fig = px.bar(top_ltv, x='LTV', y='CLIENTE', orientation='h',
                        color='Score',
                        color_continuous_scale=[[0, '#1e3a5f'], [0.5, '#3b82f6'], [1, '#00d68f']],
                        text=[fmt_currency(v) for v in top_ltv['LTV']])
            fig.update_traces(textposition='inside', textfont=dict(color='white', size=11),
                             marker_line_width=0,
                             hovertemplate='<b>%{y}</b><br>LTV: $%{x:,.0f}<extra></extra>')
            apply_chart_theme(fig, height=380)
            fig.update_layout(yaxis=dict(autorange='reversed'), coloraxis_showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col_right:
            st.markdown('<div class="section-header">⚡ VIP Score vs Churn Risk</div>', unsafe_allow_html=True)
            fig = px.scatter(ltv_df, x='Score', y='Churn_Risk',
                           size='Total_Ventas', color='LTV',
                           text='CLIENTE',
                           color_continuous_scale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#00d68f']],
                           hover_data={'Total_Ventas': ':$,.0f', 'AOV': ':$,.0f'})
            fig.update_traces(
                textposition='top center', textfont=dict(size=8, color='#64748b'),
                marker=dict(line=dict(color='#0a0f1e', width=1.5))
            )
            fig.add_vline(x=50, line_dash="dash", line_color="rgba(255,255,255,0.1)")
            fig.add_hline(y=50, line_dash="dash", line_color="rgba(255,255,255,0.1)")
            
            fig.add_annotation(x=80, y=80, text="⚠️ Alto Riesgo / Alto Valor", 
                              font=dict(color='#fbbf24', size=10), showarrow=False)
            fig.add_annotation(x=80, y=15, text="✅ Leal & Valioso", 
                              font=dict(color='#34d399', size=10), showarrow=False)
            
            apply_chart_theme(fig, height=380)
            fig.update_coloraxes(showscale=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Recommendations
        st.markdown('<div class="section-header">🎯 Recomendaciones Automáticas</div>', unsafe_allow_html=True)
        
        rec_cols = st.columns(3)
        
        with rec_cols[0]:
            st.markdown("**🔴 Contactar Urgente (Riesgo Churn)**")
            urgent = ltv_df.nlargest(5, 'Churn_Risk')[['CLIENTE', 'Dias_Sin_Comprar', 'LTV']].copy()
            for _, row in urgent.iterrows():
                st.markdown(f"""
                <div style='background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.15);
                            border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;'>
                    <div style='font-weight:600; color:#f1f5f9; font-size:13px;'>{row['CLIENTE']}</div>
                    <div style='color:#94a3b8; font-size:11px; margin-top:3px;'>
                        {row['Dias_Sin_Comprar']:.0f} días inactivo · LTV {fmt_currency(row['LTV'])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with rec_cols[1]:
            st.markdown("**🟡 Upsell Opportunity**")
            upsell = ltv_df[ltv_df['Score'] > ltv_df['Score'].median()].nsmallest(5, 'Total_Ordenes')[['CLIENTE', 'AOV', 'Score']].copy()
            for _, row in upsell.iterrows():
                st.markdown(f"""
                <div style='background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.15);
                            border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;'>
                    <div style='font-weight:600; color:#f1f5f9; font-size:13px;'>{row['CLIENTE']}</div>
                    <div style='color:#94a3b8; font-size:11px; margin-top:3px;'>
                        AOV {fmt_currency(row['AOV'])} · Score {row['Score']:.0f}/100
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with rec_cols[2]:
            st.markdown("**🟢 Top Performers (Mantener)**")
            top_perf = ltv_df.nlargest(5, 'Score')[['CLIENTE', 'Score', 'LTV']].copy()
            for _, row in top_perf.iterrows():
                st.markdown(f"""
                <div style='background: rgba(0,214,143,0.06); border: 1px solid rgba(0,214,143,0.15);
                            border-radius: 10px; padding: 12px 14px; margin-bottom: 8px;'>
                    <div style='font-weight:600; color:#f1f5f9; font-size:13px;'>{row['CLIENTE']}</div>
                    <div style='color:#94a3b8; font-size:11px; margin-top:3px;'>
                        Score {row['Score']:.0f}/100 · LTV {fmt_currency(row['LTV'])}
                    </div>
                    <div class="score-bar-container" style="margin-top:6px;">
                        <div class="score-bar-fill" style="width:{row['Score']}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Full VIP table
        st.markdown('<div class="section-header">📋 Score Completo de Clientes</div>', unsafe_allow_html=True)
        
        display_ltv = ltv_df.sort_values('Score', ascending=False)[
            ['CLIENTE', 'Score', 'LTV', 'AOV', 'Frecuencia_Mensual', 'Total_Ordenes', 'Churn_Risk', 'Dias_Sin_Comprar']
        ].copy()
        
        st.dataframe(
            display_ltv.style.format({
                'Score': '{:.0f}',
                'LTV': '${:,.0f}',
                'AOV': '${:,.0f}',
                'Frecuencia_Mensual': '{:.2f}x/mes',
                'Churn_Risk': '{:.0f}%',
                'Dias_Sin_Comprar': '{:.0f}d',
            }).background_gradient(subset=['Score'], cmap='Greens')
             .background_gradient(subset=['Churn_Risk'], cmap='Reds'),
            use_container_width=True,
            height=420
        )
        
        st.download_button("⬇️ Exportar métricas VIP",
                          display_ltv.to_csv(index=False).encode(),
                          "metricas_vip.csv", "text/csv")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding: 32px 0 16px; color: #334155; font-size: 12px;'>
    <div style='margin-bottom: 6px;'>Sales Intelligence Dashboard · Datos en tiempo real desde Google Sheets</div>
    <div style='color: #1e293b;'>Construido con Streamlit + Plotly · Actualización automática cada 5 minutos</div>
</div>
""", unsafe_allow_html=True)

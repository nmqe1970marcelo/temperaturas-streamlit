import streamlit as st

# ── Configuración de la página ──────────────────────────────────────────────
st.set_page_config(
    page_title="Conversor de Temperaturas",
    page_icon="🌡️",
    layout="centered",
)

# ── Estilos personalizados ───────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Inter:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main { background-color: #0d1117; }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Tarjeta de resultado */
    .result-card {
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border: 1px solid #374151;
        border-radius: 16px;
        padding: 28px 32px;
        margin: 16px 0;
        text-align: center;
    }
    .result-unit {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 6px;
    }
    .result-value {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 48px;
        font-weight: 700;
        color: #f9fafb;
        line-height: 1.1;
    }
    .result-value span {
        font-size: 28px;
        color: #9ca3af;
    }

    /* Paleta de escala de color */
    .celsius  { border-top: 3px solid #3b82f6; }
    .fahrenheit { border-top: 3px solid #f59e0b; }
    .kelvin   { border-top: 3px solid #8b5cf6; }

    /* Badge de escala */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 20px;
    }
    .badge-c  { background: #1d4ed8; color: #bfdbfe; }
    .badge-f  { background: #b45309; color: #fde68a; }
    .badge-k  { background: #6d28d9; color: #ddd6fe; }

    /* Separador */
    hr { border-color: #1f2937; margin: 32px 0; }

    /* Subtítulo con fórmula */
    .formula-box {
        background: #161b22;
        border-radius: 10px;
        padding: 14px 20px;
        font-family: 'Space Grotesk', monospace;
        font-size: 13px;
        color: #9ca3af;
        margin-top: 24px;
        border: 1px solid #21262d;
    }
    .formula-box code { color: #58a6ff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Funciones de conversión ──────────────────────────────────────────────────
def celsius_to_fahrenheit(c: float) -> float:
    return (c * 9 / 5) + 32

def celsius_to_kelvin(c: float) -> float:
    return c + 273.15

def fahrenheit_to_celsius(f: float) -> float:
    return (f - 32) * 5 / 9

def fahrenheit_to_kelvin(f: float) -> float:
    return fahrenheit_to_celsius(f) + 273.15

def kelvin_to_celsius(k: float) -> float:
    return k - 273.15

def kelvin_to_fahrenheit(k: float) -> float:
    return celsius_to_fahrenheit(kelvin_to_celsius(k))

# ── Encabezado ───────────────────────────────────────────────────────────────
st.markdown("## 🌡️ Conversor de Temperaturas")
st.markdown(
    "Convierte entre **Celsius**, **Fahrenheit** y **Kelvin** al instante. "
    "Ingresa el valor y selecciona la unidad de origen."
)
st.markdown("---")

# ── Controles de entrada ─────────────────────────────────────────────────────
col_input, col_unit = st.columns([2, 1])

with col_input:
    valor = st.number_input(
        "Valor de temperatura",
        value=0.0,
        step=0.1,
        format="%.2f",
        help="Ingresa el valor numérico a convertir.",
    )

with col_unit:
    unidad = st.selectbox(
        "Unidad de origen",
        options=["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
    )

# ── Validación de Kelvin negativo ────────────────────────────────────────────
if unidad == "Kelvin (K)" and valor < 0:
    st.error("⚠️ El cero absoluto es 0 K. No existen valores negativos en Kelvin.")
    st.stop()

if unidad == "Celsius (°C)" and valor < -273.15:
    st.error("⚠️ El valor mínimo en Celsius es −273.15 °C (cero absoluto).")
    st.stop()

if unidad == "Fahrenheit (°F)" and valor < -459.67:
    st.error("⚠️ El valor mínimo en Fahrenheit es −459.67 °F (cero absoluto).")
    st.stop()

# ── Cálculos ─────────────────────────────────────────────────────────────────
if unidad == "Celsius (°C)":
    c, f, k = valor, celsius_to_fahrenheit(valor), celsius_to_kelvin(valor)
    badge_class, badge_text = "badge-c", "Origen · Celsius"
    formulas = (
        "°F = (°C × 9/5) + 32 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "K = °C + 273.15"
    )

elif unidad == "Fahrenheit (°F)":
    c, f, k = fahrenheit_to_celsius(valor), valor, fahrenheit_to_kelvin(valor)
    badge_class, badge_text = "badge-f", "Origen · Fahrenheit"
    formulas = (
        "°C = (°F − 32) × 5/9 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "K = °C + 273.15"
    )

else:  # Kelvin
    c, f, k = kelvin_to_celsius(valor), kelvin_to_fahrenheit(valor), valor
    badge_class, badge_text = "badge-k", "Origen · Kelvin"
    formulas = (
        "°C = K − 273.15 &nbsp;&nbsp;|&nbsp;&nbsp; "
        "°F = (°C × 9/5) + 32"
    )

# ── Resultados ───────────────────────────────────────────────────────────────
st.markdown(
    f'<div class="badge {badge_class}">{badge_text}</div>',
    unsafe_allow_html=True,
)

cols = st.columns(3)

tarjetas = [
    ("celsius",     "Celsius",     f"{c:.4f}", "°C"),
    ("fahrenheit",  "Fahrenheit",  f"{f:.4f}", "°F"),
    ("kelvin",      "Kelvin",      f"{k:.4f}", "K"),
]

for col, (css_class, label, val, sym) in zip(cols, tarjetas):
    with col:
        st.markdown(
            f"""
            <div class="result-card {css_class}">
                <div class="result-unit">{label}</div>
                <div class="result-value">{val}<span> {sym}</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Fórmulas utilizadas ───────────────────────────────────────────────────────
st.markdown(
    f'<div class="formula-box">📐 Fórmulas aplicadas: <code>{formulas}</code></div>',
    unsafe_allow_html=True,
)

# ── Tabla comparativa rápida ─────────────────────────────────────────────────
with st.expander("📊 Ver tabla de referencia rápida"):
    st.markdown("Puntos de referencia comunes:")
    datos = {
        "Referencia": [
            "Cero absoluto",
            "Congelación del agua",
            "Temperatura corporal",
            "Ebullición del agua",
        ],
        "Celsius (°C)": [-273.15, 0, 37, 100],
        "Fahrenheit (°F)": [-459.67, 32, 98.6, 212],
        "Kelvin (K)": [0, 273.15, 310.15, 373.15],
    }
    st.dataframe(datos, use_container_width=True, hide_index=True)

# ── Pie de página ────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("Conversor de Temperaturas · Celsius · Fahrenheit · Kelvin")

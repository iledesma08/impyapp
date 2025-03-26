# Importaciones necesarias para la app
import customtkinter as ctk
import requests
import locale
import webbrowser
import re
from PIL import Image
from customtkinter import CTkImage

# Configura el locale del sistema para mostrar los montos en formato ARS
locale.setlocale(locale.LC_ALL, '')

# Modo oscuro y tema visual
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Inicialización de la ventana principal
root = ctk.CTk()
root.title("Conversor USD-ARS con Impuestos")
root.geometry("420x600")

# === FUNCIONES AUXILIARES ===

# Función para normalizar entradas numéricas en formatos como:
# 1.319,42 / 1319,42 / 1319.42 → 1319.42
def parsear_numero(texto):
    texto = texto.strip()

    # Si contiene punto y coma, se asume formato europeo: 1.319,42 → 1319.42
    if '.' in texto and ',' in texto:
        texto = texto.replace('.', '').replace(',', '.')
    # Si solo tiene coma, se asume coma como separador decimal: 1319,42 → 1319.42
    elif ',' in texto:
        texto = texto.replace(',', '.')
    # Si tiene múltiples puntos, eliminar los que no sean decimales
    elif texto.count('.') > 1:
        partes = texto.split('.')
        texto = ''.join(partes[:-1]) + '.' + partes[-1]

    try:
        return float(texto)
    except ValueError:
        return None

# Abre la web de Dolarya para consultar cotización Astropay
def abrir_dolarya():
    webbrowser.open_new("https://www.dolarya.info/astropay")

# === CONFIGURACIÓN DE DATOS ===

# Comisiones por entidad para operar MEP
mep_entidades = dict(sorted({
    "MercadoPago (1%)": 0.01,
    "Brubank (1%)": 0.01,
    "Reba (1.2%)": 0.012,
    "Cocos Capital (1.21%)": 0.0121,
    "Invertir Online (1.21%)": 0.0121,
    "Balanz (1.21%)": 0.0121,
    "Ualá (1.5%)": 0.015,
    "Santander Río (1.5%)": 0.015,
    "Portfolio Personal (1.5%)": 0.015,
    "Buenbit (1.7%)": 0.017,
    "Personal Pay (2%)": 0.02,
    "Galicia Move (2%)": 0.02,
    "BBVA Argentina (2%)": 0.02,
    "HSBC Argentina (2%)": 0.02,
    "Naranja X (2.5%)": 0.025
}.items(), key=lambda x: x[1]))

# Percepciones por provincia para cálculo de IIBB
iibb_provincias = dict(sorted({
    "Chaco (5.5%)": 0.055,
    "Misiones (5.0%)": 0.05,
    "Formosa (5.0%)": 0.05,
    "Santiago del Estero (4.5%)": 0.045,
    "Tucumán (4.0%)": 0.04,
    "Jujuy (4.0%)": 0.04,
    "Salta (3.6%)": 0.036,
    "Buenos Aires (3.5%)": 0.035,
    "Córdoba (3%)": 0.03,
    "Santa Fe (3%)": 0.03,
    "Mendoza (3%)": 0.03,
    "Entre Ríos (3%)": 0.03,
    "Neuquén (3%)": 0.03,
    "Río Negro (3%)": 0.03,
    "La Pampa (3%)": 0.03,
    "San Juan (3%)": 0.03,
    "Catamarca (3%)": 0.03,
    "San Luis (3%)": 0.03,
    "La Rioja (3%)": 0.03,
    "Chubut (3%)": 0.03,
    "Santa Cruz (3%)": 0.03,
    "Corrientes (3%)": 0.03,
    "CABA (2%)": 0.02,
    "Tierra del Fuego (0%)": 0.0
}.items(), key=lambda x: x[1], reverse=True))

# === FUNCIONES PRINCIPALES ===

def convertir_usd():
    # Leer y convertir entradas
    usd_amount = parsear_numero(usd_entry.get())
    astro_rate = parsear_numero(astro_entry.get())

    if usd_amount is None:
        conversion_result.configure(text="Monto USD inválido.")
        return
    if astro_entry.get().strip() and astro_rate is None:
        conversion_result.configure(text="Cotización Astropay inválida.")
        return

    # Obtener datos de la API
    try:
        response = requests.get("https://dolarapi.com/v1/dolares", timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception:
        conversion_result.configure(text="Error al obtener datos de la API.")
        return

    # Extraer cotizaciones relevantes
    rates = {
        item.get("casa"): float(item.get("venta") or item.get("compra") or 0)
        for item in data if item.get("casa") in ("tarjeta", "bolsa", "cripto")
    }

    results = []
    if "tarjeta" in rates:
        results.append(("Dólar Tarjeta", round(usd_amount * rates["tarjeta"], 2)))
    if "bolsa" in rates:
        entidad = entidad_mep_menu.get()
        comision = mep_entidades.get(entidad, 0.01)
        adjusted_mep = rates["bolsa"] * (1 + comision)
        results.append((f"Dólar MEP ({entidad})", round(usd_amount * adjusted_mep, 2)))
    if "cripto" in rates:
        results.append(("Dólar Cripto", round(usd_amount * rates["cripto"], 2)))
    if astro_rate:
        results.append(("Astropay Global", round(usd_amount * astro_rate, 2)))

    if not results:
        conversion_result.configure(text="No se obtuvieron cotizaciones.")
        return

    # Mostrar resultados ordenados por menor costo
    results.sort(key=lambda x: x[1])
    texto = "\n".join(f"{nombre}: {locale.currency(valor, grouping=True)}" for nombre, valor in results)
    conversion_result.configure(text=texto)

def calcular_impuestos():
    base = parsear_numero(ars_entry.get())
    if base is None:
        impuestos_result.configure(text="Monto ARS inválido.")
        return

    # Cálculo de impuestos sobre el monto ingresado
    iva = base * 0.21
    ganancias = base * 0.30
    provincia = provincia_menu.get()
    iibb = base * iibb_provincias.get(provincia, 0.03)
    total = base + iva + ganancias + iibb

    resultado = (
        f"Monto base: {locale.currency(base, grouping=True)}\n"
        f"IVA (21%): {locale.currency(iva, grouping=True)}\n"
        f"Percep. Ganancias (30%): {locale.currency(ganancias, grouping=True)}\n"
        f"IIBB {provincia}: {locale.currency(iibb, grouping=True)}\n"
        f"Total con impuestos: {locale.currency(total, grouping=True)}"
    )
    impuestos_result.configure(text=resultado)

# === UTILIDAD PARA CREAR FILAS DE ENTRADA ===
def crear_fila(frame, texto, entry_width=100):
    fila = ctk.CTkFrame(frame)
    fila.pack(pady=5)
    ctk.CTkLabel(fila, text=texto).pack(side="left", padx=5)
    entry = ctk.CTkEntry(fila, width=entry_width)
    entry.pack(side="left", padx=5)
    return entry

# === INTERFAZ GRÁFICA ===

# Sección para conversión
frame_conversion = ctk.CTkFrame(root)
frame_conversion.pack(padx=20, pady=10, fill="x")
ctk.CTkLabel(frame_conversion, text="Conversión USD a ARS", font=("Arial", 16)).pack(pady=5)

usd_entry = crear_fila(frame_conversion, "Monto en USD:")

# Entrada para cotización de Astropay con botón a Dolarya
fila_astro = ctk.CTkFrame(frame_conversion)
fila_astro.pack(pady=5)
ctk.CTkLabel(fila_astro, text="Cotización Astropay (ARS/USD):").pack(side="left", padx=5)
astro_entry = ctk.CTkEntry(fila_astro, width=100)
astro_entry.pack(side="left", padx=5)

# Botón con icono Dolarya
try:
    image = Image.open("img/dolarya.png").resize((20, 20))
    icon = CTkImage(light_image=image, dark_image=image, size=(20, 20))
    boton_dolarya = ctk.CTkButton(fila_astro, text="", image=icon, width=30, command=abrir_dolarya)
    boton_dolarya.pack(side="left", padx=5)
except:
    boton_dolarya = ctk.CTkButton(fila_astro, text="🔗", width=30, command=abrir_dolarya)
    boton_dolarya.pack(side="left", padx=5)

# Selección de entidad MEP
row3 = ctk.CTkFrame(frame_conversion)
row3.pack(pady=5)
ctk.CTkLabel(row3, text="Entidad para MEP:").pack(side="left", padx=5)
entidad_mep_menu = ctk.CTkOptionMenu(row3, values=list(mep_entidades.keys()))
entidad_mep_menu.pack(side="left", padx=5)
entidad_mep_menu.set("MercadoPago (1%)")

# Botón para convertir
ctk.CTkButton(frame_conversion, text="Convertir USD a ARS", command=convertir_usd).pack(pady=10)
conversion_result = ctk.CTkLabel(frame_conversion, text="", justify="left")
conversion_result.pack(pady=5)

# Sección para cálculo de impuestos
frame_impuestos = ctk.CTkFrame(root)
frame_impuestos.pack(padx=20, pady=10, fill="x")
ctk.CTkLabel(frame_impuestos, text="Cálculo de Impuestos", font=("Arial", 16)).pack(pady=5)

ars_entry = crear_fila(frame_impuestos, "Monto en ARS:")

# Menú de selección de provincia
row_provincia = ctk.CTkFrame(frame_impuestos)
row_provincia.pack(pady=5)
ctk.CTkLabel(row_provincia, text="Provincia: ").pack(side="left", padx=5)
provincia_menu = ctk.CTkOptionMenu(row_provincia, values=list(iibb_provincias.keys()))
provincia_menu.pack(side="left", padx=5)
provincia_menu.set("Córdoba (3%)")

# Botón para calcular impuestos
ctk.CTkButton(frame_impuestos, text="Calcular Impuestos", command=calcular_impuestos).pack(pady=10)
impuestos_result = ctk.CTkLabel(frame_impuestos, text="", justify="left")
impuestos_result.pack(pady=5)

# Crédito de la API
ctk.CTkLabel(root, text="Dólar API provisto por dolarapi.com", font=("Arial", 10)).pack(side="bottom", pady=2)

# Inicio de la app
tkloop = root.mainloop()
# === IMPORTACIÓN DE MÓDULOS ===
import customtkinter as ctk             # Interfaz gráfica personalizada (basada en tkinter)
import requests                         # Para hacer solicitudes HTTP a la API de cotización
import locale                           # Para formato numérico local (ej: separadores y símbolo $)
import webbrowser                       # Para abrir enlaces en el navegador
from PIL import Image, ImageTk          # Para cargar y mostrar imágenes (ícono de Dolarya)

# === CONFIGURACIÓN INICIAL ===

locale.setlocale(locale.LC_ALL, '')     # Aplica formato de moneda regional (ej: ARS con punto/miles)

# Configuración visual del tema oscuro
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Inicializa ventana principal
root = ctk.CTk()
root.title("Conversor USD-ARS con Impuestos")
root.geometry("420x600")

# === DATOS DE REFERENCIA ===

# Diccionario de entidades para operar MEP con sus comisiones (ordenadas de menor a mayor)
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
}.items(), key=lambda x: x[1], reverse=False))

# Diccionario de provincias y su percepción IIBB asociada (ordenadas de mayor a menor)
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

# === FUNCIONES AUXILIARES ===

def es_numero(val):
    """Valida si un string puede convertirse a float."""
    try:
        float(val)
        return True
    except ValueError:
        return False

def abrir_dolarya():
    """Abre la página de Dolarya para ver la cotización Astropay."""
    webbrowser.open_new("https://www.dolarya.info/astropay")

# === LÓGICA PRINCIPAL ===

def convertir_usd():
    """Obtiene cotizaciones y convierte el monto en USD a ARS según distintas fuentes."""
    usd_text = usd_entry.get().strip()
    astro_text = astro_entry.get().strip()

    # Validaciones
    if not es_numero(usd_text):
        conversion_result.configure(text="Monto USD inválido.")
        return
    if astro_text and not es_numero(astro_text):
        conversion_result.configure(text="Cotización Astropay inválida.")
        return

    usd_amount = float(usd_text)
    astro_rate = float(astro_text) if astro_text else 0.0

    # Consulta API de cotizaciones
    try:
        response = requests.get("https://dolarapi.com/v1/dolares", timeout=5)
        response.raise_for_status()
        data = response.json()
    except Exception:
        conversion_result.configure(text="Error al obtener datos de la API.")
        return

    # Filtra las tasas de interés útiles
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
    if astro_rate > 0:
        results.append(("Astropay Global", round(usd_amount * astro_rate, 2)))

    # Mostrar resultados
    if not results:
        conversion_result.configure(text="No se obtuvieron cotizaciones.")
        return

    results.sort(key=lambda x: x[1])
    output_lines = [f"{nombre}: {locale.currency(monto, grouping=True)}" for nombre, monto in results]
    conversion_result.configure(text="\n".join(output_lines))

def calcular_impuestos():
    """Calcula los impuestos aplicables sobre un monto en ARS."""
    ars_text = ars_entry.get().strip()
    if not es_numero(ars_text):
        impuestos_result.configure(text="Monto ARS inválido.")
        return

    base = float(ars_text)
    iva = base * 0.21
    ganancia = base * 0.30
    provincia = provincia_menu.get()
    iibb_rate = iibb_provincias.get(provincia, 0.03)
    iibb = base * iibb_rate
    total = base + iva + ganancia + iibb

    resultado = (
        f"Monto base: {locale.currency(base, grouping=True)}\n"
        f"IVA (21%): {locale.currency(iva, grouping=True)}\n"
        f"Percep. Ganancias (30%): {locale.currency(ganancia, grouping=True)}\n"
        f"IIBB {provincia}: {locale.currency(iibb, grouping=True)}\n"
        f"Total con impuestos: {locale.currency(total, grouping=True)}"
    )
    impuestos_result.configure(text=resultado)

def crear_fila(frame, texto, entry_width=100):
    """Crea una fila con una etiqueta y un campo de entrada."""
    fila = ctk.CTkFrame(frame)
    fila.pack(pady=5)
    ctk.CTkLabel(fila, text=texto).pack(side="left", padx=5)
    entry = ctk.CTkEntry(fila, width=entry_width)
    entry.pack(side="left", padx=5)
    return entry

# === INTERFAZ GRÁFICA ===

# Sección: Conversión USD a ARS
frame_conversion = ctk.CTkFrame(root)
frame_conversion.pack(padx=20, pady=10, fill="x")
ctk.CTkLabel(frame_conversion, text="Conversión USD a ARS", font=("Arial", 16)).pack(pady=5)

usd_entry = crear_fila(frame_conversion, "Monto en USD:")

# Fila de Astropay con ícono de Dolarya
fila_astro = ctk.CTkFrame(frame_conversion)
fila_astro.pack(pady=5)
ctk.CTkLabel(fila_astro, text="Cotización Astropay (ARS/USD):").pack(side="left", padx=5)
astro_entry = ctk.CTkEntry(fila_astro, width=100)
astro_entry.pack(side="left", padx=5)

# Ícono de Dolarya como botón (abre navegador)
try:
    image = Image.open("img/dolarya.png").resize((20, 20))
    icon = ImageTk.PhotoImage(image)
    boton_dolarya = ctk.CTkButton(fila_astro, text="", image=icon, width=30, command=abrir_dolarya)
    boton_dolarya.pack(side="left", padx=5)
except:
    boton_dolarya = ctk.CTkButton(fila_astro, text="🔗", width=30, command=abrir_dolarya)
    boton_dolarya.pack(side="left", padx=5)

# Menú desplegable de entidades MEP
row3 = ctk.CTkFrame(frame_conversion)
row3.pack(pady=5)
ctk.CTkLabel(row3, text="Entidad para MEP:").pack(side="left", padx=5)
entidad_mep_menu = ctk.CTkOptionMenu(row3, values=list(mep_entidades.keys()))
entidad_mep_menu.pack(side="left", padx=5)
entidad_mep_menu.set("MercadoPago (1%)")

# Botón de conversión
ctk.CTkButton(frame_conversion, text="Convertir USD a ARS", command=convertir_usd).pack(pady=10)
conversion_result = ctk.CTkLabel(frame_conversion, text="", justify="left")
conversion_result.pack(pady=5)

# Sección: Cálculo de impuestos
frame_impuestos = ctk.CTkFrame(root)
frame_impuestos.pack(padx=20, pady=10, fill="x")
ctk.CTkLabel(frame_impuestos, text="Cálculo de Impuestos", font=("Arial", 16)).pack(pady=5)

ars_entry = crear_fila(frame_impuestos, "Monto en ARS:")

# Menú desplegable de provincias
row_provincia = ctk.CTkFrame(frame_impuestos)
row_provincia.pack(pady=5)
ctk.CTkLabel(row_provincia, text="Provincia: ").pack(side="left", padx=5)
provincia_menu = ctk.CTkOptionMenu(row_provincia, values=list(iibb_provincias.keys()))
provincia_menu.pack(side="left", padx=5)
provincia_menu.set("Córdoba (3%)")

# Botón de cálculo de impuestos
ctk.CTkButton(frame_impuestos, text="Calcular Impuestos", command=calcular_impuestos).pack(pady=10)
impuestos_result = ctk.CTkLabel(frame_impuestos, text="", justify="left")
impuestos_result.pack(pady=5)

# Etiqueta final informativa
ctk.CTkLabel(root, text="Dólar API provisto por dolarapi.com", font=("Arial", 10)).pack(side="bottom", pady=2)

# Ejecuta la app
root.mainloop()

# 💱 Conversor USD-ARS con Impuestos (IMPYAPP)

Aplicación de escritorio con interfaz gráfica desarrollada en Python. Permite:

- Convertir montos en USD a pesos argentinos (ARS) según múltiples tipos de cambio:
  - Dólar Tarjeta
  - Dólar MEP (ajustado por entidad)
  - Dólar Cripto
  - Astropay (cotización ingresada manualmente)
- Calcular impuestos aplicables en compras dentro de Argentina:
  - IVA (21%)
  - Percepción Ganancias (30%)
  - Ingresos Brutos Córdoba (3%)

## 🖥️ Captura de pantalla

![image](https://github.com/user-attachments/assets/d2607c92-1520-406f-ab0b-897b41c3d1bc)

## 🚀 Cómo usar

1. Descargar el archivo `.exe` y ejecutarlo
2. Ingresar un valor en USD o ARS en alguno de los 2 campos correspondientes:
   - Si se desea convertir un valor de USD a ARS, se puede ingresar manualmente y de forma opcional la cotización de Astropay o cambiar la comisión de compra de dólar MEP a la entidad deseada.
   - Si se desea calcular los impuestos de un gasto en ARS en un producto extranjero, se puede cambiar el impuesto adicional vigente por provincia.
3. Seleccionar `Convertir USD a ARS` o `Calcular Impuestos`

## ⚙️ Entidades soportadas para MEP

Se pueden elegir entidades como MercadoPago, Brubank, Ualá, Santander, Galicia, Balanz, entre otras. Cada una tiene su comisión predefinida, la cual se aplica al dólar MEP como spread adicional.

## 🧠 Fuentes de datos

- Cotizaciones obtenidas en tiempo real desde [dolarapi.com](https://dolarapi.com)
- Cotizaciones adicionales para Astropay pueden obtenerse desde [dolarito.ar](https://www.dolarito.ar/) o [dolarya.info](https://www.dolarya.info/)
- Comisiones de compra de dolar MEP para las distintas entidades se pueden obtener buscando en las correspondientes páginas web de cada entidad.

## 📄 Licencia

MIT License.

## 🤝 Contribuciones

¡Bienvenidas! Podés hacer un fork del repo y abrir un Pull Request.

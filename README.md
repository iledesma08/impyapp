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

![image](https://github.com/user-attachments/assets/aa3ab7b9-f826-4095-ae69-a967fdf62627)

## 🚀 Cómo usar

1. Descargar el archivo `.exe` y ejecutarlo
2. Ingresar un valor en USD o ARS en alguno de los 2 campos correspondientes:
   - Si se desea convertir un valor de USD a ARS se puede:
     - Ingresar manualmente y de forma opcional la cotización de Astropay (a la que se puede acceder de forma directa a través del botón 🔗)
     - Cambiar la comisión de compra de dólar MEP a la entidad deseada.
   - Si se desea calcular los impuestos de un gasto en ARS en un producto extranjero, se puede cambiar el impuesto adicional vigente por provincia.
3. Seleccionar `Convertir USD a ARS` o `Calcular Impuestos` según corresponda.

## ⚙️ Entidades soportadas para MEP

Se pueden elegir entidades como MercadoPago, Brubank, Ualá, Santander, Galicia, Balanz, entre otras. Cada una tiene su comisión predefinida, la cual se aplica al dólar MEP como spread adicional.

## 🧠 Fuentes de datos

- Cotizaciones obtenidas en tiempo real desde [dolarapi.com](https://dolarapi.com)
- Cotizaciones adicionales para Astropay obtenidas desde [dolarya.info](https://www.dolarya.info/)

## 📄 Licencia

MIT License.

## 🤝 Contribuciones

¡Bienvenidas! Podés hacer un fork del repo y abrir un Pull Request.

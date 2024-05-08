import streamlit as st
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
st.set_page_config(
    page_title="Presupuestos",
    page_icon="📁")

# Función para crear el PDF
def create_pdf(data, services):
    c = canvas.Canvas("presupuesto.pdf", pagesize=landscape(letter))
    c.setFont("Helvetica-Bold", 11)
    width, height = landscape(letter)  # Tamaño de página horizontal
    # Insertar logo
    c.drawInlineImage('refri.jpg', 20, height - 120, width=120, height=100)

    # Datos de la empresa a la izquierda
    c.drawString(140, height - 40, f"Empresa: {data['empresa']}")
    c.drawString(140, height - 60, f"Teléfono: {data['telefono_empresa']}")
    c.drawInlineImage('instagram.png', 140, height - 86, width=20, height=20)
    c.drawString(165, height - 80, f"@refrimat05")

    # Datos del cliente a la derechaa
    c.drawString(width - 300, height - 40, f"Cliente: {data['cliente'].capitalize()}")
    c.drawString(width - 300, height - 60, f"Telefono: {data['telefono_cliente']}")

# Configurar la fuente para el título
    date_str = datetime.now().strftime('%d/%m/%Y')
    c.setFont("Helvetica-Bold", 18)  # Fuente en negrita con tamaño 18

# Dibujar el título en el centro superior de la página
    c.drawCentredString(width / 2, height - 130, f"Presupuesto de Servicios al dia {date_str}")

    # Tabla de servicios
    c.setFont("Helvetica-Bold", 11)
    y_position = height - 180
    c.drawString(30, y_position, "Descripción")
    c.drawString(330, y_position, "Cantidad")
    c.drawString(430, y_position, "Precio Unitario")
    c.drawString(580, y_position, "Total")

    subtotal = 0
    c.setFont("Helvetica", 10) 
    for service in services:
        y_position -= 20
        c.drawString(30, y_position, f"- {service['description'].capitalize()}")
        c.drawString(350, y_position, str(service['quantity']))
        c.drawString(450, y_position, f"$ {service['unit_price']}")
        total = service['quantity'] * service['unit_price']
        c.drawString(580, y_position, f"$ {total}")
        subtotal += total

    # Subtotal, IVA y Total
    y_position -= 30
    c.setFont("Helvetica-Bold", 10)
    c.drawString(450, y_position, "SUB-TOTAL")
    c.drawString(580, y_position, f"$ {subtotal}")
    iva = subtotal * 0.16
    y_position -= 20
    c.drawString(450, y_position, "IVA (16%):")
    c.drawString(580, y_position, f"$ {iva:.2f}")
    y_position -= 20
    c.setFont("Helvetica-Bold", 11) 
    c.drawString(450, y_position, "TOTAL:")
    c.drawString(580, y_position, f"$ {subtotal + iva:.2f}")

    c.setFont("Helvetica-Bold", 11)
    c.drawString(30, y_position - 30, "NOTA:")
    c.setFont("Helvetica", 9)
    c.drawString(70, y_position - 30, "El precio esta sujeto a cambios si durante el procedimiento del mismo hay que hacer cambios de algun componente o carga de gas.")
    c.setFont("Helvetica-Bold", 9) 
    c.drawString(30, y_position - 60, f"Estamos ubicados en la {data['direccion_empresa'].capitalize()}")
    c.showPage()
    c.save()

# Streamlit UI
st.title('Generador de Presupuestos')

# Datos por defecto de la empresa
data = {
    'empresa': 'REFRIMAT05',
    'direccion_empresa': 'AV LEONARDO RUIZ PINEDA EDIF BUCARE A PISO 4 APT 42 CONJUNTO RESIDENCIAL JARDIN BOTANICO CARACAS DISTRITO CAPITAL ZONA POTAL 1010',
    'telefono_empresa': '04125431092'
}

data['cliente'] = st.text_input("Nombre del Cliente")
data['telefono_cliente'] = st.text_input("Telefono del Cliente")

# Lista para mantener los servicios
if 'services' not in st.session_state:
    st.session_state['services'] = []

# Entradas para los servicios
with st.form("Service Form"):
    desc = st.text_input("Descripción del Servicio")
    qty = st.number_input("Cantidad", min_value=1, value=1)
    price = st.number_input("Precio Unitario", min_value=0.0, format="%.2f")
    add_service = st.form_submit_button("Agregar Servicio")

if add_service:
    st.session_state['services'].append({
        'description': desc,
        'quantity': qty,
        'unit_price': price
    })

# Mostrar los servicios actuales
if st.session_state['services']:
    st.write("Servicios Agregados:")
    for service in st.session_state['services']:
        st.write(f"{service['description']} - Cantidad: {service['quantity']}, Precio: ${service['unit_price']}")

# Botón para generar PDF
if st.button('Generar PDF'):
    create_pdf(data, st.session_state['services'])
    st.success("PDF generado con éxito! Encuentra tu archivo en el directorio del proyecto.")
    with open("presupuesto.pdf", "rb") as file:
        st.download_button(label="Descargar PDF", data=file, file_name="presupuesto.pdf", mime="application/pdf")
 
 # LISTO ERA UN ERROR DE TIPEO CORREMOS 

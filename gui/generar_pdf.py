import os
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from textwrap import wrap
import tempfile

def dibujar_cuadro_con_titulo(c, x, y, width, height, titulo, font="Helvetica-Bold", font_size=11, fill_color='#EEECE1', text_color=colors.black):
    
    # Dibujar el rectángulo
    c.setFillColor(fill_color)
    c.rect(x, y, width, height, fill=1, stroke=1)

    # Establecer las propiedades del texto
    c.setFont(font, font_size)
    c.setFillColor(text_color)

    # Dibujar el título
    text_y = y + (height / 2) - (font_size / 2)  # Ajuste para centrar el texto verticalmente
    c.drawString(x + 10, text_y, titulo)

def nueva_pagina(c, y_position, margen_inferior=100):
    if y_position <= margen_inferior:
        c.showPage()
        y_position = 750  # Reiniciar la posición para la nueva página
    return y_position

def escribir_parrafo(c, texto, x, y, ancho, font="Helvetica", font_size=12, linea_altura=15):
    c.setFont(font, font_size)

    # Dividir el texto en líneas para ajustarlo al ancho especificado
    lineas = wrap(texto, width=int(ancho / (font_size * 0.6)))  # Ajuste basado en el tamaño de la fuente
    for linea in lineas:
        c.drawString(x, y, linea)
        y -= linea_altura

    return y -25

def generar_pdf(codigo_hc):
    """Función para generar el PDF con la información del diagnóstico y otros detalles relevantes del paciente."""
    # Ruta para guardar el PDF en la carpeta de Descargas
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    pdf_filename = os.path.join(downloads_path, f"diagnostico_{codigo_hc}.pdf")

    try:
        # Crear un objeto canvas de ReportLab para el PDF
        c = canvas.Canvas(pdf_filename)

        # Crear una ruta para guardar el PDF en una carpeta temporal del sistema
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            pdf_filename = temp_file.name

        # Construir la ruta a la base de datos de forma relativa
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, '..', 'instance', 'CAP.db')
        
        if not os.path.exists(db_path):
            print("El archivo de la base de datos no existe en la ruta especificada.")
            return

        # Configurar el cursor para que devuelva filas como diccionarios
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        ############################################
        # Extraer información de la base de datos
        ############################################

        # Extraer información del paciente
        try:
            cursor.execute("SELECT * FROM pacientes WHERE codigo_hc=?", (codigo_hc,))
            paciente_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener el paciente: {str(e)}")
            paciente_data = {
                'documento': 'No disponible',
                'nombre': 'No disponible',
                'edad': 'No disponible',
                'fecha_nacimiento': 'No disponible',
                'id_escolaridad': 'No disponible',
                'profesion': 'No disponible',
                'telefono': 'No disponible',
                'celular': 'No disponible',
                'remision': 'No disponible'
            }

        # Extraer información del diagnóstico
        try:
            cursor.execute("SELECT * FROM diagnosticos WHERE codigo_hc=?", (codigo_hc,))
            diagnostico_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener el diagnóstico: {str(e)}")
            diagnostico_data = {
                'plan_tratamiento': 'No disponible',
                'fecha': 'No disponible',
                'conclusion': 'No disponible'
            }
        
        # Historia clínica
        # Extraer información de la historia clínica
        try:
            cursor.execute("SELECT * FROM historias_clinicas WHERE codigo_hc=?", (codigo_hc,))
            historias_clinicas_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener la historia clínica: {str(e)}")
            historias_clinicas_data = {
                'documento_paciente': 'No disponible',
                'motivo_consulta': 'No disponible',
                'estado_actual': 'No disponible',
                'antecedentes': 'No disponible',
                'historial_familiar': 'No disponible',
                'historial_personal': 'No disponible'
            }
        
        # Áreas
        try:
            cursor.execute("SELECT * FROM areas WHERE codigo_hc=?", (codigo_hc,))
            areas_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener las áreas: {str(e)}")
            areas_data = {
                'familiar': 'No disponible',
                'pareja': 'No disponible',
                'social': 'No disponible',
                'laboral': 'No disponible'
            }

        # Comentarios Clínicos
        try:
            cursor.execute("SELECT * FROM comentarios_clinicos WHERE codigo_hc=?", (codigo_hc,))
            comentarios_clinicos_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener los comentarios clínicos: {str(e)}")
            comentarios_clinicos_data = {
                'id_prueba': 'No disponible',
                'tipo_comentario': 'No disponible',
                'comentario': 'No disponible'
            }
        
        # Conversiones
        try:
            cursor.execute("SELECT * FROM conversiones WHERE codigo_hc=?", (codigo_hc,))
            conversiones_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener las conversiones: {str(e)}")
            conversiones_data = {
                'id_prueba': 'No disponible',
                'id_subprueba': 'No disponible',
                'suma_puntuacion': 0.0,
                'puntuacion_compuesta': 0.0,
                'memoria_trabajo': 0.0,
                'rango_percentil': 0.0,
                'intervalo_confianza': 0.0
            }
        
        # Diagnóstico hipotesis e hipotesis

        

        # Estado mental
        try:
            cursor.execute("SELECT * FROM estado_mental WHERE codigo_hc=?", (codigo_hc,))
            estado_mental_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener el estado mental: {str(e)}")
            estado_mental_data = {
                'atencion': 'No disponible',
                'memoria': 'No disponible',
                'lenguaje': 'No disponible',
                'pensamiento': 'No disponible',
                'introspeccion': 'No disponible'
            }

        # Evaluaciones neuropsicológicas
        try:
            cursor.execute("SELECT * FROM evaluaciones_neuropsicologicas WHERE codigo_hc=?", (codigo_hc,))
            evaluaciones_neuropsicologicas_data = cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error al obtener las evaluaciones neuropsicológicas: {str(e)}")
            evaluaciones_neuropsicologicas_data = {
                'id_prueba': 'No disponible',
                'id_subprueba': 'No disponible',
                'puntaje': 'No disponible',
                'media': 'No disponible',
                'desviacion_estandar': 'No disponible',
                'escalar': 'No disponible',
                'interpretacion': 'No disponible'
            }

        # Hipótesis
        
        #try:
         #   cursor.execute("SELECT * FROM hipotesis WHERE codigo_hc=?", (codigo_hc,))
          #  hipotesis_data = cursor.fetchone()
        #except sqlite3.Error as e:
         #   print(f"Error al obtener las hipótesis: {str(e)}")
          #  hipotesis_data = {
           #     'descripcion': 'No disponible'
            #}
        
        # Nivel escolaridad
        try:
            id_escolaridad = paciente_data['id_escolaridad']
            cursor.execute("SELECT descripcion FROM nivel_escolaridad WHERE id=?", (id_escolaridad,))
            nivel_escolaridad = cursor.fetchone()
            nivel_escolaridad = nivel_escolaridad['descripcion']
        except sqlite3.Error as e:
            print(f"Error al obtener el nivel de escolaridad: {str(e)}")
            nivel_escolaridad = {
                'descripcion': 'No disponible'
            }
        
        


        # Verificar si los datos del paciente y diagnóstico existen
        if not paciente_data or not diagnostico_data or not historias_clinicas_data:
            print("No se encontró información del paciente o del diagnóstico en la base de datos.")
            return
        


        ########################################
        # EMPIEZA EL PDF
        ########################################
        
        # Iniciar posición vertical para la escritura
        y_position = 750

        # Dibujar cabecera al principio del PDF
        c.setLineWidth(1)
        
        # Definir posiciones de los cuadros
        x_start = 50
        y_start = y_position

        # Primer cuadro vacío
        c.rect(x_start, y_start, 70, 50)

        # Segundo cuadro: Título
        c.rect(x_start + 70, y_start, 280, 50)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x_start + 70 + 140, y_start + 30, "HISTORIA CLÍNICA")
        c.drawCentredString(x_start + 70 + 140, y_start + 15, "ATENCIÓN NEUROPSICOLOGICA ADULTOS")

        # Tercer cuadro: Código
        c.rect(x_start + 350, y_start, 100, 50)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_start + 360, y_start + 35, "CÓDIGO:")
        c.setFont("Helvetica", 10)
        c.drawCentredString(x_start + 365, y_start + 20, str(paciente_data['codigo_hc']))

        # Cuarto cuadro: Fecha de versión
        c.rect(x_start + 450, y_start, 80, 50)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_start + 460, y_start + 35, "FECHA DE")
        c.drawString(x_start + 460, y_start + 25, "VERSIÓN:")
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.darkgray)
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        c.drawString(x_start + 460, y_start + 10, fecha_actual)
        c.setFillColor(colors.black)

        y_position -= 45

        # Dibujar cuadro para 'Datos Personales'
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "DATOS PERSONALES")
        y_position -= 25

        # Información del paciente
        c.setFont("Helvetica", 12)
        c.drawString(100, y_position, f"  Nombre del paciente: {paciente_data['nombre']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Edad: {paciente_data['edad']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Fecha de Nacimiento: {paciente_data['fecha_nacimiento']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Escolaridad: {nivel_escolaridad}")
        y_position -= 20
        c.drawString(100, y_position, f"  Profesión: {paciente_data['profesion']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Teléfono: {paciente_data['telefono']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Celular: {paciente_data['celular']}")
        y_position -= 20
        c.drawString(100, y_position, f"  Remisión: {paciente_data['remision']}")
        y_position -= 40

        # MOTIVO DE CONSULTA
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "MOTIVO DE CONSULTA")
        y_position -= 25
        altura_parrafo = len(wrap(historias_clinicas_data['motivo_consulta'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, historias_clinicas_data['motivo_consulta'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # ESTADO ACTUAL
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "ESTADO ACTUAL")
        y_position -= 25
        altura_parrafo = len(wrap(historias_clinicas_data['estado_actual'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, historias_clinicas_data['estado_actual'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # HISTORIA MÉDICA Y PSIQUIÁTRICA ANTERIOR
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "HISTORIA MÉDICA Y PSIQUIÁTRICA ANTERIOR")
        y_position -= 25
        altura_parrafo = len(wrap(historias_clinicas_data['antecedentes'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, historias_clinicas_data['antecedentes'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # ANTECEDENTES PSIQUIÁTRICOS FAMILIARES
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "ANTECEDENTES PSIQUIÁTRICOS FAMILIARES")
        y_position -= 25
        altura_parrafo = len(wrap(historias_clinicas_data['historial_familiar'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, historias_clinicas_data['historial_familiar'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # HISTORIA PERSONAL
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "HISTORIA PERSONAL")
        y_position -= 25
        p = "Situaciones significativas: (Comportamentales, emocionales y socioafectivos)"
        altura_parrafo = len(wrap(p + "\n" + historias_clinicas_data['historial_personal'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, p + "\n" + historias_clinicas_data['historial_personal'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # ESTADO MENTAL
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "ESTADO MENTAL")
        y_position -= 25
        altura_parrafo = len(wrap("Atención: " + estado_mental_data['atencion'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Atención: " + estado_mental_data['atencion'], 120, y_position, 480)

        altura_parrafo = len(wrap("Memoria: " + estado_mental_data['memoria'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Memoria: " + estado_mental_data['memoria'], 120, y_position, 480)

        altura_parrafo = len(wrap("Lenguaje: " + estado_mental_data['lenguaje'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Lenguaje: " + estado_mental_data['lenguaje'], 120, y_position, 480)

        altura_parrafo = len(wrap("Pensamiento: " + estado_mental_data['pensamiento'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Pensamiento: " + estado_mental_data['pensamiento'], 120, y_position, 480)

        altura_parrafo = len(wrap("Introspección: " + estado_mental_data['introspeccion'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Introspección: " + estado_mental_data['introspeccion'], 120, y_position, 480)

        y_position = nueva_pagina(c, y_position)

        # ÁREAS
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "ÁREAS")
        y_position -= 25
        altura_parrafo = len(wrap("Familiar: " + areas_data['familiar'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Familiar: " + areas_data['familiar'], 120, y_position, 480)

        altura_parrafo = len(wrap("Pareja: " + areas_data['pareja'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Pareja: " + areas_data['pareja'], 120, y_position, 480)

        altura_parrafo = len(wrap("Social: " + areas_data['social'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Social: " + areas_data['social'], 120, y_position, 480)

        altura_parrafo = len(wrap("Laboral: " + areas_data['laboral'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Laboral: " + areas_data['laboral'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)
        ###############################################





        ############################################
        # PRUEBAS
        ############################################

        # Consultas a la base de datos
        cursor.execute("""
            SELECT p.nombre as prueba, sp.nombre as subprueba, e.puntaje, e.media, e.desviacion_estandar, e.escalar, e.interpretacion
            FROM evaluaciones_neuropsicologicas e
            JOIN sub_pruebas sp ON e.id_subprueba = sp.id
            JOIN pruebas p ON e.id_prueba = p.id
            WHERE e.codigo_hc = ?
            ORDER BY e.id_prueba, e.id_subprueba
        """, (codigo_hc,))

        evaluaciones = cursor.fetchall()

        # Agrupar las evaluaciones por prueba
        evaluaciones_por_prueba = {}
        for evaluacion in evaluaciones:
            prueba = evaluacion['prueba']
            if prueba not in evaluaciones_por_prueba:
                evaluaciones_por_prueba[prueba] = []
            evaluaciones_por_prueba[prueba].append(evaluacion)
        
        y_position -= 30
        
        # EVALUACIÓN NEUROPSICOLÓGICA
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "EVALUACIÓN NEUROPSICOLÓGICA")
        y_position -= 25
        p = "(Los puntajes clasificados como Indicador clínico -I.C-. son clasificados como de alto riesgo.)"
        altura_parrafo = len(wrap(p, width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, p, 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # 1. ATENCIÓN Y CONCENTRACIÓN
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "ATENCIÓN Y CONCENTRACIÓN")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Atención y concentración']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(310, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 1
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            y_position -= 5

            # Dibujar tipo de comentario
            if tipo_comentario != 'Conclusión':
                #c.setFont("Helvetica-Bold", 12)
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                #c.drawString(100, y_position, f"{tipo_comentario}:")
                y_position += 10
                # Dibujar contenido del comentario
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position, ancho=400)
                y_position = nueva_pagina(c, y_position)
        
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']

            if tipo_comentario == 'Conclusión':
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                y_position += 10
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position, ancho=400)
                y_position = nueva_pagina(c, y_position)


        # 2. PROCESOS PERCEPTUALES
        y_position -= 20
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "PROCESOS PERCEPTUALES")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Procesos perceptuales']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(320, y_position, str(evaluacion['media']))
                c.drawString(370, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 2
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            # Dibujar tipo de comentario
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_position, f"{tipo_comentario}:")
            y_position -= 15
            
            # Dibujar contenido del comentario
            y_position = escribir_parrafo(c, comentario_texto, 120, y_position, ancho=400)
            y_position -= 5

            y_position = nueva_pagina(c, y_position)

        # 3. Funciones Neurocognitivas
        y_position -= 10
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "FUNCIONES NEUROCOGNITIVAS (GNOSIAS Y PRAXIAS)")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Funciones neurocognitivas']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(310, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 3
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            # Dibujar tipo de comentario
            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, y_position, f"{tipo_comentario}:")
            y_position -= 15
            
            # Dibujar contenido del comentario
            y_position = escribir_parrafo(c, comentario_texto, 120, y_position, ancho=400)
            y_position -= 5

            y_position = nueva_pagina(c, y_position)

        # 4. Lenguaje
        y_position = nueva_pagina(c, y_position-100)
        y_position -= 10
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "LENGUAJE")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Lenguaje']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(310, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 4
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            y_position -= 5

            # Dibujar tipo de comentario
            if tipo_comentario != 'Conclusión':
                #c.setFont("Helvetica-Bold", 12)
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                #c.drawString(100, y_position, f"{tipo_comentario}:")
                y_position += 10
                # Dibujar contenido del comentario
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+15, ancho=450)
                y_position = nueva_pagina(c, y_position)
        
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            y_position = nueva_pagina(c, y_position)

            if tipo_comentario == 'Conclusión':
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                y_position += 10
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+15, ancho=500)
                y_position = nueva_pagina(c, y_position)


        # 5. Procesos de memoria
        y_position = nueva_pagina(c, y_position-30)
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "PROCESOS DE MEMORIA")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Procesos de memoria']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(310, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 5
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            y_position -= 5

            # Dibujar tipo de comentario
            if tipo_comentario != 'Conclusión':
                #c.setFont("Helvetica-Bold", 12)
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                #c.drawString(100, y_position, f"{tipo_comentario}:")
                y_position += 10
                # Dibujar contenido del comentario
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+15, ancho=450)
                y_position = nueva_pagina(c, y_position)
        
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            y_position = nueva_pagina(c, y_position)

            if tipo_comentario == 'Conclusión':
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                y_position += 10
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+15, ancho=500)
                y_position = nueva_pagina(c, y_position)



        # 6. Función ejecutiva
        y_position = nueva_pagina(c, y_position)
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "FUNCIÓN EJECUTIVA")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Función ejecutiva']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=150)
                c.drawString(250, y_position, str(evaluacion['puntaje']))
                c.drawString(310, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        # Consultar comentarios clínicos específicos para 'Atención y concentración'
        cursor.execute("""
            SELECT tipo_comentario, comentario
            FROM comentarios_clinicos
            WHERE codigo_hc = ? AND id_prueba = 6
        """, (codigo_hc,))

        comentarios = cursor.fetchall()

        # Dibujar los comentarios clínicos al final de la prueba
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']
            
            y_position -= 5

            # Dibujar tipo de comentario
            if tipo_comentario != 'Conclusión':
                #c.setFont("Helvetica-Bold", 12)
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                #c.drawString(100, y_position, f"{tipo_comentario}:")
                y_position += 10
                # Dibujar contenido del comentario
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+10, ancho=400)
                y_position = nueva_pagina(c, y_position+14)
        
        for comentario in comentarios:
            tipo_comentario = comentario['tipo_comentario']
            comentario_texto = comentario['comentario']

            if tipo_comentario == 'Conclusión':
                y_position = escribir_parrafo(c, tipo_comentario, 100, y_position, ancho=400, font="Helvetica-Bold")
                y_position += 5
                y_position = escribir_parrafo(c, comentario_texto, 120, y_position+15, ancho=400)
                y_position = nueva_pagina(c, y_position)

        # 7. Capacidad intelectual
        y_position = nueva_pagina(c, y_position)
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "CAPACIDAD INTELECTUAL")
        evaluaciones_atencion_conc = evaluaciones_por_prueba['Capacidad intelectual']
        y_position -= 25
        y_position = nueva_pagina(c, y_position)

        # Dibujar encabezados de la tabla
        c.setFont("Helvetica-Bold", 12)
        encabezados = ["Subprueba", "Puntaje", "Media", "D.S.", "Interpretación"]
        x_positions = [100, 250, 310, 365, 400]
        for i, encabezado in enumerate(encabezados):
            c.drawString(x_positions[i], y_position, encabezado)
        y_position -= 20
        y_position = nueva_pagina(c, y_position)

        # Dibujar datos de cada subprueba
        c.setFont("Helvetica", 10)
        for evaluacion in evaluaciones_atencion_conc:

            if evaluacion['subprueba'] != 'Otra Prueba':
                escribir_parrafo(c, evaluacion['subprueba'], 100, y_position, ancho=120)
                c.drawString(280, y_position, str(evaluacion['puntaje']))
                c.drawString(320, y_position, str(evaluacion['media']))
                c.drawString(365, y_position, str(evaluacion['desviacion_estandar']))
                y_position = escribir_parrafo(c, evaluacion['interpretacion'], 400, y_position, ancho=150)
                y_position -= 10
                c.line(100, y_position + 30, 550, y_position + 30)

            y_position = nueva_pagina(c, y_position)

        
        ####################################################
        # Información de las hipótesis diagnósticas
        y_position -= 20
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "HIPÓTESIS DIAGNÓSTICA")
        y_position -= 25

        c.setFont("Helvetica", 12)
        cursor.execute("""
            SELECT h.descripcion 
            FROM diagnostico_hipotesis dh
            JOIN hipotesis h ON dh.codigo_hipotesis = h.id
            WHERE dh.codigo_hc=?
        """, (codigo_hc,))
        hipotesis = cursor.fetchall()
        
        for hip in hipotesis:
            altura_parrafo = len(wrap(hip['descripcion'], width=80)) * 15
            y_position = nueva_pagina(c, y_position, altura_parrafo)
            y_position = escribir_parrafo(c, hip['descripcion'], 120, y_position, 480)
        

        # Plan de tratamiento
        dibujar_cuadro_con_titulo(c, 100, y_position, 400, 20, "PLAN DE TRATAMIENTO")
        y_position -= 25
        altura_parrafo = len(wrap(diagnostico_data['plan_tratamiento'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, diagnostico_data['plan_tratamiento'], 120, y_position, 480)
        y_position = nueva_pagina(c, y_position)

        # CONCLUSIONES
        altura_parrafo = len(wrap("Conclusión: " + diagnostico_data['conclusion'], width=80)) * 15
        y_position = nueva_pagina(c, y_position, altura_parrafo)
        y_position = escribir_parrafo(c, "Conclusión: " + diagnostico_data['conclusion'], 120, y_position, 480)

        # ESPACIO PARA LA FIRMA DEL PRÁCTICANTE Y EL PROFESIONAL (EN 2 COLUMNAS)
        y_position -= 70
        c.setLineWidth(1)
        c.line(100, y_position, 300, y_position)
        c.line(350, y_position, 550, y_position)
        c.setFont("Helvetica", 10)
        c.drawString(100, y_position - 10, "Practicante")
        c.drawString(100, y_position - 20, "Reg.")

        c.drawString(350, y_position - 10, "Profesional")
        c.drawString(350, y_position - 20, "Reg.")

        # Guardar el PDF
        c.save()

        # Confirmación de generación de PDF
        print(f"PDF generado exitosamente: {pdf_filename}")

    except sqlite3.Error as e:
        print(f"Error en la base de datos: {str(e)}")
    except Exception as e:
        print(f"Ha ocurrido un error: {str(e)}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # Aquí puedes cambiar el código del paciente para probar con diferentes datos
    codigo_hc = 1
    generar_pdf(codigo_hc)

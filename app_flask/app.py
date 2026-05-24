from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from functools import wraps
import uuid
import re
import json
import random
from datetime import datetime
import google.generativeai as genai

# ======================================
# CONEXIÓN A MYSQL
# ======================================
app = Flask(__name__)
app.secret_key = "hackathon"


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",  # Tu contraseña de MySQL
    database="asistente_nutrimental"
)

cursor = db.cursor(dictionary=True)


# API
genai.configure(api_key="AIzaSyDuawCa_l_w4HTa46qBtXqwAGM_vWpRZxY")

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    generation_config={
        "temperature": 0.2
    }
)


SYSTEM_PROMPT = """
Eres un asistente nutrimental especializado
en diabetes tipo 2.

Tu tarea es analizar alimentos y responder
SIEMPRE exclusivamente en JSON válido.

NUNCA respondas texto fuera del JSON.
NUNCA uses markdown.
NUNCA uses bloques ```.

REGLAS GENERALES
==============================
Debes clasificar la entrada del usuario en UNA de estas categorías:

1. ALIMENTO VÁLIDO
- comida consumible
- bebidas consumibles
- alimentos comunes
- ingredientes normales

2. ALIMENTO PELIGROSO O TÓXICO
- comida podrida
- comida contaminada
- sustancias tóxicas
- cosas no aptas para consumo
- productos peligrosos
- químicos
- venenos
- sustancias dañinas

3. SOLICITUD NO RELACIONADA
- preguntas generales
- conversaciones normales
- temas no alimenticios
- mensajes aleatorios
- salud mental
- suicidio
- autolesión
- violencia
- cualquier cosa que no sea comida

RESPUESTAS
==============================

Si es ALIMENTO VÁLIDO, 

{
  "accion": "registrar",
  "alimento": "",
  "carbohidratos": 0,
  "proteinas": 0,
  "grasas": 0,
  "sodio": 0,
  "riesgo": "Bajo",
  "recomendacion": ""
}

La recomendación debe:
- explicar si es recomendable o no
- mencionar índice glucémico
- sugerir porciones adecuadas
- usar tono profesional y claro
la informacion nutrimental tiene que venir de fuentes comprobables como


https://www.sistemadigitaldealimentos.org/, si no estas seguro, has una estimación 
Si es ALIMENTO PELIGROSO O TÓXICO:

y menciona en la recomendacion que es una estimación

{
  "accion": "rechazar",
  "alimento": "",
  "carbohidratos": 0,
  "proteinas": 0,
  "grasas": 0,
  "sodio": 0,
  "riesgo": "No valido",
  "recomendacion": "Ese alimento o sustancia puede representar un riesgo para la salud y no es seguro consumirlo. Consulta a un profesional de salud si hubo ingestión."
}


Si es SOLICITUD NO RELACIONADA:

{
  "accion": "rechazar",
  "alimento": "",
  "carbohidratos": 0,
  "proteinas": 0,
  "grasas": 0,
  "sodio": 0,
  "riesgo": "No valido",
  "recomendacion": "Solo puedo analizar alimentos y bebidas relacionadas con nutrición y diabetes."
}

==============================
VALORES VÁLIDOS PARA RIESGO
==============================

La sección riesgo SOLO puede contener:
- "Alto"
- "Medio"
- "Bajo"
- "No valido"

==============================
IMPORTANTE
==============================

SIEMPRE devuelve JSON válido.
NO agregues explicaciones fuera del JSON.
""" 

# ======================================
# DECORADOR PARA SESIÓN
# ======================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


# ======================================
# BASE DE DATOS DE RESPUESTAS PREDEFINIDAS
# ======================================


def analizar_alimento(nombre_alimento, perfil_paciente):
    """
    Analiza un alimento usando respuestas predefinidas o respuestas largas de LLM simuladas
    """
    prompt = SYSTEM_PROMPT + nombre_alimento
    response = model.generate_content(prompt)

    try: 
        text = response.text.strip()

        text = text.replace(
            "```json", ""
        ).replace("```", "")

        respuesta = json.loads(text)

                
        return {
            "success": True,
            "analysis": {
                "carbohidratos": respuesta["carbohidratos"],
                "proteinas": respuesta["proteinas"],
                "grasas": respuesta["grasas"],
                "sodio": respuesta["sodio"],
                "riesgo": respuesta["riesgo"],
                "recomendacion": respuesta["recomendacion"]
            }
        }
    except Exception as e: 
        return {
            "success": False,
            "message": f"Error al procesar la respuesta de IA"
        }



# ======================================
# LOGIN
# ======================================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        query = """
        SELECT id, email, paciente_id 
        FROM usuarios 
        WHERE email = %s AND password = %s
        """
        
        cursor.execute(query, (email, password))
        user = cursor.fetchone()
        
        if user:
            session["user_id"] = user["id"]
            session["paciente_id"] = user["paciente_id"]
            
            if not user["paciente_id"]:
                return redirect("/profile")
            else:
                return redirect("/dashboard")
        
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        </head>
        <body>
            <script>
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "Correo o contraseña incorrectos",
                    confirmButtonText: "Intentar de nuevo"
                }).then(function() {
                    window.location.href = "/";
                });
            </script>
        </body>
        </html>
        '''
    
    return render_template("login.html")


# ======================================
# REGISTRO
# ======================================

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    
    # Validar contraseña mínima
    if len(password) < 8:
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        </head>
        <body>
            <script>
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "La contraseña debe tener al menos 8 caracteres",
                    confirmButtonText: "Corregir"
                }).then(function() {
                    window.location.href = "/";
                });
            </script>
        </body>
        </html>
        '''
    
    # Verificar si el email ya existe
    check_query = "SELECT id FROM usuarios WHERE email = %s"
    cursor.execute(check_query, (email,))
    
    if cursor.fetchone():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        </head>
        <body>
            <script>
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "Ese correo ya está registrado",
                    confirmButtonText: "Corregir"
                }).then(function() {
                    window.location.href = "/";
                });
            </script>
        </body>
        </html>
        '''
    
    # Insertar nuevo usuario
    insert_query = """
    INSERT INTO usuarios (email, password, paciente_id)
    VALUES (%s, %s, %s)
    """
    
    cursor.execute(insert_query, (email, password, None))
    db.commit()
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    </head>
    <body>
        <script>
            Swal.fire({
                icon: "success",
                title: "¡Registro exitoso!",
                text: "Cuenta creada correctamente. Ahora inicia sesión.",
                confirmButtonText: "Ir a iniciar sesión"
            }).then(function() {
                window.location.href = "/";
            });
        </script>
    </body>
    </html>
    '''


# ======================================
# PERFIL
# ======================================

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    profile_data = None
    
    # Obtener perfil existente
    if session.get("paciente_id"):
        query = """
        SELECT id, nombre, edad, peso_kg, altura_cm, notas
        FROM pacientes 
        WHERE id = %s
        """
        cursor.execute(query, (session["paciente_id"],))
        profile_data = cursor.fetchone()
    
    return render_template("profile.html", profile=profile_data)


# ======================================
# API PARA GUARDAR PERFIL
# ======================================

@app.route("/api/profile", methods=["POST"])
@login_required
def api_save_profile():
    data = request.get_json()
    
    nombre = data.get("nombre")
    edad = data.get("edad")
    peso_kg = data.get("peso_kg")
    altura_cm = data.get("altura_cm")
    notas = data.get("notas")
    
    # Validaciones
    errores = []
    
    if not nombre:
        errores.append("El nombre del paciente no puede estar vacío.")
    elif len(nombre) > 100:
        errores.append("El nombre del paciente no debe superar 100 caracteres.")
    elif not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
        errores.append("El nombre solo debe contener letras y espacios.")
    
    if not edad:
        errores.append("La edad no puede estar vacía.")
    else:
        try:
            edad_num = int(edad)
            if edad_num <= 0:
                errores.append("La edad debe ser mayor que cero.")
            elif edad_num > 130:
                errores.append("La edad no debe ser mayor a 130.")
        except ValueError:
            errores.append("La edad debe ser un número entero.")
    
    if not peso_kg:
        errores.append("El peso no puede estar vacío.")
    else:
        try:
            peso_num = float(peso_kg)
            if peso_num <= 0:
                errores.append("El peso debe ser mayor que cero.")
            elif peso_num > 999.99:
                errores.append("El peso no debe superar 999.99 kg.")
        except ValueError:
            errores.append("El peso debe ser un número válido.")
    
    if not altura_cm:
        errores.append("La altura no puede estar vacía.")
    else:
        try:
            altura_num = int(altura_cm)
            if altura_num <= 0:
                errores.append("La altura debe ser mayor que cero.")
            elif altura_num > 300:
                errores.append("La altura no debe ser mayor a 300 cm.")
        except ValueError:
            errores.append("La altura debe ser un número entero.")
    
    if notas and len(notas) > 500:
        errores.append("Las notas no deben superar 500 caracteres.")
    
    if errores:
        return jsonify({
            "success": False,
            "errors": errores
        }), 400
    
    try:
        if not session.get("paciente_id"):
            paciente_id = str(uuid.uuid4())[:8]
            
            insert_query = """
            INSERT INTO pacientes (id, nombre, edad, peso_kg, altura_cm, notas)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (paciente_id, nombre, edad, peso_kg, altura_cm, notas))
            
            update_query = "UPDATE usuarios SET paciente_id = %s WHERE id = %s"
            cursor.execute(update_query, (paciente_id, session["user_id"]))
            
            db.commit()
            session["paciente_id"] = paciente_id
            
            return jsonify({
                "success": True,
                "message": "Perfil creado exitosamente"
            })
        else:
            update_query = """
            UPDATE pacientes 
            SET nombre = %s, edad = %s, peso_kg = %s, altura_cm = %s, notas = %s
            WHERE id = %s
            """
            
            cursor.execute(update_query, (nombre, edad, peso_kg, altura_cm, notas, session["paciente_id"]))
            db.commit()
            
            return jsonify({
                "success": True,
                "message": "Perfil actualizado exitosamente"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error al guardar: {str(e)}"
        }), 500


# ======================================
# DASHBOARD
# ======================================

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    if not session.get("paciente_id"):
        return redirect("/profile")
    
    # Obtener perfil del paciente
    profile_query = """
    SELECT nombre, edad, peso_kg, altura_cm, notas
    FROM pacientes 
    WHERE id = %s
    """
    cursor.execute(profile_query, (session["paciente_id"],))
    profile = cursor.fetchone()
    
    # Obtener historial de consumos
    history_query = """
    SELECT 
        c.fecha,
        a.nombre,
        a.carbohidratos_porcion,
        a.proteinas_porcion,
        a.grasas_porcion,
        a.sodio_porcion,
        c.nivel_riesgo,
        c.fecha as fecha_consumo
    FROM consumos c
    JOIN alimentos a ON c.alimento_id = a.id
    WHERE c.paciente_id = %s
    ORDER BY c.fecha DESC, c.id DESC
    LIMIT 20
    """
    cursor.execute(history_query, (session["paciente_id"],))
    history = cursor.fetchall()
    
    history_json = json.dumps(history, default=str)

    return render_template(
        "dashboard.html",
        profile=profile,
        history=history,
        history_json=json.dumps(history, default=str)
    )

# ======================================
# API PARA ANALIZAR ALIMENTO 
# ======================================

@app.route("/api/analyze", methods=["POST"])
@login_required
def analyze_food():
    if not session.get("paciente_id"):
        return jsonify({
            "success": False,
            "message": "Perfil no encontrado"
        }), 400
    
    data = request.get_json()
    food = data.get("food")
    
    if not food:
        return jsonify({
            "success": False,
            "message": "El alimento es obligatorio"
        }), 400
    
    if len(food) > 100:
        return jsonify({
            "success": False,
            "message": "El nombre del alimento no debe superar 100 caracteres"
        }), 400
    
    # Obtener perfil del paciente
    profile_query = """
    SELECT nombre, edad, peso_kg, altura_cm, notas
    FROM pacientes 
    WHERE id = %s
    """
    cursor.execute(profile_query, (session["paciente_id"],))
    profile = cursor.fetchone()
    
    if not profile:
        return jsonify({
            "success": False,
            "message": "Perfil del paciente no encontrado"
        }), 404
    
    # Analizar con Gemini
    resultado = analizar_alimento(food, profile)
    
    if not resultado["success"]:
        return jsonify({
            "success": False,
            "message": resultado.get("message", "Error al analizar el alimento")
        }), 500
    
    analysis = resultado["analysis"]

    # Validar riesgo
    riesgo_valido = [
    "Alto",
    "Medio",
    "Bajo",
    "No valido"
    ]

    riesgo = analysis.get("riesgo", "").strip()

    if analysis.get("riesgo") == "No valido":

        return jsonify({
            "success": False,
            "message": analysis.get(
                "recomendacion",
                "Solicitud inválida"
            )
        }), 400
    
    try:
        # Insertar alimento en la BD
        food_query = """
        INSERT INTO alimentos (nombre, carbohidratos_porcion, proteinas_porcion, grasas_porcion, sodio_porcion)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(food_query, (
            food,
            analysis.get("carbohidratos", 0),
            analysis.get("proteinas", 0),
            analysis.get("grasas", 0),
            analysis.get("sodio", 0)
        ))
        db.commit()
        alimento_id = cursor.lastrowid
        
        # Insertar consumo
        consumo_query = """
        INSERT INTO consumos (paciente_id, alimento_id, fecha, porciones, nivel_riesgo)
        VALUES (%s, %s, CURDATE(), %s, %s)
        """
        
        cursor.execute(consumo_query, (
            session["paciente_id"],
            alimento_id,
            1,
            analysis.get("riesgo", "Medio")
        ))
        db.commit()
        
        print(f"✅ Alimento guardado exitosamente: {food}")
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "message": "Alimento analizado y guardado correctamente"
        })
        
    except Exception as e:
        print(f"❌ Error al guardar en BD: {e}")
        return jsonify({
            "success": False,
            "message": f"Error al guardar en BD: {str(e)}"
        }), 500


# ======================================
# LOGOUT
# ======================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ======================================
# RUN
# ======================================

if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    app.run(debug=True)
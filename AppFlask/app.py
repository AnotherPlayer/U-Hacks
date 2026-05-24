from flask import Flask, render_template, request, redirect, session, jsonify
import mysql.connector
from functools import wraps
import uuid
import re
import json
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "hackathon"

# ======================================
# CONFIGURACIÓN DE GEMINI
# ======================================

genai.configure(
    api_key="TU_API_KEY_AQUI"  # CAMBIA ESTO POR TU API KEY REAL DE GOOGLE AI STUDIO
)

model = genai.GenerativeModel("gemini-1.5-flash")

# ======================================
# CONEXIÓN A MYSQL
# ======================================

db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",  # Tu contraseña de MySQL
    database="asistente_nutrimental"
)

cursor = db.cursor(dictionary=True)


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
# PERFIL - CON VALIDACIONES
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
    
    # ======================================
    # VALIDACIONES
    # ======================================
    errores = []
    
    # Validar nombre
    if not nombre:
        errores.append("El nombre del paciente no puede estar vacío.")
    elif len(nombre) > 100:
        errores.append("El nombre del paciente no debe superar 100 caracteres.")
    elif not re.match(r'^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
        errores.append("El nombre solo debe contener letras y espacios.")
    
    # Validar edad
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
    
    # Validar peso
    if not peso_kg:
        errores.append("El peso no puede estar vacío.")
    else:
        try:
            peso_num = float(peso_kg)
            if peso_num <= 0:
                errores.append("El peso debe ser mayor que cero.")
            elif peso_num > 999.99:
                errores.append("El peso no debe superar 999.99 kg.")
            elif not re.match(r'^\d{1,3}(\.\d{1,2})?$', peso_kg):
                errores.append("El peso debe tener máximo 3 dígitos enteros y 2 decimales.")
        except ValueError:
            errores.append("El peso debe ser un número válido.")
    
    # Validar altura
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
    
    # Validar notas
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
    
    return render_template("dashboard.html", profile=profile, history=history, analysis=None, alimento_analizado=None)


# ======================================
# API PARA ANALIZAR ALIMENTO CON GEMINI
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
    
    # Contexto del paciente para Gemini
    patient_context = f"""
    Paciente con DIABETES TIPO 2:
    - Nombre: {profile['nombre']}
    - Edad: {profile['edad']} años
    - Peso: {profile['peso_kg']} kg
    - Altura: {profile['altura_cm']} cm
    - Notas adicionales: {profile['notas'] if profile['notas'] else 'Ninguna'}
    """
    
    prompt = f"""
    {patient_context}
    
    Eres un asistente nutrimental especializado en diabetes tipo 2.
    
    Analiza el siguiente alimento pensando en una porción estándar (1 taza o 100g).
    
    Responde SOLAMENTE con un objeto JSON válido, sin texto adicional, sin markdown.
    
    Formato requerido:
    {{
        "carbohidratos": 0,
        "proteinas": 0,
        "grasas": 0,
        "sodio": 0,
        "riesgo": "Alto/Medio/Bajo",
        "recomendacion": "Recomendación breve para el paciente con diabetes tipo 2"
    }}
    
    Alimento a analizar: {food}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Limpiar markdown
        text = text.replace("```json", "").replace("```", "").strip()
        
        analysis = json.loads(text)
        
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
        
        return jsonify({
            "success": True,
            "analysis": analysis,
            "message": "Alimento analizado y guardado correctamente"
        })
        
    except json.JSONDecodeError as e:
        return jsonify({
            "success": False,
            "message": f"Error al procesar la respuesta de IA: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error al analizar: {str(e)}"
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
    app.run(debug=True)
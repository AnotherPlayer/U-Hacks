#!/bin/bash

# Script de configuración local para MediByte
# Instalación directa de dependencias encontradas en el código

set -e

echo "🚀 Iniciando configuración de MediByte..."
echo ""

# 1. Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi
echo "✓ Python detectado"
echo ""

# 2. Crear entorno virtual
echo "✅ Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate
echo "✓ Entorno virtual activado"
echo ""

# 3. Actualizar pip
echo "✅ Actualizando pip..."
pip install --upgrade pip
echo ""

# 4. Instalar librerías de Python encontradas en el código
echo "✅ Instalando librerías necesarias..."
pip install flask==2.3.0
pip install mysql-connector-python==8.2.0
pip install google-generativeai==0.3.0
pip install python-dotenv==1.0.0
echo "✓ Todas las librerías instaladas"
echo ""

# 5. Crear archivo .env
if [ ! -f ".env" ]; then
    echo "✅ Creando archivo .env..."
    cat > .env << 'EOF'
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=hackathon

# Base de datos MySQL
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=
DB_NAME=asistente_nutrimental

# API Google Generative AI
GOOGLE_API_KEY=AIzaSyDuawCa_l_w4HTa46qBtXqwAGM_vWpRZxY
EOF
    echo "✓ Archivo .env creado"
else
    echo "✓ Archivo .env ya existe"
fi
echo ""

echo "════════════════════════════════════════════════════════"
echo "✨ ¡Configuración completada!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Para ejecutar MediByte:"
echo "  1. Activa el entorno: source venv/bin/activate"
echo "  2. Ejecuta: python3 app_flask/app.py"
echo ""
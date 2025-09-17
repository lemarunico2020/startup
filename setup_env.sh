#!/bin/bash

echo "🚀 Configurando entorno virtual para Startup Equity Manager..."
echo "=============================================================="

# Verificar que Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    echo "Por favor instala Python 3.8+ desde python.org"
    exit 1
fi

echo "✅ Python detectado: $(python3 --version)"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv startup_env

if [ $? -ne 0 ]; then
    echo "❌ Error creando entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual creado: startup_env"

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source startup_env/bin/activate

# Actualizar pip
echo "📈 Actualizando pip..."
python -m pip install --upgrade pip

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo "✅ Dependencias instaladas correctamente"

# Verificar instalación de Streamlit
if ! command -v streamlit &> /dev/null; then
    echo "❌ Error: Streamlit no se instaló correctamente"
    exit 1
fi

echo "✅ Streamlit instalado correctamente"

echo ""
echo "🎉 ¡Entorno virtual configurado exitosamente!"
echo "============================================="
echo ""
echo "📋 Para USAR la aplicación:"
echo "1. source startup_env/bin/activate"
echo "2. streamlit run startup_equity_manager.py"
echo "3. deactivate (cuando termines)"
echo ""
echo "🚀 Para EJECUTAR AHORA:"
echo "streamlit run startup_equity_manager.py"
echo ""
echo "⚠️  IMPORTANTE: El entorno ya está activado para esta sesión"
echo "   En futuras sesiones necesitarás activarlo manualmente"
echo ""

# Preguntar si quiere ejecutar ahora
read -p "¿Quieres ejecutar la aplicación ahora? (y/n): " ejecutar
if [[ $ejecutar == "y" || $ejecutar == "Y" ]]; then
    echo "🚀 Ejecutando Startup Equity Manager..."
    streamlit run startup_equity_manager.py
else
    echo "📋 Para ejecutar después: streamlit run startup_equity_manager.py"
fi

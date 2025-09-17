@echo off
echo 🚀 Configurando entorno virtual para Startup Equity Manager...
echo ================================================================

REM Verificar que Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    echo Por favor instala Python 3.8+ desde python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
python --version

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv startup_env

if errorlevel 1 (
    echo ❌ Error creando entorno virtual
    pause
    exit /b 1
)

echo ✅ Entorno virtual creado: startup_env

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call startup_env\Scripts\activate.bat

REM Actualizar pip
echo 📈 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)

echo ✅ Dependencias instaladas correctamente

REM Verificar instalación de Streamlit
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Streamlit no se instaló correctamente
    pause
    exit /b 1
)

echo ✅ Streamlit instalado correctamente

echo.
echo 🎉 ¡Entorno virtual configurado exitosamente!
echo ================================================
echo.
echo 📋 Para USAR la aplicación:
echo 1. startup_env\Scripts\activate.bat
echo 2. streamlit run startup_equity_manager.py
echo 3. deactivate (cuando termines)
echo.
echo 🚀 Para EJECUTAR AHORA:
echo streamlit run startup_equity_manager.py
echo.
echo ⚠️  IMPORTANTE: El entorno ya está activado para esta sesión
echo    En futuras sesiones necesitarás activarlo manualmente
echo.

REM Preguntar si quiere ejecutar ahora
set /p ejecutar="¿Quieres ejecutar la aplicación ahora? (y/n): "
if /i "%ejecutar%"=="y" (
    echo 🚀 Ejecutando Startup Equity Manager...
    streamlit run startup_equity_manager.py
) else (
    echo 📋 Para ejecutar después: streamlit run startup_equity_manager.py
)

pause

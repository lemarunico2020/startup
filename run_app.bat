@echo off
echo 🚀 Ejecutando Startup Equity Manager...
echo ====================================

REM Verificar que existe el entorno virtual
if not exist "startup_env\Scripts\activate.bat" (
    echo ❌ Error: El entorno virtual no existe
    echo 📋 Ejecuta primero: setup_env.bat
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call startup_env\Scripts\activate.bat

REM Verificar que Streamlit está disponible
streamlit --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Streamlit no está disponible en el entorno
    echo 📋 Ejecuta: setup_env.bat para reinstalar
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo ✅ Entorno activado
echo 🚀 Iniciando aplicación...
echo.
echo 📍 La aplicación se abrirá en: http://localhost:8501
echo 🛑 Para detener: Ctrl+C en esta ventana
echo.

streamlit run startup_equity_manager.py

echo.
echo 👋 Aplicación cerrada
echo 🔄 Desactivando entorno virtual...
deactivate

pause

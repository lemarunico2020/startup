# 🚀 INSTRUCCIONES RÁPIDAS - Startup Equity Manager

## 📋 Para empezar AHORA (2 opciones):

### 🐍 OPCIÓN 1: CON ENTORNO VIRTUAL (RECOMENDADO)
**1️⃣ Configuración automática:**
```bash
# Doble clic en:
setup_env.bat
```

**2️⃣ Ejecutar aplicación:**
```bash
# Doble clic en:
run_app.bat
```

**Para sesiones futuras:** Solo usa `run_app.bat`

---

### ⚡ OPCIÓN 2: INSTALACIÓN DIRECTA (RÁPIDA)
**1️⃣ Instalar dependencias:**
```bash
# Doble clic en:
install.bat
```

**2️⃣ Ejecutar aplicación:**
```bash
streamlit run startup_equity_manager.py
```

### 3️⃣ PROBAR CON DATOS DE EJEMPLO
- Ve a la pestaña "Export/Import" 
- Importa el archivo: `ejemplo_startup.json`
- ¡Ya tienes una startup completa para probar!

---

## 🎯 QUÉ HACE LA APLICACIÓN:

✅ **Gestiona socios**: Agrega cada uno con roles, dedicación, equity  
✅ **Tipos de acciones**: Ordinarias, Preferenciales, Stock Options  
✅ **Configuración vesting**: Períodos, cliff, cronogramas  
✅ **Análisis visual**: Gráficos de distribución y alertas  
✅ **Simulador dilución**: Ve efectos de nuevas emisiones  
✅ **Genera prompt Claude**: Consulta personalizada con toda tu info  

---

## 🤖 USAR CON CLAUDE:

1. **Completa tu información** en la app
2. **Ve a pestaña "Prompt Claude"**  
3. **Configura áreas de enfoque** (vesting, pacto socios, etc.)
4. **Genera prompt automático**
5. **Copia y pega** en nueva conversación con Claude
6. **Recibe recomendaciones específicas** para Colombia

---

## 📁 ARCHIVOS INCLUIDOS:

- `startup_equity_manager.py` - Aplicación principal
- `requirements.txt` - Dependencias  
- `setup_env.bat` - Configurar entorno virtual
- `run_app.bat` - Ejecutar con entorno virtual
- `install.bat` - Instalador directo
- `ejemplo_startup.json` - Datos de prueba
- `README_ENV.md` - Guía entorno virtual detallada

---

## ⚡ INICIO SÚPER RÁPIDO:

### 🐍 Con entorno virtual (MEJOR):
```cmd
# Una sola vez:
setup_env.bat

# Siempre:
run_app.bat
```

### 📦 Sin entorno virtual:
```cmd
pip install streamlit pandas plotly
streamlit run startup_equity_manager.py
```

¡Listo! La app se abre en tu navegador automáticamente.

---

## 🚨 SI TIENES PROBLEMAS:

1. **Python no instalado**: Descarga desde python.org
2. **Error de pip**: Reinstala Python con "Add to PATH" 
3. **App no abre**: Verifica que dice "Running on http://localhost:8501"
4. **Problemas entorno virtual**: Lee `README_ENV.md` para guía detallada
5. **Dudas**: El archivo ejemplo_startup.json tiene datos completos para probar

---

## 🎯 DIFERENCIAS ENTRE OPCIONES:

### 🐍 Entorno Virtual:
✅ Aislamiento de dependencias  
✅ No afecta otros proyectos Python  
✅ Fácil de limpiar/eliminar  
✅ Reproducible en otras máquinas  
⚠️ Requiere activar entorno cada vez  

### 📦 Instalación Directa:
✅ Más rápida para empezar  
✅ No necesita activar entorno  
⚠️ Puede generar conflictos con otros proyectos  
⚠️ Instala paquetes globalmente  

---

**🎉 ¡Ya estás listo para gestionar tu startup como un pro!**

**🔗 Para guía completa del entorno virtual:** Lee `README_ENV.md`

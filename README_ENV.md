# 🐍 INSTALACIÓN CON ENTORNO VIRTUAL DE PYTHON

## 🎯 Instalación Profesional (Recomendada)

### 📋 OPCIÓN 1: Con `venv` (Python estándar)

#### 1️⃣ Crear el entorno virtual
```bash
# En la carpeta del proyecto
cd D:\ClaudeAI_File

# Crear entorno virtual
python -m venv startup_env

# Activar entorno (Windows)
startup_env\Scripts\activate

# Activar entorno (Mac/Linux)
source startup_env/bin/activate
```

#### 2️⃣ Instalar dependencias
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación
pip list
```

#### 3️⃣ Ejecutar la aplicación
```bash
# Con el entorno activado
streamlit run startup_equity_manager.py
```

#### 4️⃣ Desactivar cuando termines
```bash
deactivate
```

---

### 📋 OPCIÓN 2: Con `conda` (Si tienes Anaconda/Miniconda)

#### 1️⃣ Crear entorno con conda
```bash
# Crear entorno con Python 3.9+
conda create -n startup_env python=3.9

# Activar entorno
conda activate startup_env
```

#### 2️⃣ Instalar dependencias
```bash
# Instalar con conda (recomendado)
conda install streamlit pandas plotly

# O usar pip si prefieres
pip install -r requirements.txt
```

#### 3️⃣ Ejecutar aplicación
```bash
streamlit run startup_equity_manager.py
```

#### 4️⃣ Desactivar
```bash
conda deactivate
```

---

### 📋 OPCIÓN 3: Con `pipenv` (Avanzado)

#### 1️⃣ Instalar pipenv (si no lo tienes)
```bash
pip install pipenv
```

#### 2️⃣ Crear Pipfile y entorno
```bash
cd D:\ClaudeAI_File
pipenv install streamlit pandas plotly
```

#### 3️⃣ Ejecutar en el entorno
```bash
pipenv run streamlit run startup_equity_manager.py
```

---

## 🚀 SCRIPTS AUTOMATIZADOS

### Para Windows (.bat)
```batch
@echo off
echo 🚀 Configurando entorno virtual para Startup Equity Manager...

REM Crear entorno virtual
python -m venv startup_env

REM Activar entorno
call startup_env\Scripts\activate.bat

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar dependencias
pip install -r requirements.txt

echo ✅ Entorno configurado exitosamente!
echo 📋 Para usar la aplicación:
echo 1. startup_env\Scripts\activate.bat
echo 2. streamlit run startup_equity_manager.py
echo 3. deactivate (cuando termines)

pause
```

### Para Mac/Linux (.sh)
```bash
#!/bin/bash
echo "🚀 Configurando entorno virtual para Startup Equity Manager..."

# Crear entorno virtual
python3 -m venv startup_env

# Activar entorno
source startup_env/bin/activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

echo "✅ Entorno configurado exitosamente!"
echo "📋 Para usar la aplicación:"
echo "1. source startup_env/bin/activate"
echo "2. streamlit run startup_equity_manager.py"
echo "3. deactivate (cuando termines)"
```

---

## 📁 ESTRUCTURA RECOMENDADA DEL PROYECTO

```
D:\ClaudeAI_File\
├── startup_env/              # Entorno virtual (se crea automáticamente)
├── startup_equity_manager.py # Aplicación principal
├── requirements.txt          # Dependencias
├── ejemplo_startup.json      # Datos de ejemplo
├── setup_env.bat            # Script de configuración Windows
├── setup_env.sh             # Script de configuración Mac/Linux
├── INSTRUCCIONES.md          # Guía de uso
└── README_ENV.md            # Este archivo
```

---

## 🔧 COMANDOS ÚTILES

### Gestión del entorno
```bash
# Ver paquetes instalados
pip list

# Generar requirements.txt actualizado
pip freeze > requirements.txt

# Instalar paquete específico
pip install nombre_paquete

# Desinstalar paquete
pip uninstall nombre_paquete

# Ver información del entorno
pip show streamlit
```

### Troubleshooting común
```bash
# Si pip no está actualizado
python -m pip install --upgrade pip

# Si hay conflictos de dependencias
pip install --force-reinstall streamlit pandas plotly

# Limpiar cache de pip
pip cache purge

# Reinstalar todo desde cero
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## ⚡ INICIO RÁPIDO CON ENTORNO VIRTUAL

### Método más rápido:
1. **Abre terminal** en `D:\ClaudeAI_File`
2. **Ejecuta**:
   ```bash
   python -m venv startup_env
   startup_env\Scripts\activate
   pip install streamlit pandas plotly
   streamlit run startup_equity_manager.py
   ```
3. **¡Listo!** La app se abre en tu navegador

### Para próximas veces:
```bash
# Solo necesitas activar y ejecutar
cd D:\ClaudeAI_File
startup_env\Scripts\activate
streamlit run startup_equity_manager.py
```

---

## 🎯 VENTAJAS DEL ENTORNO VIRTUAL

✅ **Aislamiento**: No afecta otros proyectos Python  
✅ **Reproducibilidad**: Mismas versiones en cualquier máquina  
✅ **Limpieza**: Fácil eliminar sin afectar sistema  
✅ **Colaboración**: Otros desarrolladores usan mismo entorno  
✅ **Profesional**: Estándar en desarrollo Python  

---

## 🚨 NOTAS IMPORTANTES

- **Siempre activa** el entorno antes de trabajar
- **Desactiva** cuando termines con `deactivate`
- **No subas** la carpeta `startup_env/` a Git
- **Usa** `requirements.txt` para compartir dependencias
- **Actualiza** pip regularmente: `python -m pip install --upgrade pip`

---

**🎉 ¡Ya tienes un entorno profesional para tu Startup Equity Manager!**

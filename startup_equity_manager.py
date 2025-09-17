import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Configuración de la página
st.set_page_config(
    page_title="🚀 Startup Equity Manager",
    page_icon="🚀",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #ff7f0e;
        border-bottom: 2px solid #ff7f0e;
        margin: 2rem 0 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .edit-mode {
        background-color: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'socios' not in st.session_state:
    st.session_state.socios = []
if 'company_info' not in st.session_state:
    st.session_state.company_info = {}
if 'editing_socio' not in st.session_state:
    st.session_state.editing_socio = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False

def mostrar_ayuda_concepto(concepto):
    """Mostrar ayuda detallada para conceptos"""
    ayudas = {
        "acciones_ordinarias": {
            "titulo": "🗳️ Acciones Ordinarias",
            "descripcion": "Son las acciones básicas de la empresa. Dan derecho a voto y participación en ganancias.",
            "ejemplo": "Si tienes 10% de acciones ordinarias = 10% de votos + 10% de dividendos",
            "recomendacion": "Típico para fundadores y empleados clave"
        },
        "acciones_preferenciales": {
            "titulo": "👑 Acciones Preferenciales",
            "descripcion": "Tienen privilegios especiales: cobran primero en liquidación y pueden tener dividendos preferenciales.",
            "ejemplo": "Los inversionistas suelen pedir estas para proteger su inversión",
            "recomendacion": "Úsalas para inversionistas externos, no para fundadores iniciales"
        },
        "stock_options": {
            "titulo": "📈 Stock Options (Opciones)",
            "descripcion": "Derecho a COMPRAR acciones a un precio fijo en el futuro. No son acciones reales todavía.",
            "ejemplo": "Opción de comprar 2% de acciones a $1000 cada una en 2 años",
            "recomendacion": "Perfectas para empleados - incentivo sin diluir inmediatamente"
        },
        "vesting": {
            "titulo": "⏳ Vesting (Adquisición Gradual)",
            "descripcion": "Las acciones se 'ganan' poco a poco con el tiempo. Si alguien se va temprano, pierde las no adquiridas.",
            "ejemplo": "4 años de vesting = 25% por año. Si se va en año 2, solo tiene 50%",
            "recomendacion": "ESENCIAL para todos - protege la empresa de salidas tempranas"
        },
        "cliff": {
            "titulo": "🚧 Cliff (Período mínimo)",
            "descripcion": "Tiempo mínimo antes de ganar cualquier acción. Si se va antes del cliff, no gana nada.",
            "ejemplo": "Cliff de 12 meses = si se va en mes 11, pierde todo",
            "recomendacion": "Típico: 12 meses para empleados, 6-12 meses para fundadores"
        }
    }

    if concepto in ayudas:
        ayuda = ayudas[concepto]
        with st.expander(f"❓ {ayuda['titulo']} - ¿Qué significa?"):
            st.markdown(f"**📖 Explicación:** {ayuda['descripcion']}")
            st.markdown(f"**💡 Ejemplo:** {ayuda['ejemplo']}")
            st.markdown(f"**✅ Recomendación:** {ayuda['recomendacion']}")

def mostrar_ayuda_antidilucion():
    """Mostrar ayuda detallada para protección antidilución"""
    with st.expander("❓ 🛡️ Protección Antidilución - ¿Qué significa?"):
        st.markdown("""
        **📖 ¿Qué es?**
        La protección antidilución es como un "seguro" que protege el valor de tu participación en la empresa cuando se venden nuevas acciones más baratas.

        **🏠 Analogía simple:**
        Imagina que compraste una casa por $100K cuando el barrio valía $1M. Si el barrio se devalúa a $500K, tu casa ahora vale $50K.
        La protección antidilución sería como recibir otra casa gratis para mantener tu inversión original de $100K.

        **💡 Ejemplo con números reales:**

        **Situación inicial:**
        - Tu participación: 10% de la empresa
        - Valoración empresa: $1,000,000
        - Tu inversión: $100,000

        **Problema - nueva ronda barata:**
        - La empresa necesita dinero urgente
        - Vende acciones valorando la empresa en solo $500,000
        - Tu 10% ahora vale: $50,000 (¡perdiste $50,000!)

        **Solución - con protección:**
        - Recibes acciones adicionales GRATIS
        - Mantienes el valor de tu inversión original
        - Tu participación puede aumentar al 15% para compensar
        """)

        st.warning("⚠️ **¿Cuándo pasa esto?** Cuando la empresa está en problemas, necesita dinero urgente, o hay una crisis económica que obliga a vender acciones más baratas.")

        st.info("💡 **¿Quién necesita protección?** Fundadores y empleados clave que han invertido dinero propio o han hecho aportes significativos.")

def mostrar_ayuda_prorata():
    """Mostrar ayuda detallada para derechos pro-rata"""
    with st.expander("❓ 🎯 Derechos Pro-rata (Derechos de Proporción) - ¿Qué significa?"):
        st.markdown("""
        **📖 ¿Qué son los Derechos Pro-rata?**
        Son el derecho que tienes como socio actual a **comprar tu parte proporcional** en futuras emisiones de acciones, manteniendo así tu porcentaje de participación en la empresa.

        **🍕 Analogía simple:**
        Imagina que tienes una pizza de 8 pedazos y tienes 2 pedazos (25%). Si hacen una pizza nueva de 8 pedazos más, tienes el DERECHO a comprar 2 pedazos de la nueva pizza para mantener tu 25% del total.

        **💡 Ejemplo con números reales:**

        **Situación inicial:**
        - Tienes: 20% de la empresa (200,000 acciones de 1,000,000 total)
        - La empresa vale: $1,000,000
        - Tu participación vale: $200,000

        **Nueva emisión de acciones:**
        - La empresa emite: 500,000 acciones nuevas
        - Precio por acción: $2 cada una
        - Total a recaudar: $1,000,000

        **❌ Sin derechos pro-rata:**
        - Total acciones después: 1,500,000
        - Tus acciones: 200,000 (sin cambio)
        - Tu nuevo porcentaje: 13.3% (¡perdiste 6.7%!)

        **✅ Con derechos pro-rata:**
        - Tienes derecho a comprar: 20% de las 500,000 nuevas = 100,000 acciones
        - Costo para ti: 100,000 × $2 = $200,000
        - Tus acciones después: 300,000
        - Tu porcentaje después: 20% (¡se mantiene!)
        """)

        st.warning("⚠️ **Importante**: Los derechos pro-rata NO te obligan a comprar, solo te dan la OPCIÓN de hacerlo antes que terceros.")

        st.info("💡 **¿Quién los necesita?** Todos los socios que quieren mantener su nivel de control e influencia en la empresa.")

        st.markdown("""
        **🔧 Tipos de derechos pro-rata:**
        - **🎯 Derechos Completos**: Puedes comprar tu proporción exacta en TODAS las futuras emisiones
        - **⚖️ Derechos Parciales**: Solo en ciertas emisiones (ej: no en rondas de empleados)
        - **👑 Derechos Preferenciales**: Tienes prioridad sobre otros para comprar
        - **🔄 Derechos de Sobresuscripción**: Si otros no compran, puedes comprar sus partes también
        """)

        st.success("✅ **Beneficio clave**: Evitas la dilución involuntaria y mantienes tu nivel de influencia en la empresa.")

def obtener_valores_sugeridos(categoria, dedicacion):
    """Sugerir valores típicos según categoría y dedicación"""
    sugerencias = {
        'Fundador Principal': {'ordinarias': (35, 51), 'cliff': 12, 'vesting': 4},
        'Co-fundador': {'ordinarias': (10, 25), 'cliff': 12, 'vesting': 4},
        'Early Employee': {'options': (1, 5), 'cliff': 12, 'vesting': 4},
        'Employee': {'options': (0.1, 2), 'cliff': 12, 'vesting': 4},
        'Advisor': {'options': (0.25, 1), 'cliff': 6, 'vesting': 2},
    }
    
    return sugerencias.get(categoria, {'ordinarias': (0, 5), 'cliff': 12, 'vesting': 4})

def formulario_socio(socio_data=None, modo="agregar"):
    """Formulario para agregar o editar socio"""
    es_edicion = modo == "editar" and socio_data is not None
    
    # Título del formulario
    if es_edicion:
        st.markdown(f"### ✏️ **Editando: {socio_data['nombre']}**")
        st.markdown('<div class="edit-mode">', unsafe_allow_html=True)
    else:
        st.markdown("### 1️⃣ **Información Básica**")
    
    # PASO 1: Información básica
    col_basic1, col_basic2 = st.columns(2)
    
    with col_basic1:
        nombre = st.text_input("👤 **Nombre completo**", 
                              value=socio_data.get('nombre', '') if es_edicion else '',
                              placeholder="Ej: María García")
        
    with col_basic2:
        categorias = ['Fundador Principal', 'Co-fundador', 'Early Employee', 'Employee', 'Advisor', 'Consultor']
        categoria_index = categorias.index(socio_data['categoria']) if es_edicion and socio_data['categoria'] in categorias else 0
        categoria = st.selectbox("🏷️ **¿Qué tipo de socio es?**", categorias,
                                index=categoria_index,
                                help="Esto determina rangos típicos de equity y configuración")
    
    col_basic3, col_basic4 = st.columns(2)
    
    with col_basic3:
        roles = ['CEO/Fundador Principal', 'Co-fundador', 'CTO', 'CMO', 'CFO',
                'VP Tecnología', 'VP Marketing', 'VP Ventas', 'VP Operaciones',
                'Director', 'Gerente', 'Empleado Senior', 'Empleado', 'Advisor', 'Consultor']
        rol_index = roles.index(socio_data['rol']) if es_edicion and socio_data['rol'] in roles else 0
        rol = st.selectbox("💼 **Rol en la empresa**", roles, index=rol_index)
        
    with col_basic4:
        dedicaciones = ['Tiempo Completo (100%)', 'Tiempo Parcial (75%)', 'Tiempo Parcial (50%)', 'Tiempo Parcial (25%)', 'Consultoría']
        dedicacion_index = dedicaciones.index(socio_data['dedicacion']) if es_edicion and socio_data['dedicacion'] in dedicaciones else 0
        dedicacion = st.selectbox("⏰ **Dedicación de tiempo**", dedicaciones,
                                 index=dedicacion_index,
                                 help="La dedicación afecta la cantidad de equity típica")
    
    # Obtener sugerencias basadas en categoría
    sugerencias = obtener_valores_sugeridos(categoria, dedicacion)
    
    st.markdown("---")
    
    # PASO 2: Asignación de Equity (simplificado y mejorado para Colombia)
    if not es_edicion:
        st.markdown("### 2️⃣ **Asignación de Equity** - ¡Lo más importante!")
        st.info("💡 **¿Necesitas ayuda?** Ve a la pestaña **'📚 Ayuda y Guías'** para ver todas las explicaciones detalladas.")
    else:
        st.markdown("### **Asignación de Equity**")

    # Selector del tipo de equity (simplificado)
    col_equity_main1, col_equity_main2 = st.columns([2, 1])

    with col_equity_main1:
        if categoria in ['Fundador Principal', 'Co-fundador']:
            # Para fundadores: principalmente acciones ordinarias
            sugerido_min, sugerido_max = sugerencias.get('ordinarias', (20, 51))
            valor_inicial = socio_data.get('acciones_ordinarias', float(sugerido_min)) if es_edicion else float(sugerido_min)
            acciones_ordinarias = st.slider(
                f"🗳️ **Acciones Ordinarias (%)** - Recomendado: {sugerido_min}-{sugerido_max}%",
                min_value=0.0, max_value=100.0, step=0.5,
                value=valor_inicial,
                help="Acciones con derecho a voto - típico para fundadores"
            )

            # Alternativamente pueden tener preferenciales
            valor_inicial_pref = socio_data.get('acciones_preferenciales', 0.0) if es_edicion else 0.0
            acciones_preferenciales = st.slider(
                "👑 **Acciones Preferenciales (%)** - Solo si hay inversores",
                min_value=0.0, max_value=50.0, step=0.5,
                value=valor_inicial_pref,
                help="Solo usar si hay rondas de inversión"
            )

            # Stock options/alternativas colombianas para fundadores (menor uso)
            stock_options = 0.0
            phantom_equity = 0.0
            profit_sharing = 0.0
            warrants = 0.0
            acciones_vesting = 0.0

        else:
            # Para empleados: primero acciones ordinarias básicas
            valor_inicial = socio_data.get('acciones_ordinarias', 0.0) if es_edicion else 0.0
            acciones_ordinarias = st.slider(
                "🗳️ **Acciones Ordinarias (%)** - Para empleados clave",
                min_value=0.0, max_value=20.0, step=0.1,
                value=valor_inicial,
                help="Solo para empleados muy importantes o con aporte económico"
            )

            acciones_preferenciales = 0.0  # Empleados no suelen tener preferenciales

            # ALTERNATIVAS COLOMBIANAS PARA EMPLEADOS
            st.markdown("**🇨🇴 Alternativas para SAS Colombia:**")

            # Phantom Equity
            valor_phantom = socio_data.get('phantom_equity', 0.0) if es_edicion else 0.0
            phantom_equity = st.slider(
                "👻 **Phantom Equity (%)** - ¡Recomendado para Colombia!",
                min_value=0.0, max_value=10.0, step=0.1,
                value=valor_phantom,
                help="Derecho a ganancias futuras sin acciones reales - Muy popular en Colombia"
            )

            # Profit Sharing
            valor_profit = socio_data.get('profit_sharing', 0.0) if es_edicion else 0.0
            profit_sharing = st.slider(
                "💰 **Profit Sharing (% utilidades anuales)** - Más simple",
                min_value=0.0, max_value=15.0, step=0.5,
                value=valor_profit,
                help="Porcentaje de utilidades anuales - Fácil de implementar"
            )

            # Warrants
            valor_warrants = socio_data.get('warrants', 0.0) if es_edicion else 0.0
            warrants = st.slider(
                "📜 **Warrants (%)** - Para eventos específicos",
                min_value=0.0, max_value=10.0, step=0.1,
                value=valor_warrants,
                help="Derecho a comprar acciones en eventos específicos (venta, inversión)"
            )

            # Acciones con Vesting
            valor_vesting_acc = socio_data.get('acciones_vesting', 0.0) if es_edicion else 0.0
            acciones_vesting = st.slider(
                "📈 **Acciones con Vesting (%)** - Entrega directa",
                min_value=0.0, max_value=10.0, step=0.1,
                value=valor_vesting_acc,
                help="Acciones reales que se liberan gradualmente"
            )

            # Stock Options tradicionales (menos usadas en Colombia)
            if st.checkbox("📈 **¿Incluir Stock Options tradicionales?**",
                          value=socio_data.get('incluir_stock_options', False) if es_edicion else False,
                          help="Poco usadas en Colombia, mejor usar alternativas de arriba"):
                valor_stock = socio_data.get('stock_options', 0.0) if es_edicion else 0.0
                stock_options = st.slider(
                    "📈 **Stock Options (%)**",
                    min_value=0.0, max_value=10.0, step=0.1,
                    value=valor_stock,
                    help="Derecho a comprar acciones - Poco común en SAS Colombia"
                )
            else:
                stock_options = 0.0

    with col_equity_main2:
        # Resumen y recomendaciones
        equity_total = acciones_ordinarias + acciones_preferenciales + stock_options + phantom_equity + acciones_vesting

        if categoria in ['Fundador Principal', 'Co-fundador']:
            st.markdown("**🎯 Para Fundadores:**")
            st.success("✅ Acciones Ordinarias son lo típico")
            if acciones_preferenciales > 0:
                st.info("ℹ️ Preferenciales solo si hay inversores")
        else:
            st.markdown("**🇨🇴 Para Empleados en Colombia:**")
            if phantom_equity > 0:
                st.success("✅ Phantom Equity es muy popular")
            if profit_sharing > 0:
                st.success("✅ Profit Sharing es simple")
            if acciones_ordinarias > 0:
                st.warning("⚠️ Acciones reales solo para empleados clave")

        st.metric("📊 Total Equity", f"{equity_total:.1f}%")

        # Mostrar número de acciones si está configurado (solo para equity real)
        equity_real = acciones_ordinarias + acciones_preferenciales + stock_options + acciones_vesting
        if st.session_state.company_info.get('acciones_a_emitir', 0) > 0 and equity_real > 0:
            acciones_a_emitir = st.session_state.company_info.get('acciones_a_emitir', 0)
            numero_acciones = int((equity_real / 100) * acciones_a_emitir)
            valor_por_accion = st.session_state.company_info.get('valor_por_accion', 1000)
            valor_total = numero_acciones * valor_por_accion

            st.metric("🔢 Acciones Reales", f"{numero_acciones:,}")
            st.metric("💰 Valor en Acciones", f"${valor_total:,}")

            if numero_acciones > 0:
                st.info(f"💡 {numero_acciones:,} acciones × ${valor_por_accion:,} = ${valor_total:,}")

        # Mostrar valor de alternativas colombianas
        if phantom_equity > 0 or profit_sharing > 0:
            st.markdown("**💰 Valor de Alternativas Colombianas:**")
            if phantom_equity > 0:
                st.info(f"👻 Phantom Equity: {phantom_equity:.1f}% (pago en eventos de liquidez)")
            if profit_sharing > 0:
                st.info(f"📊 Profit Sharing: {profit_sharing:.1f}% (pago anual en utilidades)")

        if equity_total > 15 and categoria not in ['Fundador Principal', 'Co-fundador']:
            st.warning(f"⚠️ {equity_total:.1f}% es alto para {categoria}")
        elif equity_total > 0:
            st.success(f"✅ {equity_total:.1f}% es apropiado")
    
    # SECCIONES AVANZADAS (Simplificadas)
    st.markdown("---")
    st.markdown("### 🛡️ **Protecciones Avanzadas** - Opcional")

    col_protecciones1, col_protecciones2 = st.columns(2)

    with col_protecciones1:
        # Protección Antidilución (simplificada)
        tiene_proteccion = st.toggle(
            "🛡️ **Protección Antidilución**",
            value=socio_data.get('proteccion_antidilucion', False) if es_edicion else False,
            help="Protege si venden acciones más baratas en el futuro"
        )

        if tiene_proteccion:
            if categoria in ['Fundador Principal', 'Co-fundador']:
                tipo_proteccion = "Full Ratchet (Máxima protección)"
                porcentaje_proteccion = 100
                umbral_activacion = 20.0
                duracion_proteccion = "3 años"
                st.success("✅ Configuración recomendada para fundadores aplicada")
            else:
                tipo_proteccion = "Weighted Average Broad (Protección balanceada)"
                porcentaje_proteccion = 100
                umbral_activacion = 25.0
                duracion_proteccion = "2 años"
                st.info("ℹ️ Configuración recomendada para empleados aplicada")
        else:
            tipo_proteccion = "Sin protección"
            porcentaje_proteccion = 0
            umbral_activacion = 0.0
            duracion_proteccion = "Sin protección"

    with col_protecciones2:
        # Derechos Pro-rata (simplificados)
        tiene_derechos_prorata = st.toggle(
            "🎯 **Derechos Pro-rata**",
            value=socio_data.get('derechos_prorata', False) if es_edicion else False,
            help="Derecho a mantener tu porcentaje en futuras emisiones"
        )

        if tiene_derechos_prorata:
            if categoria in ['Fundador Principal', 'Co-fundador']:
                tipo_derechos_prorata = "Derechos Completos (todas las emisiones)"
                participacion_minima = 1.0
                plazo_ejercicio = "30 días"
                transferibilidad_derechos = False
                exclusiones = ["Emisiones para empleados (stock options)"]
                st.success("✅ Configuración recomendada para fundadores aplicada")
            else:
                tipo_derechos_prorata = "Derechos Parciales (emisiones principales)"
                participacion_minima = 2.0
                plazo_ejercicio = "30 días"
                transferibilidad_derechos = False
                exclusiones = ["Emisiones para empleados (stock options)", "Conversión de deuda en acciones"]
                st.info("ℹ️ Configuración recomendada para empleados aplicada")
        else:
            tipo_derechos_prorata = "Sin derechos pro-rata"
            participacion_minima = 0.0
            plazo_ejercicio = "No aplica"
            transferibilidad_derechos = False
            exclusiones = []

    if tiene_proteccion or tiene_derechos_prorata:
        st.info("💡 **Detalles completos:** Ve a **'📚 Ayuda y Guías'** para entender cómo funcionan estas protecciones.")

    st.markdown("---")

    # PASO 3: Configuración de Vesting (simplificado)
    if not es_edicion:
        st.markdown("### 3️⃣ **Configuración de Vesting** - ¡Protección esencial!")
        
        mostrar_ayuda_concepto("vesting")
        mostrar_ayuda_concepto("cliff")
    else:
        st.markdown("### **Configuración de Vesting**")
    
    col_vest1, col_vest2 = st.columns(2)
    
    with col_vest1:
        vesting_options = [1, 2, 3, 4, 5]
        vesting_index = vesting_options.index(socio_data['vesting_total']) if es_edicion and socio_data['vesting_total'] in vesting_options else 3
        vesting_total = st.selectbox("📅 **Período de vesting**", vesting_options, 
                                    index=vesting_index, help="4 años es el estándar de la industria")
        st.info(f"✅ **{vesting_total} años** {'✨ Estándar!' if vesting_total == 4 else ''}")
        
        valor_inicial = socio_data.get('immediate_vest', 25.0 if categoria == 'Fundador Principal' else 0.0) if es_edicion else (25.0 if categoria == 'Fundador Principal' else 0.0)
        immediate_vest = st.number_input("💨 **Vesting inmediato (%)**", 
                                       min_value=0.0, max_value=50.0, 
                                       value=valor_inicial,
                                       help="% que se adquiere inmediatamente")
    
    with col_vest2:
        cliff_options = [0, 6, 12, 18, 24]
        cliff_index = cliff_options.index(socio_data['cliff_period']) if es_edicion and socio_data['cliff_period'] in cliff_options else 2
        cliff_period = st.selectbox("🚧 **Período de cliff (meses)**", cliff_options, 
                                   index=cliff_index, help="12 meses es típico")
        st.info(f"✅ **{cliff_period} meses** {'✨ Estándar!' if cliff_period == 12 else ''}")
        
        schedules = ['Mensual', 'Trimestral', 'Semestral', 'Anual']
        schedule_index = schedules.index(socio_data['vesting_schedule']) if es_edicion and socio_data['vesting_schedule'] in schedules else 0
        vesting_schedule = st.selectbox("📊 **Cronograma**", schedules,
                                       index=schedule_index, help="Mensual es lo más común")
    
    # PASO 4: Información adicional (opcional y colapsable)
    with st.expander("4️⃣ **Información Adicional** (Opcional)", expanded=False):
        col_extra1, col_extra2 = st.columns(2)
        
        with col_extra1:
            valor_fecha = datetime.strptime(socio_data['fecha_ingreso'], "%Y-%m-%d").date() if es_edicion else datetime.now().date()
            fecha_ingreso = st.date_input("📅 Fecha de ingreso", value=valor_fecha)
            
            valor_inicial = socio_data.get('salario', 0) if es_edicion else 0
            salario = st.number_input("💵 Salario mensual (COP)", min_value=0, step=500000, 
                                    value=valor_inicial, help="Opcional - para cálculos internos")
            
            valor_inicial = socio_data.get('aporte_inicial', 0) if es_edicion else 0
            aporte_inicial = st.number_input("💰 Aporte inicial (COP)", min_value=0, step=1000000,
                                           value=valor_inicial, help="Dinero o activos aportados")
            
        with col_extra2:
            acceleration = st.checkbox("⚡ Aceleración por salida",
                                     value=socio_data.get('acceleration', False) if es_edicion else False,
                                     help="Si se va la empresa, ¿acelerar vesting?")
            buyback_option = st.checkbox("🔄 Opción de recompra", 
                                       value=socio_data.get('buyback_option', True) if es_edicion else True,
                                       help="¿Puede la empresa recomprar acciones?")
            
        experiencia = st.text_area("🎓 Experiencia relevante", height=60,
                                 value=socio_data.get('experiencia', '') if es_edicion else '',
                                 placeholder="Ej: 5 años en marketing digital, ex-Google")
        responsabilidades = st.text_area("📋 Responsabilidades principales", height=60,
                                       value=socio_data.get('responsabilidades', '') if es_edicion else '',
                                       placeholder="Ej: Liderar equipo de desarrollo, arquitectura técnica")
        notas = st.text_area("📌 Notas adicionales", height=60,
                            value=socio_data.get('notas', '') if es_edicion else '',
                            placeholder="Cualquier información adicional relevante")
    
    # Validación y botones
    st.markdown("---")

    equity_total = acciones_ordinarias + acciones_preferenciales + stock_options + phantom_equity + acciones_vesting
    
    if equity_total > 0:
        col_summary1, col_summary2 = st.columns(2)
        with col_summary1:
            st.success(f"✅ **Equity total para {nombre or 'este socio'}**: {equity_total:.1f}%")
        with col_summary2:
            if equity_total > 15 and categoria not in ['Fundador Principal', 'Co-fundador']:
                st.warning(f"⚠️ {equity_total:.1f}% parece alto para {categoria}")
    
    if es_edicion:
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Retornar datos del formulario
    return {
        'nombre': nombre,
        'rol': rol,
        'categoria': categoria,
        'dedicacion': dedicacion,
        'fecha_ingreso': fecha_ingreso.strftime("%Y-%m-%d"),
        'salario': salario,
        'acciones_ordinarias': acciones_ordinarias,
        'acciones_preferenciales': acciones_preferenciales,
        'stock_options': stock_options,
        'phantom_equity': phantom_equity,
        'profit_sharing': profit_sharing,
        'warrants': warrants,
        'acciones_vesting': acciones_vesting,
        'vesting_total': vesting_total,
        'cliff_period': cliff_period,
        'vesting_schedule': vesting_schedule,
        'acceleration': acceleration,
        'immediate_vest': immediate_vest,
        'buyback_option': buyback_option,
        'aporte_inicial': aporte_inicial,
        'experiencia': experiencia,
        'responsabilidades': responsabilidades,
        'notas': notas,
        'equity_total': equity_total,
        'proteccion_antidilucion': tiene_proteccion,
        'tipo_proteccion': tipo_proteccion,
        'porcentaje_proteccion': porcentaje_proteccion,
        'umbral_activacion': umbral_activacion,
        'duracion_proteccion': duracion_proteccion,
        'derechos_prorata': tiene_derechos_prorata,
        'tipo_derechos_prorata': tipo_derechos_prorata,
        'participacion_minima_prorata': participacion_minima,
        'plazo_ejercicio_prorata': plazo_ejercicio,
        'transferibilidad_derechos': transferibilidad_derechos,
        'exclusiones_prorata': exclusiones if tiene_derechos_prorata else [],
        'warrants': warrants if 'warrants' in locals() else 0.0,
        'acciones_vesting': acciones_vesting if 'acciones_vesting' in locals() else 0.0,
        'incluir_stock_options': socio_data.get('incluir_stock_options', False) if es_edicion else False
    }

def main():
    # Disclaimer legal prominente
    st.markdown("""
    <div style="background-color: #fff3cd; border-left: 6px solid #856404; padding: 10px; margin-bottom: 20px;">
        <h4 style="color: #856404; margin: 0;">⚖️ Aviso Legal Importante</h4>
        <p style="margin: 5px 0 0 0; color: #856404;">
            <strong>Esta herramienta es únicamente para fines educativos y de planificación preliminar.</strong><br>
            No constituye asesoría legal, contable o fiscal. Siempre consulta con profesionales especializados
            en derecho societario y tributario antes de tomar decisiones sobre la estructura de equity de tu empresa.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-header">🚀 Startup Equity Manager</h1>', unsafe_allow_html=True)
    st.markdown("### Gestiona la estructura de acciones de tu startup de forma profesional")

    # Información del desarrollador
    with st.expander("ℹ️ Acerca de esta herramienta"):
        st.markdown("""
        **🎯 Propósito**: Herramienta educativa para planificación preliminar de equity en startups colombianas.

        **🇨🇴 Especialización**: Adaptada para Sociedades por Acciones Simplificadas (SAS) en Colombia,
        incluyendo alternativas de equity apropiadas para el contexto legal colombiano.

        **📊 Funcionalidades**:
        - Configuración de estructura accionaria SAS
        - Calculadora de acciones vs porcentajes
        - Alternativas colombianas (Phantom Equity, Profit Sharing, Warrants)
        - Simulador de dilución futura
        - Normatividad legal colombiana

        **⚠️ Limitaciones**: No almacena datos permanentemente. Exporta tu configuración antes de cerrar.

        ---
        💡 **¿Tienes sugerencias?** Esta herramienta está en desarrollo continuo para servir mejor a la comunidad startup colombiana.
        """)
    
    # Tabs principales
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Info Empresa",
        "👥 Gestión Socios",
        "📋 Tabla Resumen",
        "📈 Análisis Equity",
        "📚 Ayuda y Guías",
        "📋 Prompt Claude",
        "💾 Export/Import"
    ])
    
    with tab1:
        company_info_section()

    with tab2:
        socios_management_section()

    with tab3:
        tabla_resumen_section()

    with tab4:
        equity_analysis_section()

    with tab5:
        ayuda_y_guias_section()

    with tab6:
        claude_prompt_section()

    with tab7:
        export_import_section()

def ayuda_y_guias_section():
    st.markdown('<h2 class="section-header">📚 Ayuda y Guías Completas</h2>', unsafe_allow_html=True)

    # Selector de temas
    temas_disponibles = [
        "🎯 Conceptos Básicos de Equity",
        "🇨🇴 Alternativas para SAS Colombia",
        "🛡️ Protección Antidilución",
        "🎯 Derechos Pro-rata",
        "⏳ Vesting y Cliff",
        "📊 Guía de Distribución Típica",
        "⚖️ Aspectos Legales Colombia"
    ]

    tema_seleccionado = st.selectbox("🔍 **Selecciona el tema que quieres aprender:**", temas_disponibles)

    st.markdown("---")

    if tema_seleccionado == "🎯 Conceptos Básicos de Equity":
        mostrar_conceptos_basicos()
    elif tema_seleccionado == "🇨🇴 Alternativas para SAS Colombia":
        mostrar_alternativas_colombia()
    elif tema_seleccionado == "🛡️ Protección Antidilución":
        mostrar_guia_antidilucion()
    elif tema_seleccionado == "🎯 Derechos Pro-rata":
        mostrar_guia_prorata()
    elif tema_seleccionado == "⏳ Vesting y Cliff":
        mostrar_guia_vesting()
    elif tema_seleccionado == "📊 Guía de Distribución Típica":
        mostrar_guia_distribucion()
    elif tema_seleccionado == "⚖️ Aspectos Legales Colombia":
        mostrar_aspectos_legales()

def mostrar_conceptos_basicos():
    st.markdown("### 🎯 **Conceptos Básicos de Equity**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 🗳️ **Acciones Ordinarias**

        **¿Qué son?**
        - Las acciones básicas de la empresa
        - Dan derecho a voto en decisiones importantes
        - Participan en dividendos y ganancias

        **💡 Ejemplo:**
        Si tienes 10% en acciones ordinarias = 10% de votos + 10% de dividendos

        **✅ Recomendado para:**
        - Fundadores principales
        - Co-fundadores
        - Empleados clave con aporte económico
        """)

        st.markdown("""
        #### 👑 **Acciones Preferenciales**

        **¿Qué son?**
        - Acciones con privilegios especiales
        - Cobran primero en liquidación
        - Pueden tener dividendos preferenciales

        **💡 Ejemplo:**
        Si la empresa se vende, los preferenciales cobran antes que los ordinarios

        **✅ Recomendado para:**
        - Inversionistas externos
        - NO para fundadores iniciales
        """)

    with col2:
        st.markdown("""
        #### 📈 **Stock Options (Opciones)**

        **¿Qué son?**
        - Derecho a COMPRAR acciones a precio fijo
        - No son acciones reales todavía
        - Se ejercen en el futuro

        **💡 Ejemplo:**
        Opción de comprar 2% de acciones a $1000 cada una en 2 años

        **⚠️ En Colombia:**
        - Poco usadas en SAS
        - Ver alternativas colombianas en la siguiente sección
        """)

        st.markdown("""
        #### ⏳ **Vesting (Adquisición Gradual)**

        **¿Qué es?**
        - Las acciones se "ganan" poco a poco con el tiempo
        - Protege la empresa de salidas tempranas

        **💡 Ejemplo:**
        4 años de vesting = 25% por año. Si se va en año 2, solo tiene 50%

        **✅ Esencial para:**
        - TODOS los socios (incluso fundadores)
        """)

def mostrar_alternativas_colombia():
    st.markdown("### 🇨🇴 **Alternativas para SAS Colombia**")
    st.info("💡 **Las Stock Options tradicionales no se usan mucho en Colombia. Estas son las alternativas más utilizadas:**")

    # Phantom Equity
    with st.expander("👻 **PHANTOM EQUITY (Acciones Fantasma)** - La más popular"):
        st.markdown("""
        **📖 ¿Qué es?**
        El empleado recibe derecho a un porcentaje de las ganancias futuras de la empresa, pero SIN recibir acciones reales.

        **🏠 Analogía simple:**
        Es como tener derecho a las ganancias de una casa sin ser propietario. Si la casa se vende más cara, recibes tu parte en efectivo.

        **✅ Ventajas:**
        - Sin dilución para fundadores
        - Sin derechos de voto para empleados
        - Pago solo en efectivo
        - Más simple tributariamente

        **📊 Ejemplo práctico:**
        - Empleado tiene 2% en Phantom Equity
        - Empresa se valora inicialmente en $1M
        - 3 años después se vende en $5M
        - Empleado recibe: 2% × ($5M - $1M) = $80,000

        **⚙️ Configuración típica:**
        - Porcentaje: 0.5% - 5% para empleados clave
        - Vesting: 4 años, cliff 12 meses
        - Pago: Solo en eventos de liquidez (venta, fusión)

        **📋 Aspectos legales:**
        - Se documenta como contrato laboral especial
        - El empleado paga impuesto como ingreso laboral
        - La empresa puede deducir como gasto
        """)

    # Profit Sharing
    with st.expander("💰 **PROFIT SHARING (Participación en Ganancias)** - Más simple"):
        st.markdown("""
        **📖 ¿Qué es?**
        El empleado recibe un porcentaje fijo de las utilidades anuales de la empresa.

        **🏠 Analogía simple:**
        Es como ser socio en las ganancias anuales de un negocio, sin ser dueño del negocio.

        **✅ Ventajas:**
        - Muy simple de implementar
        - Pago anual en efectivo
        - Fácil de entender para empleados
        - Sin complicaciones de valoración

        **📊 Ejemplo práctico:**
        - Empleado tiene 5% de profit sharing
        - Empresa tuvo utilidades de $200,000 este año
        - Empleado recibe: 5% × $200,000 = $10,000

        **⚙️ Configuración típica:**
        - Porcentaje: 1% - 10% de utilidades anuales
        - Pool total: Máximo 20% de utilidades para empleados
        - Pago: Anual, después de cierre contable

        **📋 Aspectos legales:**
        - Se documenta en contrato laboral
        - Empleado paga impuesto como ingreso laboral
        - Empresa deduce como gasto operacional
        """)

    # Warrants
    with st.expander("📜 **WARRANTS (Opciones Contractuales)** - Para eventos específicos"):
        st.markdown("""
        **📖 ¿Qué es?**
        Contrato que da derecho a comprar acciones a precio fijo, pero solo se puede ejercer en eventos específicos.

        **🏠 Analogía simple:**
        Es como tener un cupón para comprar algo a precio fijo, pero solo puedes usarlo en fechas específicas.

        **✅ Ventajas:**
        - Control total sobre cuándo se ejercen
        - Precio fijo garantizado
        - Solo se activan en eventos importantes

        **📊 Ejemplo práctico:**
        - Empleado tiene warrant para comprar 3% a $100,000
        - Solo se puede ejercer si empresa se vende o recibe inversión >$2M
        - Si empresa se vende en $5M, empleado paga $100K y recibe 3% = $150K
        - Ganancia neta: $50,000

        **⚙️ Configuración típica:**
        - Precio: Valor actual de mercado o descuento 10-20%
        - Vigencia: 5-10 años
        - Eventos activadores: Venta, fusión, IPO, ronda >$X

        **📋 Aspectos legales:**
        - Contrato privado entre empresa y empleado
        - Ejercicio genera compra real de acciones
        - Tributación al momento del ejercicio
        """)

    # Acciones con Vesting
    with st.expander("📈 **ACCIONES CON VESTING** - Entrega directa"):
        st.markdown("""
        **📖 ¿Qué es?**
        Entrega directa de acciones reales, pero con restricciones que se liberan gradualmente en el tiempo.

        **🏠 Analogía simple:**
        Es como recibir las llaves de una casa, pero solo puedes usarlas completamente después de varios años.

        **✅ Ventajas:**
        - Empleado es accionista real desde el inicio
        - Derechos de voto (si se quiere)
        - Participación en dividendos inmediata

        **📊 Ejemplo práctico:**
        - Empleado recibe 2% de acciones con vesting 4 años
        - Año 1: Puede vender 0.5% (25%)
        - Año 2: Puede vender 1% (50%)
        - Año 4: Puede vender 2% (100%)

        **⚙️ Configuración típica:**
        - Vesting: 4 años, 25% anual
        - Cliff: 12 meses antes del primer vesting
        - Restricciones: Derecho de primera oferta para empresa

        **📋 Aspectos legales:**
        - Empleado debe pagar impuesto como ingreso laboral
        - Valor = valor de mercado de las acciones
        - Registro en Cámara de Comercio
        - Pacto de socios requerido
        """)

    # Comparación
    st.markdown("---")
    st.markdown("### 📊 **Comparación de Alternativas**")

    comparacion_data = {
        "Característica": [
            "Complejidad de implementación",
            "Tributación empleado",
            "Dilución fundadores",
            "Derechos de voto",
            "Pago empleado",
            "Ideal para"
        ],
        "Phantom Equity": [
            "Media",
            "Como ingreso laboral",
            "❌ No hay",
            "❌ No",
            "Solo en liquidez",
            "Empleados clave"
        ],
        "Profit Sharing": [
            "Baja",
            "Como ingreso laboral",
            "❌ No hay",
            "❌ No",
            "Anual en efectivo",
            "Todos los empleados"
        ],
        "Warrants": [
            "Alta",
            "Al ejercer opción",
            "✅ Sí, al ejercer",
            "✅ Sí, al ejercer",
            "Solo en eventos",
            "Empleados senior"
        ],
        "Acciones con Vesting": [
            "Alta",
            "Al recibir acciones",
            "✅ Sí, inmediata",
            "✅ Sí",
            "Dividendos + venta",
            "Co-fundadores"
        ]
    }

    df_comparacion = pd.DataFrame(comparacion_data)
    st.dataframe(df_comparacion, use_container_width=True, hide_index=True)

def mostrar_guia_antidilucion():
    st.markdown("### 🛡️ **Protección Antidilución - Guía Completa**")

    # Contenido detallado de antidilución
    mostrar_ayuda_antidilucion()

def mostrar_guia_prorata():
    st.markdown("### 🎯 **Derechos Pro-rata - Guía Completa**")

    # Contenido detallado de pro-rata
    mostrar_ayuda_prorata()

def mostrar_guia_vesting():
    st.markdown("### ⏳ **Vesting y Cliff - Guía Completa**")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### ⏳ **¿Qué es el Vesting?**

        El vesting es el proceso gradual por el cual un empleado "gana" o "adquiere" sus acciones o derechos de equity a lo largo del tiempo.

        **🏠 Analogía:**
        Es como un apartamento que compras a cuotas. Cada mes que pagas, eres dueño de una parte más grande.

        **📊 Ejemplo típico (4 años):**
        - Año 1: Adquiere 25% de sus acciones
        - Año 2: Adquiere 50% (25% adicional)
        - Año 3: Adquiere 75% (25% adicional)
        - Año 4: Adquiere 100% (25% final)

        **✅ Beneficios del Vesting:**
        - Retiene talento clave
        - Protege a la empresa de salidas tempranas
        - Asegura compromiso a largo plazo
        - Es estándar en la industria
        """)

    with col2:
        st.markdown("""
        #### 🚧 **¿Qué es el Cliff?**

        El cliff es un período mínimo que debe cumplir un empleado antes de adquirir CUALQUIER parte de sus acciones.

        **🏠 Analogía:**
        Es como un período de prueba. Si no completas el período mínimo, no recibes nada.

        **📊 Ejemplo típico (12 meses):**
        - Meses 1-11: No adquiere nada (0%)
        - Mes 12: Adquiere 25% de una vez
        - Luego continúa vesting normal mensual

        **✅ Beneficios del Cliff:**
        - Protege de contrataciones erróneas
        - Evita repartir equity a personas que se van rápido
        - Da tiempo para evaluar desempeño
        - Estándar: 12 meses para empleados
        """)

    st.markdown("""
    ### 📋 **Configuraciones Estándar**

    | Tipo de Socio | Vesting Total | Cliff | Cronograma | Justificación |
    |---------------|---------------|-------|------------|---------------|
    | **Fundador Principal** | 4 años | 6-12 meses | Mensual | Protege contra salidas tempranas |
    | **Co-fundador** | 4 años | 12 meses | Mensual | Estándar de industria |
    | **Empleado Clave** | 4 años | 12 meses | Mensual | Retención de talento |
    | **Empleado Regular** | 3-4 años | 12 meses | Mensual | Incentivo a largo plazo |
    | **Advisor** | 2 años | 6 meses | Trimestral | Compromiso menor |
    | **Consultor** | 1-2 años | 3 meses | Trimestral | Proyectos específicos |

    ### ⚠️ **Errores Comunes a Evitar**

    - **❌ No aplicar vesting a fundadores:** "Somos amigos, no necesitamos vesting"
    - **❌ Períodos muy largos:** Más de 4 años desmotiva
    - **❌ Sin cliff:** Personas que se van en 1 mes con equity
    - **❌ Vesting anual:** Muy poco granular, mejor mensual
    - **❌ No documentar:** Debe estar en contratos y pacto de socios
    """)

def mostrar_guia_distribucion():
    st.markdown("### 📊 **Guía de Distribución Típica de Equity**")

    # Distribución por etapa
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### 🚀 **Startup Temprana (Pre-Seed)**

        **Distribución sugerida:**
        - **Fundadores**: 60-80%
        - **Pool empleados**: 15-20%
        - **Advisors**: 2-5%
        - **Reserva futura**: 15-20%

        **👥 Por tipo de fundador:**
        - **CEO/Fundador Principal**: 30-51%
        - **CTO/Co-fundador**: 15-25%
        - **Otros co-fundadores**: 5-15% c/u

        **💼 Por tipo de empleado:**
        - **VP/Director**: 1-5%
        - **Empleado senior**: 0.5-2%
        - **Empleado regular**: 0.1-0.5%
        """)

    with col2:
        st.markdown("""
        #### 💰 **Después de Inversión (Seed/Serie A)**

        **Nueva distribución:**
        - **Fundadores**: 40-60% (diluidos)
        - **Empleados**: 10-20%
        - **Inversores**: 20-40%
        - **Pool empleados**: 10-15%

        **📈 Crecimiento del pool:**
        - **Pre-inversión**: 15-20%
        - **Post-Serie A**: 15-20% adicional
        - **Post-Serie B**: 10-15% adicional

        **⚖️ Balance recomendado:**
        - Fundadores nunca <30% (mantener control)
        - Pool empleados siempre >10% (atraer talento)
        - Inversores <50% (evitar control externo)
        """)

    st.markdown("""
    ### 🎯 **Factores para Distribuir Equity**

    #### **1. Contribución Inicial:**
    - **Idea original**: +5-10%
    - **Capital inicial**: +5-15%
    - **Desarrollo temprano**: +10-20%
    - **Red de contactos**: +2-5%

    #### **2. Rol y Responsabilidad:**
    - **CEO**: Mayor equity (liderazgo, responsabilidad final)
    - **CTO**: Segundo en equity (ejecución técnica)
    - **Otros fundadores**: Según aporte específico

    #### **3. Timing de Entrada:**
    - **Día 0**: Equity de fundador
    - **Primeros 6 meses**: Early employee (mayor equity)
    - **6-18 meses**: Employee regular
    - **18+ meses**: Equity menor

    #### **4. Dedicación:**
    - **Tiempo completo**: Equity completo
    - **Tiempo parcial 75%**: Reduce equity 15-25%
    - **Tiempo parcial 50%**: Reduce equity 30-50%
    - **Consultoría**: Equity mínimo

    ### ⚠️ **Errores Típicos a Evitar**

    - **❌ Dividir en partes iguales:** No todos contribuyen igual
    - **❌ Prometer equity sin documentar:** Conflictos futuros garantizados
    - **❌ No reservar para empleados:** Imposible escalar el equipo
    - **❌ Dar demasiado muy temprano:** No queda para crecimiento
    - **❌ No considerar dilución futura:** Planificar rondas de inversión
    """)

def mostrar_aspectos_legales():
    st.markdown("### ⚖️ **Aspectos Legales en Colombia**")

    st.warning("⚠️ **Importante:** Esta información es educativa. Siempre consulta con un abogado especializado en derecho societario.")

    # Normatividad SAS
    with st.expander("📜 **Normatividad Colombiana - SAS (Ley 1258 de 2008)**"):
        st.markdown("""
        ### **🏛️ Marco Legal de las SAS en Colombia**

        **📋 Ley 1258 de 2008 - Creación de SAS:**
        - Simplifica la creación y funcionamiento de sociedades
        - Flexibilidad en estructura de capital y administración
        - Responsabilidad limitada de los accionistas

        **🔄 Decretos Reglamentarios:**
        - **Decreto 2020 de 2009**: Reglamentación general
        - **Decreto 1966 de 2020**: Modernización de trámites
        - **Circular 100-000008 de 2020 (Supersociedades)**: Instrucciones operativas

        **⚖️ Artículos Clave para Equity:**

        **Art. 10 - Capital Autorizado:**
        - No requiere pagarse al momento de constitución
        - Límite máximo que puede emitir la sociedad
        - Reformas de aumento requieren modificación de estatutos

        **Art. 11 - Capital Suscrito:**
        - Parte del capital autorizado que se compromete a pagar
        - Mínimo 1/3 del capital suscrito debe pagarse al constituir
        - Plazo máximo 24 meses para pagar el resto

        **Art. 27 - Transferencia de Acciones:**
        - Derecho de preferencia en favor de accionistas existentes
        - Restricciones pueden establecerse en estatutos
        - Fundamental para estructuras de vesting

        **📚 Referencias Normativas:**
        - Código de Comercio (arts. 373 y ss.)
        - Estatuto Tributario (art. 103 - ingresos laborales)
        - Ley 1429 de 2010 (beneficios tributarios startups)
        """)

    # Requisitos SAS
    with st.expander("🏢 **Requisitos para SAS (Sociedad por Acciones Simplificada)**"):
        st.markdown("""
        **📋 Documentos requeridos:**

        1. **Estatutos sociales**
           - Objeto social amplio
           - Capital autorizado vs suscrito
           - Órganos de administración
           - Transferencia de acciones

        2. **Pacto de socios (recomendado)**
           - Vesting de acciones
           - Derechos de preferencia
           - Resolución de conflictos
           - Cláusulas de salida

        3. **Contratos laborales especiales**
           - Para phantom equity
           - Para profit sharing
           - Para warrants

        **📊 Capital mínimo:**
        - No hay capital mínimo
        - Recomendado: $10M-$100M COP

        **👥 Socios:**
        - Mínimo: 1 accionista
        - Máximo: 200 accionistas
        """)

    # Tributación
    with st.expander("💰 **Tributación de Equity en Colombia**"):
        st.markdown("""
        **👨‍💼 Para el empleado:**

        - **Phantom Equity**: Gravado como ingreso laboral al momento del pago
        - **Profit Sharing**: Gravado como ingreso laboral (anual)
        - **Acciones recibidas**: Gravado como ingreso laboral al momento de recibirlas
        - **Warrants ejercidos**: Gravado al momento del ejercicio

        **🏢 Para la empresa:**

        - **Phantom Equity**: Deducible como gasto al momento del pago
        - **Profit Sharing**: Deducible como gasto operacional
        - **Acciones entregadas**: Sin deducción (es dilución de capital)
        - **Warrants**: Depende de la estructura específica

        **📋 Obligaciones:**
        - Retención en la fuente
        - Declaración de renta
        - Medios y formas de pago (si supera límites)
        """)

    # Registro y formalización
    with st.expander("📝 **Registro y Formalización**"):
        st.markdown("""
        **🏛️ Cámara de Comercio:**

        - Registro inicial de la SAS
        - Reformas estatutarias (cambios de capital)
        - Libros de accionistas
        - Actas de asamblea

        **📋 Documentación requerida:**

        1. **Para nuevos accionistas:**
           - Reforma de estatutos (si aumenta capital)
           - Actualización libro de accionistas
           - Contratos de suscripción de acciones

        2. **Para esquemas de incentivos:**
           - Contratos laborales especiales
           - Actas de junta directiva aprobando esquemas
           - Políticas internas de equity

        **⏰ Plazos típicos:**
        - Registro SAS: 1-2 semanas
        - Reformas estatutarias: 1-2 semanas
        - Contratos: Inmediato
        """)

    # Recomendaciones prácticas
    st.markdown("""
    ### 💡 **Recomendaciones Prácticas**

    #### **1. Antes de implementar:**
    - ✅ Consultar con abogado societario
    - ✅ Consultar con contador especializado
    - ✅ Definir políticas internas claras
    - ✅ Calcular impacto tributario

    #### **2. Documentación esencial:**
    - ✅ Estatutos actualizados
    - ✅ Pacto de socios
    - ✅ Contratos de trabajo modificados
    - ✅ Política de equity por escrito

    #### **3. Para startups que buscan inversión:**
    - ✅ Data room organizado
    - ✅ Cap table (tabla de capitalización) actualizada
    - ✅ Todos los contratos firmados
    - ✅ Cumplimiento tributario al día

    #### **4. Costos estimados:**
    - Abogado societario: $2M-$5M COP
    - Registro Cámara Comercio: $200K-$500K COP
    - Contador especializado: $1M-$3M COP/año
    """)

def tabla_resumen_section():
    st.markdown('<h2 class="section-header">📋 Tabla Resumen de Socios</h2>', unsafe_allow_html=True)

    if not st.session_state.socios:
        st.warning("⚠️ No hay socios registrados. Ve a la pestaña 'Gestión Socios' para agregar.")
        return

    # Crear DataFrame a partir de los datos de socios
    df = pd.DataFrame(st.session_state.socios)

    # Calcular métricas de resumen
    total_socios = len(df)
    total_equity = (df['acciones_ordinarias'] + df['acciones_preferenciales'] + df['stock_options'] +
                   (df['phantom_equity'] if 'phantom_equity' in df.columns else 0) +
                   (df['acciones_vesting'] if 'acciones_vesting' in df.columns else 0)).sum()
    equity_disponible = 100 - total_equity
    total_aportes = df['aporte_inicial'].sum()
    total_salarios = df['salario'].sum()

    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("👥 Total Socios", total_socios)
    with col2:
        st.metric("📊 Equity Asignado", f"{total_equity:.1f}%")
    with col3:
        st.metric("🆓 Equity Disponible", f"{equity_disponible:.1f}%")
    with col4:
        st.metric("💰 Aportes Totales", f"${total_aportes:,}")
    with col5:
        st.metric("💵 Nómina Mensual", f"${total_salarios:,}")

    # Alertas de estado
    if total_equity > 100:
        st.error(f"❌ **SOBREASIGNACIÓN**: {total_equity:.1f}% excede el 100%")
    elif total_equity > 85:
        st.warning(f"⚠️ **ALTO PORCENTAJE**: {total_equity:.1f}% asignado. Considera reservar más para empleados e inversores.")
    elif equity_disponible > 40:
        st.info(f"ℹ️ **OPORTUNIDAD**: {equity_disponible:.1f}% disponible para crecimiento del equipo.")

    st.markdown("---")

    # Filtros y controles
    st.markdown("### 🔍 Filtros y Opciones")

    col_filter1, col_filter2, col_filter3 = st.columns(3)

    with col_filter1:
        categorias_disponibles = ['Todos'] + list(df['categoria'].unique())
        categoria_filtro = st.selectbox("🏷️ Filtrar por categoría", categorias_disponibles)

    with col_filter2:
        mostrar_proteccion = st.checkbox("🛡️ Mostrar protección antidilución", value=True)

    with col_filter3:
        formato_tabla = st.selectbox("📋 Formato de tabla", ["Completa", "Resumida", "Ejecutiva"])

    # Aplicar filtros
    df_filtrado = df.copy()
    if categoria_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]

    st.markdown("---")

    # Tabla principal según formato seleccionado
    if formato_tabla == "Ejecutiva":
        st.markdown("### 📊 Vista Ejecutiva")
        tabla_ejecutiva(df_filtrado, mostrar_proteccion)
    elif formato_tabla == "Resumida":
        st.markdown("### 📋 Vista Resumida")
        tabla_resumida(df_filtrado, mostrar_proteccion)
    else:
        st.markdown("### 📋 Vista Completa")
        tabla_completa(df_filtrado, mostrar_proteccion)

    # Análisis por categorías
    st.markdown("---")
    st.markdown("### 📊 Análisis por Categorías")

    analisis_categorias = df.groupby('categoria').agg({
        'acciones_ordinarias': 'sum',
        'acciones_preferenciales': 'sum',
        'stock_options': 'sum',
        'aporte_inicial': 'sum',
        'salario': 'sum',
        'nombre': 'count'
    }).round(2)

    analisis_categorias.columns = ['Ordinarias %', 'Preferenciales %', 'Options %', 'Aportes', 'Salarios', 'Cantidad']
    analisis_categorias['Total Equity %'] = (analisis_categorias['Ordinarias %'] +
                                          analisis_categorias['Preferenciales %'] +
                                          analisis_categorias['Options %'])

    # Formatear números para mejor visualización
    analisis_categorias['Aportes'] = analisis_categorias['Aportes'].apply(lambda x: f"${x:,.0f}")
    analisis_categorias['Salarios'] = analisis_categorias['Salarios'].apply(lambda x: f"${x:,.0f}")

    st.dataframe(analisis_categorias, use_container_width=True)

    # Resumen de protecciones antidilución
    if mostrar_proteccion and 'proteccion_antidilucion' in df.columns:
        st.markdown("### 🛡️ Resumen de Protecciones Antidilución")

        socios_con_proteccion = df[df.get('proteccion_antidilucion', False) == True]

        if not socios_con_proteccion.empty:
            col_prot1, col_prot2 = st.columns(2)

            with col_prot1:
                st.metric("👥 Socios Protegidos", len(socios_con_proteccion))
                equity_protegido = (socios_con_proteccion['acciones_ordinarias'] +
                                  socios_con_proteccion['acciones_preferenciales'] +
                                  socios_con_proteccion['stock_options']).sum()
                st.metric("📊 Equity Protegido", f"{equity_protegido:.1f}%")

            with col_prot2:
                tipos_proteccion = socios_con_proteccion['tipo_proteccion'].value_counts()
                st.markdown("**🔧 Tipos de protección:**")
                for tipo, cantidad in tipos_proteccion.items():
                    st.write(f"- {tipo}: {cantidad} socios")
        else:
            st.info("ℹ️ No hay socios con protección antidilución configurada.")

    # Resumen de derechos pro-rata
    if mostrar_proteccion and 'derechos_prorata' in df.columns:
        st.markdown("### 🎯 Resumen de Derechos Pro-rata")

        socios_con_prorata = df[df.get('derechos_prorata', False) == True]

        if not socios_con_prorata.empty:
            col_prorata1, col_prorata2 = st.columns(2)

            with col_prorata1:
                st.metric("👥 Socios con Derechos", len(socios_con_prorata))
                equity_con_derechos = (socios_con_prorata['acciones_ordinarias'] +
                                     socios_con_prorata['acciones_preferenciales'] +
                                     socios_con_prorata['stock_options']).sum()
                st.metric("📊 Equity con Derechos", f"{equity_con_derechos:.1f}%")

            with col_prorata2:
                tipos_derechos = socios_con_prorata['tipo_derechos_prorata'].value_counts()
                st.markdown("**🔧 Tipos de derechos:**")
                for tipo, cantidad in tipos_derechos.items():
                    st.write(f"- {tipo}: {cantidad} socios")
        else:
            st.info("ℹ️ No hay socios con derechos pro-rata configurados.")

def tabla_ejecutiva(df, mostrar_proteccion):
    """Vista ejecutiva con métricas clave"""
    tabla_exec = df[['nombre', 'categoria', 'rol']].copy()

    # Calcular equity total incluyendo alternativas colombianas
    tabla_exec['Equity Total %'] = (
        df['acciones_ordinarias'] +
        df['acciones_preferenciales'] +
        df['stock_options'] +
        (df['phantom_equity'] if 'phantom_equity' in df.columns else 0) +
        (df['acciones_vesting'] if 'acciones_vesting' in df.columns else 0)
    ).round(1)

    # Mostrar tipo principal de equity
    def determinar_tipo_equity(row):
        if row.get('acciones_ordinarias', 0) > 0:
            return "🗳️ Ordinarias"
        elif row.get('phantom_equity', 0) > 0:
            return "👻 Phantom"
        elif row.get('profit_sharing', 0) > 0:
            return "💰 Profit Share"
        elif row.get('warrants', 0) > 0:
            return "📜 Warrants"
        elif row.get('acciones_vesting', 0) > 0:
            return "📈 Acc. Vesting"
        elif row.get('stock_options', 0) > 0:
            return "📈 Options"
        else:
            return "❌ Ninguno"

    tabla_exec['Tipo Equity'] = df.apply(determinar_tipo_equity, axis=1)
    tabla_exec['Vesting'] = df['vesting_total'].astype(str) + 'a / ' + df['cliff_period'].astype(str) + 'm'
    tabla_exec['Aportes'] = df['aporte_inicial'].apply(lambda x: f"${x:,.0f}")

    if mostrar_proteccion and 'proteccion_antidilucion' in df.columns:
        tabla_exec['Protección Anti-D'] = df.get('proteccion_antidilucion', False).apply(
            lambda x: "🛡️ Sí" if x else "❌ No"
        )

    if mostrar_proteccion and 'derechos_prorata' in df.columns:
        tabla_exec['Derechos Pro-rata'] = df.get('derechos_prorata', False).apply(
            lambda x: "🎯 Sí" if x else "❌ No"
        )

    st.dataframe(tabla_exec, use_container_width=True, hide_index=True)

def tabla_resumida(df, mostrar_proteccion):
    """Vista resumida con información esencial"""
    tabla_res = df[['nombre', 'categoria', 'dedicacion']].copy()
    tabla_res['Ordinarias %'] = df['acciones_ordinarias'].round(1)
    tabla_res['Phantom %'] = df['phantom_equity'].round(1) if 'phantom_equity' in df.columns else 0
    tabla_res['Profit Share %'] = df['profit_sharing'].round(1) if 'profit_sharing' in df.columns else 0
    tabla_res['Total %'] = (df['acciones_ordinarias'] +
                           df['acciones_preferenciales'] +
                           df['stock_options'] +
                           (df['phantom_equity'] if 'phantom_equity' in df.columns else 0) +
                           (df['acciones_vesting'] if 'acciones_vesting' in df.columns else 0)).round(1)
    tabla_res['Salario'] = df['salario'].apply(lambda x: f"${x:,.0f}")

    if mostrar_proteccion and 'proteccion_antidilucion' in df.columns:
        tabla_res['Protección Anti-D'] = df.get('tipo_proteccion', 'Sin protección')

    if mostrar_proteccion and 'derechos_prorata' in df.columns:
        tabla_res['Derechos Pro-rata'] = df.get('tipo_derechos_prorata', 'Sin derechos')

    st.dataframe(tabla_res, use_container_width=True, hide_index=True)

def tabla_completa(df, mostrar_proteccion):
    """Vista completa con toda la información"""
    tabla_comp = df[['nombre', 'categoria', 'rol', 'dedicacion']].copy()
    tabla_comp['Ordinarias %'] = df['acciones_ordinarias'].round(1)
    tabla_comp['Preferenciales %'] = df['acciones_preferenciales'].round(1)
    tabla_comp['Options %'] = df['stock_options'].round(1)
    tabla_comp['Phantom %'] = df['phantom_equity'].round(1) if 'phantom_equity' in df.columns else 0
    tabla_comp['Profit Share %'] = df['profit_sharing'].round(1) if 'profit_sharing' in df.columns else 0
    tabla_comp['Warrants %'] = df['warrants'].round(1) if 'warrants' in df.columns else 0
    tabla_comp['Acc. Vesting %'] = df['acciones_vesting'].round(1) if 'acciones_vesting' in df.columns else 0
    tabla_comp['Total %'] = (df['acciones_ordinarias'] +
                            df['acciones_preferenciales'] +
                            df['stock_options'] +
                            (df['phantom_equity'] if 'phantom_equity' in df.columns else 0) +
                            (df['profit_sharing'] if 'profit_sharing' in df.columns else 0) +
                            (df['warrants'] if 'warrants' in df.columns else 0) +
                            (df['acciones_vesting'] if 'acciones_vesting' in df.columns else 0)).round(1)
    tabla_comp['Vesting'] = df['vesting_total'].astype(str) + 'a'
    tabla_comp['Cliff'] = df['cliff_period'].astype(str) + 'm'
    tabla_comp['Aportes'] = df['aporte_inicial'].apply(lambda x: f"${x:,.0f}")
    tabla_comp['Salario'] = df['salario'].apply(lambda x: f"${x:,.0f}")

    if mostrar_proteccion and 'proteccion_antidilucion' in df.columns:
        tabla_comp['Protección Anti-D'] = df.get('proteccion_antidilucion', False).apply(
            lambda x: "🛡️ Activa" if x else "❌ Inactiva"
        )
        tabla_comp['Tipo Protección'] = df.get('tipo_proteccion', 'N/A')

    if mostrar_proteccion and 'derechos_prorata' in df.columns:
        tabla_comp['Derechos Pro-rata'] = df.get('derechos_prorata', False).apply(
            lambda x: "🎯 Activos" if x else "❌ Inactivos"
        )
        tabla_comp['Tipo Pro-rata'] = df.get('tipo_derechos_prorata', 'N/A')

    st.dataframe(tabla_comp, use_container_width=True, hide_index=True)

def company_info_section():
    st.markdown('<h2 class="section-header">📊 Información de la Empresa</h2>', unsafe_allow_html=True)

    # Información básica
    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("🏢 Nombre de la empresa", value=st.session_state.company_info.get('name', ''))
        stage = st.selectbox("📈 Etapa actual", [
            'Idea', 'Prototipo', 'MVP', 'Primeros ingresos',
            'Crecimiento', 'Expansión', 'Pre-IPO'
        ], index=['Idea', 'Prototipo', 'MVP', 'Primeros ingresos', 'Crecimiento', 'Expansión', 'Pre-IPO'].index(
            st.session_state.company_info.get('stage', 'MVP')
        ))

        sector = st.text_input("🏭 Sector/Industria", value=st.session_state.company_info.get('sector', ''))

    with col2:
        country = st.selectbox("🌍 País", ['Colombia', 'México', 'Chile', 'Perú', 'Argentina', 'Brasil'],
                              index=['Colombia', 'México', 'Chile', 'Perú', 'Argentina', 'Brasil'].index(
                                  st.session_state.company_info.get('country', 'Colombia')
                              ))

        valuation_actual = st.number_input("📊 Valoración Actual (USD)", min_value=0,
                                         value=st.session_state.company_info.get('valuation', 0),
                                         step=50000)

        busca_inversion = st.checkbox("💸 ¿Busca inversión externa?",
                                    value=st.session_state.company_info.get('busca_inversion', False))

    # Nueva sección: Estructura Accionaria SAS Colombia
    if country == 'Colombia':
        st.markdown("---")
        st.markdown("### 🏛️ **Estructura Accionaria SAS Colombia**")
        st.info("💡 **Importante**: Define la estructura de acciones desde el inicio para evitar reformas costosas.")

        col_shares1, col_shares2 = st.columns(2)

        with col_shares1:
            st.markdown("#### 💰 **Capital y Acciones**")

            valor_por_accion = st.selectbox(
                "💵 **Valor nominal por acción (COP)**",
                [100, 500, 1000, 2000, 5000, 10000],
                index=2,  # Default 1000
                help="Recomendado: $1,000 COP (fácil cálculo, profesional)"
            )

            capital_autorizado = st.number_input(
                "💰 **Capital Autorizado (COP)**",
                min_value=valor_por_accion,
                value=st.session_state.company_info.get('capital_autorizado', 150000000),
                step=10000000,
                help="Máximo que puedes emitir sin reformar estatutos"
            )

            acciones_totales = capital_autorizado // valor_por_accion
            st.metric("📊 Total Acciones Disponibles", f"{acciones_totales:,}")

        with col_shares2:
            st.markdown("#### 🎯 **Emisión y Reservas**")

            porcentaje_emision_inicial = st.slider(
                "📈 **% del capital a emitir inicialmente**",
                min_value=10, max_value=90, value=40, step=5,
                help="Recomendado: 30-50% para equipo inicial"
            )

            acciones_a_emitir = int(acciones_totales * porcentaje_emision_inicial / 100)
            acciones_en_reserva = acciones_totales - acciones_a_emitir
            capital_a_emitir = acciones_a_emitir * valor_por_accion

            col_metrics1, col_metrics2 = st.columns(2)
            with col_metrics1:
                st.metric("✅ Acciones a Emitir", f"{acciones_a_emitir:,}")
                st.metric("💳 Capital a Suscribir", f"${capital_a_emitir:,}")
            with col_metrics2:
                st.metric("🏦 Acciones en Reserva", f"{acciones_en_reserva:,}")
                st.metric("📊 % en Reserva", f"{100-porcentaje_emision_inicial}%")

        # Planificación de capas
        st.markdown("#### 🏗️ **Planificación de Capas (Acciones a Emitir)**")

        col_layers1, col_layers2, col_layers3 = st.columns(3)

        with col_layers1:
            st.markdown("**👥 CAPA 1 - Fundadores**")
            porcentaje_fundadores = st.slider(
                "% para fundadores",
                min_value=20, max_value=80, value=60, step=1,
                key="fundadores_slider"
            )
            acciones_fundadores = int(acciones_a_emitir * porcentaje_fundadores / 100)
            st.metric("Acciones", f"{acciones_fundadores:,}")
            st.success("🗳️ Acciones Ordinarias + Protecciones")

        with col_layers2:
            st.markdown("**💼 CAPA 2 - Early Employees**")
            porcentaje_employees = st.slider(
                "% para empleados iniciales",
                min_value=1, max_value=40, value=25, step=1,
                key="employees_slider"
            )
            acciones_employees = int(acciones_a_emitir * porcentaje_employees / 100)
            st.metric("Acciones", f"{acciones_employees:,}")
            st.info("👻 Phantom Equity → Conversión")

        with col_layers3:
            st.markdown("**🎯 CAPA 3 - Pool Futuro**")
            porcentaje_pool = 100 - porcentaje_fundadores - porcentaje_employees
            acciones_pool = acciones_a_emitir - acciones_fundadores - acciones_employees
            st.metric("% restante", f"{porcentaje_pool}%")
            st.metric("Acciones", f"{acciones_pool:,}")
            st.warning("🔄 Para empleados futuros")

        # Costos de registro
        st.markdown("#### 💰 **Costos Estimados de Registro SAS**")

        # Cálculo de costos
        costo_registro_base = 600000  # COP
        costo_por_capital = capital_autorizado * 0.007  # 0.7%
        costo_total_registro = costo_registro_base + costo_por_capital

        col_costs1, col_costs2, col_costs3 = st.columns(3)

        with col_costs1:
            st.metric("📋 Derechos de Matrícula", f"${costo_registro_base:,.0f}")
        with col_costs2:
            st.metric("📊 Registro Mercantil (0.7%)", f"${costo_por_capital:,.0f}")
        with col_costs3:
            st.metric("💰 Total Estimado", f"${costo_total_registro:,.0f}")

        if costo_total_registro > 2000000:
            st.warning("⚠️ **Costo alto**: Considera reducir el capital autorizado si es tu primera empresa.")
        else:
            st.success("✅ **Costo razonable** para una estructura profesional.")

        # Proyección de dilución
        st.markdown("#### 📈 **Proyección de Dilución Futura**")

        if st.checkbox("🔮 **Ver proyección de rondas futuras**"):
            mostrar_proyeccion_dilucion(acciones_totales, acciones_a_emitir, valor_por_accion)

    # Guardar información actualizada
    st.session_state.company_info = {
        'name': company_name,
        'stage': stage,
        'sector': sector,
        'country': country,
        'capital_autorizado': capital_autorizado,
        'capital_suscrito': capital_a_emitir if country == 'Colombia' else st.session_state.company_info.get('capital_suscrito', 200000000),
        'valuation': valuation_actual,
        'busca_inversion': busca_inversion,
        # Nuevos campos para SAS
        'valor_por_accion': valor_por_accion if country == 'Colombia' else 1000,
        'acciones_totales': acciones_totales if country == 'Colombia' else 0,
        'acciones_a_emitir': acciones_a_emitir if country == 'Colombia' else 0,
        'acciones_en_reserva': acciones_en_reserva if country == 'Colombia' else 0,
        'porcentaje_emision_inicial': porcentaje_emision_inicial if country == 'Colombia' else 40,
        'acciones_fundadores': acciones_fundadores if country == 'Colombia' else 0,
        'acciones_employees': acciones_employees if country == 'Colombia' else 0,
        'acciones_pool': acciones_pool if country == 'Colombia' else 0,
        'costo_registro': costo_total_registro if country == 'Colombia' else 0
    }

def mostrar_proyeccion_dilucion(acciones_totales, acciones_emitidas, valor_por_accion):
    """Mostrar proyección de dilución en futuras rondas"""

    st.markdown("##### 🎯 **Simulación de Rondas Futuras**")

    # Pre-Seed
    col_pre, col_seed, col_a = st.columns(3)

    with col_pre:
        st.markdown("**💡 Pre-Seed**")
        max_pre_seed = acciones_totales//4
        default_pre_seed = min(10000, max_pre_seed)
        pre_seed_acciones = st.number_input("Acciones a emitir", 0, max_pre_seed, default_pre_seed, key="pre_seed")
        pre_seed_precio = st.number_input("Precio por acción (COP)", valor_por_accion, valor_por_accion*10, valor_por_accion*2, key="pre_precio")
        pre_seed_dilucion = (pre_seed_acciones / (acciones_emitidas + pre_seed_acciones)) * 100 if pre_seed_acciones > 0 else 0
        st.metric("Dilución", f"{pre_seed_dilucion:.1f}%")
        st.metric("Capital", f"${pre_seed_acciones * pre_seed_precio:,.0f}")

    with col_seed:
        st.markdown("**🌱 Seed**")
        max_seed = acciones_totales//3
        default_seed = min(15000, max_seed)
        seed_acciones = st.number_input("Acciones a emitir", 0, max_seed, default_seed, key="seed")
        seed_precio = st.number_input("Precio por acción (COP)", pre_seed_precio, pre_seed_precio*5, pre_seed_precio*2, key="seed_precio")
        acciones_post_pre = acciones_emitidas + pre_seed_acciones
        seed_dilucion = (seed_acciones / (acciones_post_pre + seed_acciones)) * 100 if seed_acciones > 0 else 0
        st.metric("Dilución", f"{seed_dilucion:.1f}%")
        st.metric("Capital", f"${seed_acciones * seed_precio:,.0f}")

    with col_a:
        st.markdown("**🚀 Serie A**")
        max_serie_a = acciones_totales//2
        default_serie_a = min(20000, max_serie_a)
        a_acciones = st.number_input("Acciones a emitir", 0, max_serie_a, default_serie_a, key="serie_a")
        a_precio = st.number_input("Precio por acción (COP)", seed_precio, seed_precio*5, seed_precio*3, key="a_precio")
        acciones_post_seed = acciones_post_pre + seed_acciones
        a_dilucion = (a_acciones / (acciones_post_seed + a_acciones)) * 100 if a_acciones > 0 else 0
        st.metric("Dilución", f"{a_dilucion:.1f}%")
        st.metric("Capital", f"${a_acciones * a_precio:,.0f}")

    # Resumen final
    acciones_finales = acciones_emitidas + pre_seed_acciones + seed_acciones + a_acciones
    acciones_restantes = acciones_totales - acciones_finales

    st.markdown("##### 📊 **Resumen Final**")
    col_final1, col_final2, col_final3 = st.columns(3)

    with col_final1:
        st.metric("💼 Acciones Emitidas Total", f"{acciones_finales:,}")
        st.metric("🏦 Acciones Aún Disponibles", f"{acciones_restantes:,}")

    with col_final2:
        porcentaje_usado = (acciones_finales / acciones_totales) * 100
        st.metric("📈 % Capital Utilizado", f"{porcentaje_usado:.1f}%")
        st.metric("🎯 % Aún Disponible", f"{100-porcentaje_usado:.1f}%")

    with col_final3:
        dilucion_total_fundadores = ((pre_seed_dilucion + seed_dilucion + a_dilucion) / 100) * 60  # Asumiendo 60% inicial
        st.metric("😱 Dilución Total Fundadores", f"{dilucion_total_fundadores:.1f}%")

        if dilucion_total_fundadores > 40:
            st.error("❌ Dilución excesiva")
        elif dilucion_total_fundadores > 25:
            st.warning("⚠️ Dilución alta")
        else:
            st.success("✅ Dilución manejable")

def socios_management_section():
    st.markdown('<h2 class="section-header">👥 Gestión de Socios</h2>', unsafe_allow_html=True)
    
    # Guía rápida
    with st.expander("📚 ¿Necesitas ayuda? - Guía rápida", expanded=False):
        col_help1, col_help2 = st.columns(2)
        
        with col_help1:
            st.markdown("""
            **🎯 Distribución típica:**
            - **Fundador Principal**: 35-51%
            - **Co-fundadores**: 10-25% cada uno
            - **Empleados clave**: 1-5%
            - **Advisors**: 0.25-1%
            """)
            
        with col_help2:
            st.markdown("""
            **⏳ Vesting estándar:**
            - **Período**: 4 años
            - **Cliff**: 12 meses
            - **Cronograma**: Mensual
            - **Para todos**: Sí, incluso fundadores
            """)
    
    # Modo de edición
    if st.session_state.edit_mode and st.session_state.editing_socio is not None:
        socio_index = st.session_state.editing_socio
        socio_data = st.session_state.socios[socio_index]
        
        # Formulario de edición
        datos_formulario = formulario_socio(socio_data, "editar")
        
        # Botones de acción para edición
        col_edit1, col_edit2, col_edit3 = st.columns(3)
        
        with col_edit1:
            if st.button("💾 **Guardar Cambios**", type="primary", use_container_width=True):
                if datos_formulario['nombre'] and datos_formulario['equity_total'] > 0:
                    st.session_state.socios[socio_index] = datos_formulario
                    st.session_state.edit_mode = False
                    st.session_state.editing_socio = None
                    st.success(f"✅ Cambios guardados para {datos_formulario['nombre']}!")
                    st.rerun()
                else:
                    st.error("❌ Completa el nombre y asigna equity válido")
        
        with col_edit2:
            if st.button("❌ **Cancelar**", type="secondary", use_container_width=True):
                st.session_state.edit_mode = False
                st.session_state.editing_socio = None
                st.rerun()
        
        with col_edit3:
            st.info("💡 Los cambios no se guardan hasta que hagas clic en 'Guardar'")
    
    else:
        # Formulario para agregar nuevo socio
        with st.expander("➕ Agregar Nuevo Socio", expanded=True):
            datos_formulario = formulario_socio(None, "agregar")
            
            if st.button("➕ **Agregar Socio**", type="primary", use_container_width=True):
                if datos_formulario['nombre'] and datos_formulario['equity_total'] > 0:
                    st.session_state.socios.append(datos_formulario)
                    st.success(f"🎉 ¡{datos_formulario['nombre']} agregado exitosamente!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Completa el nombre y asigna al menos algo de equity")
    
    # Lista de socios actuales (mejorada)
    if st.session_state.socios:
        st.markdown('<h3 class="section-header">📋 Socios Registrados</h3>', unsafe_allow_html=True)
        
        # Mostrar resumen visual
        for i, socio in enumerate(st.session_state.socios):
            equity_total = (socio['acciones_ordinarias'] + socio['acciones_preferenciales'] + socio['stock_options'] +
                          socio.get('phantom_equity', 0) + socio.get('acciones_vesting', 0))
            
            # Destacar si está en modo edición
            is_editing = st.session_state.edit_mode and st.session_state.editing_socio == i
            
            with st.container():
                if is_editing:
                    st.markdown('<div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #2196f3;">', unsafe_allow_html=True)
                    st.markdown("**🔧 EDITANDO ESTE SOCIO**")
                
                col_socio1, col_socio2, col_socio3, col_socio4 = st.columns([3, 2, 2, 1.5])
                
                with col_socio1:
                    st.markdown(f"**👤 {socio['nombre']}**")
                    st.caption(f"{socio['rol']} • {socio['categoria']} • {socio['dedicacion']}")
                
                with col_socio2:
                    st.metric("Total Equity", f"{equity_total:.1f}%")
                    
                with col_socio3:
                    vesting_info = f"{socio['vesting_total']}a, cliff {socio['cliff_period']}m"
                    st.write(f"**Vesting:** {vesting_info}")
                    proteccion_status = "🛡️ Protegido" if socio.get('proteccion_antidilucion', False) else "❌ Sin protección"
                    st.caption(f"💰 Aporte: ${socio['aporte_inicial']:,} • {proteccion_status}")
                
                with col_socio4:
                    if not st.session_state.edit_mode:
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button(f"✏️", key=f"edit_{i}", help=f"Editar {socio['nombre']}"):
                                st.session_state.edit_mode = True
                                st.session_state.editing_socio = i
                                st.rerun()
                        with col_btn2:
                            if st.button(f"🗑️", key=f"delete_{i}", help=f"Eliminar {socio['nombre']}"):
                                st.session_state.socios.pop(i)
                                st.success(f"✅ {socio['nombre']} eliminado!")
                                st.rerun()
                    else:
                        if is_editing:
                            st.write("**Editando...**")
                        else:
                            st.write("*Bloqueado*")
                
                if is_editing:
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.divider()
    
    else:
        st.info("📝 **No hay socios registrados aún.** \n¡Agrega tu primer socio usando el formulario de arriba!")
        
        # Sugerir importar ejemplo
        if st.button("🎯 **¿Quieres ver un ejemplo?** Importa datos de muestra"):
            st.info("💡 Ve a la pestaña **'Export/Import'** y carga el archivo **'ejemplo_startup.json'** para ver una startup completa!")

def equity_analysis_section():
    st.markdown('<h2 class="section-header">📈 Análisis de Equity</h2>', unsafe_allow_html=True)
    
    if not st.session_state.socios:
        st.warning("⚠️ No hay socios registrados. Ve a la pestaña 'Gestión Socios' para agregar.")
        return
    
    # Calcular totales
    df = pd.DataFrame(st.session_state.socios)
    
    total_ordinarias = df['acciones_ordinarias'].sum()
    total_preferenciales = df['acciones_preferenciales'].sum()
    total_options = df['stock_options'].sum()
    total_phantom = df['phantom_equity'].sum() if 'phantom_equity' in df.columns else 0
    total_vesting = df['acciones_vesting'].sum() if 'acciones_vesting' in df.columns else 0
    total_equity = total_ordinarias + total_preferenciales + total_options + total_phantom + total_vesting
    
    # Métricas principales
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🗳️ Ordinarias", f"{total_ordinarias:.1f}%")
    with col2:
        st.metric("👻 Phantom", f"{total_phantom:.1f}%")
    with col3:
        st.metric("📈 Acciones Vesting", f"{total_vesting:.1f}%")
    with col4:
        st.metric("📊 Options", f"{total_options:.1f}%")
    with col5:
        st.metric("📊 Total", f"{total_equity:.1f}%")
    
    # Alertas
    if total_equity > 100:
        st.error(f"❌ **ERROR**: Total de equity asignado ({total_equity:.1f}%) excede el 100%")
    elif total_equity > 85:
        st.warning(f"⚠️ **ATENCIÓN**: Alto porcentaje asignado ({total_equity:.1f}%). Considera reservar más para futuros empleados e inversores.")
    elif total_equity < 60:
        st.info(f"ℹ️ **INFO**: Tienes {100-total_equity:.1f}% disponible para futuros empleados e inversores.")
    
    # Gráficos
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**📊 Distribución por Socio (Equity Total)**")
        df['equity_total'] = (df['acciones_ordinarias'] + df['acciones_preferenciales'] + df['stock_options'] +
                             (df['phantom_equity'] if 'phantom_equity' in df.columns else 0) +
                             (df['acciones_vesting'] if 'acciones_vesting' in df.columns else 0))
        fig_pie = px.pie(df, values='equity_total', names='nombre',
                        title="Distribución de Equity Total")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col_chart2:
        st.markdown("**📈 Distribución por Tipo de Acción**")
        equity_types = {
            'Acciones Ordinarias': total_ordinarias,
            'Phantom Equity': total_phantom,
            'Acciones con Vesting': total_vesting,
            'Stock Options': total_options,
            'Disponible': max(0, 100 - total_equity)
        }
        fig_pie2 = px.pie(values=list(equity_types.values()), names=list(equity_types.keys()),
                         title="Distribución por Tipo de Equity")
        st.plotly_chart(fig_pie2, use_container_width=True)
    
    # Análisis por categoría
    st.markdown("**🏷️ Análisis por Categoría**")
    category_analysis = df.groupby('categoria').agg({
        'acciones_ordinarias': 'sum',
        'acciones_preferenciales': 'sum',
        'stock_options': 'sum',
        **{col: 'sum' for col in ['phantom_equity', 'acciones_vesting'] if col in df.columns},
        'nombre': 'count'
    }).round(2)

    # Renombrar columnas dinámicamente
    new_columns = ['Ordinarias %', 'Preferenciales %', 'Options %']
    if 'phantom_equity' in df.columns:
        new_columns.append('Phantom %')
    if 'acciones_vesting' in df.columns:
        new_columns.append('Vesting %')
    new_columns.append('Cantidad')

    category_analysis.columns = new_columns

    # Calcular total dinámicamente
    total_cols = [col for col in category_analysis.columns if col.endswith('%') and col != 'Total %']
    category_analysis['Total %'] = category_analysis[total_cols].sum(axis=1)
    st.dataframe(category_analysis, use_container_width=True)
    
    # Simulación de dilución
    st.markdown('<h3 class="section-header">💧 Simulador de Dilución</h3>', unsafe_allow_html=True)

    col_sim1, col_sim2, col_sim3 = st.columns(3)

    with col_sim1:
        nueva_emision = st.number_input("📈 Nueva emisión (%)", min_value=0.0, max_value=50.0, value=20.0, step=1.0)
    with col_sim2:
        tipo_emision = st.selectbox("🏷️ Tipo de emisión", ['Inversores', 'Pool empleados', 'Mixto'])
    with col_sim3:
        if st.button("🧮 Calcular Dilución"):
            calcular_dilucion(df, nueva_emision)

    # Simulador de Derechos Pro-rata
    st.markdown('<h3 class="section-header">🎯 Simulador de Derechos Pro-rata</h3>', unsafe_allow_html=True)

    # Verificar si hay socios con derechos pro-rata
    socios_con_prorata = df[df.get('derechos_prorata', False) == True] if 'derechos_prorata' in df.columns else pd.DataFrame()

    if not socios_con_prorata.empty:
        st.info(f"📊 **{len(socios_con_prorata)} socios tienen derechos pro-rata configurados**")

        col_prorata_sim1, col_prorata_sim2 = st.columns(2)

        with col_prorata_sim1:
            # Configuración de la simulación
            st.markdown("**⚙️ Configuración de la Nueva Emisión:**")

            monto_recaudar = st.number_input(
                "💰 **Monto a recaudar (USD)**",
                min_value=10000, max_value=10000000,
                value=500000, step=50000,
                help="¿Cuánto dinero quiere recaudar la empresa?"
            )

            valoracion_pre_money = st.number_input(
                "📊 **Valoración pre-money (USD)**",
                min_value=100000, max_value=50000000,
                value=2000000, step=100000,
                help="¿Cuál es la valoración de la empresa ANTES de la nueva inversión?"
            )

            # Calcular valoración post-money y porcentaje de dilución
            valoracion_post_money = valoracion_pre_money + monto_recaudar
            porcentaje_nueva_emision = (monto_recaudar / valoracion_post_money) * 100
            precio_por_accion = valoracion_pre_money / 1000000  # Asumiendo 1M acciones base

            st.metric("💹 Valoración post-money", f"${valoracion_post_money:,}")
            st.metric("📉 Dilución total", f"{porcentaje_nueva_emision:.1f}%")
            st.metric("💵 Precio por acción", f"${precio_por_accion:.2f}")

        with col_prorata_sim2:
            st.markdown("**🎯 Configuración de Derechos:**")

            incluir_en_prorata = st.multiselect(
                "¿Qué tipo de emisión es?",
                [
                    "Emisiones para empleados (stock options)",
                    "Conversión de deuda en acciones",
                    "Emisiones de acciones preferenciales",
                    "Fusiones y adquisiciones",
                    "Spin-offs o escisiones"
                ],
                help="Selecciona si esta emisión tiene exclusiones para algunos socios"
            )

            # Determinar qué socios pueden ejercer
            socios_elegibles = socios_con_prorata.copy()

            # Filtrar por exclusiones
            for _, socio in socios_elegibles.iterrows():
                exclusiones = socio.get('exclusiones_prorata', [])
                for exclusion in incluir_en_prorata:
                    if exclusion in exclusiones:
                        socios_elegibles = socios_elegibles.drop(socio.name)
                        break

            # Filtrar por participación mínima
            for _, socio in socios_elegibles.iterrows():
                equity_total = (socio['acciones_ordinarias'] + socio['acciones_preferenciales'] + socio['stock_options'] +
                              socio.get('phantom_equity', 0) + socio.get('acciones_vesting', 0))
                participacion_minima = socio.get('participacion_minima_prorata', 1.0)
                if equity_total < participacion_minima:
                    socios_elegibles = socios_elegibles.drop(socio.name)

            st.metric("✅ Socios elegibles", len(socios_elegibles))

            if len(socios_elegibles) > 0:
                porcentaje_ejercicio = st.slider(
                    "💪 **¿Qué % de socios ejercerán sus derechos?**",
                    min_value=0, max_value=100, value=80, step=10,
                    help="En la realidad, no todos los socios ejercen sus derechos"
                )

        # Botón de simulación
        if st.button("🚀 **Simular Emisión con Derechos Pro-rata**", type="primary"):
            if len(socios_elegibles) > 0:
                simular_emision_prorata(
                    df, socios_elegibles, monto_recaudar,
                    valoracion_pre_money, porcentaje_ejercicio
                )
            else:
                st.warning("⚠️ No hay socios elegibles para ejercer derechos pro-rata en este tipo de emisión.")

    else:
        st.info("ℹ️ **No hay socios con derechos pro-rata configurados.** Configura derechos pro-rata en la sección 'Gestión Socios' para usar este simulador.")

        if st.button("➕ **¿Cómo agregar derechos pro-rata?**"):
            st.markdown("""
            **📋 Pasos para configurar derechos pro-rata:**

            1. Ve a la pestaña **'Gestión Socios'**
            2. Edita un socio existente o agrega uno nuevo
            3. En la sección **'🎯 Derechos Pro-rata'**, marca la casilla
            4. Configura el tipo de derechos y parámetros
            5. Guarda los cambios
            6. Regresa aquí para simular emisiones
            """)

def simular_emision_prorata(df, socios_elegibles, monto_recaudar, valoracion_pre_money, porcentaje_ejercicio):
    """Simular emisión de acciones con derechos pro-rata"""
    st.markdown("### 🚀 **Resultados de la Simulación Pro-rata**")

    # Calcular parámetros básicos
    valoracion_post_money = valoracion_pre_money + monto_recaudar
    porcentaje_nueva_emision = (monto_recaudar / valoracion_post_money) * 100

    # Crear tabla de resultados
    resultados = []

    total_ejercido = 0
    total_no_ejercido = 0

    for _, socio in socios_elegibles.iterrows():
        equity_actual = socio['acciones_ordinarias'] + socio['acciones_preferenciales'] + socio['stock_options']

        # Calcular derecho pro-rata
        derecho_porcentaje = equity_actual * (porcentaje_nueva_emision / 100)
        derecho_monto = (equity_actual / 100) * monto_recaudar

        # Simular si ejerce o no (basado en el porcentaje de ejercicio)
        import random
        random.seed(hash(socio['nombre']))  # Para consistencia en la simulación
        ejerce = random.random() < (porcentaje_ejercicio / 100)

        if ejerce:
            equity_final = equity_actual  # Mantiene su porcentaje
            dilución = 0
            costo = derecho_monto
            status = "✅ Ejerció"
            total_ejercido += derecho_monto
        else:
            # Sufre dilución
            factor_dilucion = 100 / (100 + porcentaje_nueva_emision)
            equity_final = equity_actual * factor_dilucion
            dilución = equity_actual - equity_final
            costo = 0
            status = "❌ No ejerció"
            total_no_ejercido += derecho_monto

        resultados.append({
            'Socio': socio['nombre'],
            'Categoria': socio['categoria'],
            'Equity Inicial %': round(equity_actual, 2),
            'Derecho ($)': f"${derecho_monto:,.0f}",
            'Status': status,
            'Equity Final %': round(equity_final, 2),
            'Dilución %': round(dilución, 2),
            'Costo ($)': f"${costo:,.0f}" if costo > 0 else "N/A"
        })

    # Mostrar tabla de resultados
    df_resultados = pd.DataFrame(resultados)
    st.dataframe(df_resultados, use_container_width=True, hide_index=True)

    # Métricas de resumen
    st.markdown("---")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)

    with col_res1:
        st.metric("💰 Total ejercido", f"${total_ejercido:,.0f}")

    with col_res2:
        st.metric("💸 Disponible para externos", f"${total_no_ejercido:,.0f}")

    with col_res3:
        socios_que_ejercieron = len([r for r in resultados if "✅" in r['Status']])
        st.metric("✅ Socios que ejercieron", f"{socios_que_ejercieron}/{len(resultados)}")

    with col_res4:
        porcentaje_ejercido = (total_ejercido / monto_recaudar) * 100 if monto_recaudar > 0 else 0
        st.metric("📊 % Ejercido", f"{porcentaje_ejercido:.1f}%")

    # Análisis de impacto
    st.markdown("### 📈 **Análisis de Impacto**")

    if total_no_ejercido > 0:
        st.warning(f"⚠️ **${total_no_ejercido:,.0f} disponibles para inversores externos** - Esto podría traer mayor dilución para quienes no ejercieron.")

    if porcentaje_ejercido > 70:
        st.success("✅ **Alto nivel de ejercicio** - Los socios mantuvieron bien su participación.")
    elif porcentaje_ejercido > 40:
        st.info("ℹ️ **Nivel moderado de ejercicio** - Balance entre socios actuales y externos.")
    else:
        st.warning("⚠️ **Bajo nivel de ejercicio** - Mayor oportunidad para inversores externos.")

    # Recomendaciones
    with st.expander("💡 **Recomendaciones y Próximos Pasos**"):
        st.markdown(f"""
        **📋 Basado en esta simulación:**

        1. **Para socios que NO ejercieron:**
           - Sufrirán dilución del {porcentaje_nueva_emision:.1f}%
           - Considerar renegociar términos o buscar financiamiento

        2. **Para la empresa:**
           - Necesita conseguir ${total_no_ejercido:,.0f} adicionales de inversores externos
           - Podría ofrecer los derechos no ejercidos a otros socios (sobresuscripción)

        3. **Timing:**
           - Los socios tienen {socios_elegibles.iloc[0].get('plazo_ejercicio_prorata', '30 días')} para decidir
           - Planificar comunicación clara sobre términos y beneficios

        4. **Alternativas:**
           - Considerar prestamos puente para socios que quieren ejercer pero no tienen liquidez
           - Ofrecer pagos diferidos o por cuotas
        """)

def calcular_dilucion(df, nueva_emision):
    st.markdown("**📊 Efectos de la Dilución:**")

    factor_dilucion = 100 / (100 + nueva_emision)

    df_diluido = df.copy()
    df_diluido['equity_actual'] = df['acciones_ordinarias'] + df['acciones_preferenciales'] + df['stock_options']
    df_diluido['equity_post_dilucion'] = df_diluido['equity_actual'] * factor_dilucion
    df_diluido['perdida_equity'] = df_diluido['equity_actual'] - df_diluido['equity_post_dilucion']

    cols_show = ['nombre', 'equity_actual', 'equity_post_dilucion', 'perdida_equity']
    st.dataframe(df_diluido[cols_show].round(2), use_container_width=True)

def claude_prompt_section():
    st.markdown('<h2 class="section-header">📋 Generador de Prompt para Claude</h2>', unsafe_allow_html=True)
    
    if not st.session_state.socios:
        st.warning("⚠️ Necesitas agregar socios primero para generar el prompt.")
        return
    
    # Configuración del prompt
    st.markdown("**⚙️ Configuración del Análisis:**")
    
    col_config1, col_config2 = st.columns(2)
    
    with col_config1:
        areas_focus = st.multiselect("🎯 Áreas de enfoque", [
            'Estructura de vesting', 'Cláusulas de salida', 'Pacto de socios',
            'Estatutos corporativos', 'Protección anti-dilución', 'Derechos de voto',
            'Transferencia de acciones', 'Valoración de salida', 'Pool de empleados',
            'Estrategia de inversión', 'Aspectos fiscales', 'Cumplimiento legal'
        ], default=['Estructura de vesting', 'Cláusulas de salida', 'Pacto de socios'])
    
    with col_config2:
        urgencia = st.selectbox("⚡ Nivel de urgencia", [
            'Exploratoria', 'Planificación', 'Implementación urgente', 'Crisis/Conflicto'
        ])
        detalle_nivel = st.selectbox("📊 Nivel de detalle", [
            'Resumen ejecutivo', 'Análisis detallado', 'Implementación completa'
        ])
    
    # Problemas específicos
    st.markdown("**🚨 Problemas o Preocupaciones Específicas:**")
    problemas_especificos = st.text_area(
        "Describe cualquier problema actual o preocupación específica",
        height=100,
        placeholder="Ej: Uno de los cofundadores quiere reducir su dedicación, necesitamos atraer inversión, hay conflictos sobre la distribución actual..."
    )
    
    # Objetivos
    objetivos = st.text_area(
        "🎯 Objetivos principales de la consultoría",
        height=100,
        placeholder="Ej: Estructurar documentos legales, preparar para ronda de inversión, resolver conflictos entre socios..."
    )
    
    if st.button("🤖 Generar Prompt para Claude", type="primary"):
        prompt = generar_prompt_claude(areas_focus, urgencia, detalle_nivel, problemas_especificos, objetivos)
        
        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.markdown("### 🤖 Prompt Generado para Claude:")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.code(prompt, language="text")
        
        # Botón para copiar
        st.markdown("**📋 Copia este prompt y úsalo en una nueva conversación con Claude**")

def generar_prompt_claude(areas_focus, urgencia, detalle_nivel, problemas_especificos, objetivos):
    # Preparar datos de la empresa
    company_data = st.session_state.company_info
    socios_data = st.session_state.socios
    
    # Calcular métricas
    df = pd.DataFrame(socios_data)
    total_equity = (df['acciones_ordinarias'] + df['acciones_preferenciales'] + df['stock_options']).sum()
    
    prompt = f"""Actúa como un experto consultor en estructuración de startups y derecho corporativo. Necesito tu análisis y recomendaciones para la siguiente startup:

## 📊 INFORMACIÓN DE LA EMPRESA:
- **Nombre**: {company_data.get('name', 'No especificado')}
- **Etapa**: {company_data.get('stage', 'No especificado')}
- **Sector**: {company_data.get('sector', 'No especificado')}
- **País**: {company_data.get('country', 'No especificado')}
- **Capital Autorizado**: ${company_data.get('capital_autorizado', 0):,} COP
- **Capital Suscrito**: ${company_data.get('capital_suscrito', 0):,} COP
- **Valoración Actual**: ${company_data.get('valuation', 0):,} USD
- **Busca Inversión**: {'Sí' if company_data.get('busca_inversion', False) else 'No'}

## 👥 ESTRUCTURA DE SOCIOS ACTUAL:
**Total Equity Asignado**: {total_equity:.1f}%
**Equity Disponible**: {100-total_equity:.1f}%

"""
    
    # Agregar detalles de cada socio
    for i, socio in enumerate(socios_data, 1):
        proteccion_info = ""
        if socio.get('proteccion_antidilucion', False):
            proteccion_info = f"""
- **Protección Antidilución**: {socio.get('tipo_proteccion', 'No especificado')}
  - Porcentaje protegido: {socio.get('porcentaje_proteccion', 0)}%
  - Umbral activación: {socio.get('umbral_activacion', 0)}% descuento
  - Duración: {socio.get('duracion_proteccion', 'No especificado')}"""
        else:
            proteccion_info = "\n- **Protección Antidilución**: No configurada"

        prorata_info = ""
        if socio.get('derechos_prorata', False):
            exclusiones_str = ", ".join(socio.get('exclusiones_prorata', []))
            prorata_info = f"""
- **Derechos Pro-rata**: {socio.get('tipo_derechos_prorata', 'No especificado')}
  - Participación mínima: {socio.get('participacion_minima_prorata', 0)}%
  - Plazo ejercicio: {socio.get('plazo_ejercicio_prorata', 'No especificado')}
  - Transferible: {'Sí' if socio.get('transferibilidad_derechos', False) else 'No'}
  - Exclusiones: {exclusiones_str if exclusiones_str else 'Ninguna'}"""
        else:
            prorata_info = "\n- **Derechos Pro-rata**: No configurados"

        prompt += f"""
### Socio {i}: {socio['nombre']}
- **Rol**: {socio['rol']} ({socio['categoria']})
- **Dedicación**: {socio['dedicacion']}
- **Equity Total**: {socio['acciones_ordinarias'] + socio['acciones_preferenciales'] + socio['stock_options']:.1f}%
  - Ordinarias: {socio['acciones_ordinarias']:.1f}%
  - Preferenciales: {socio['acciones_preferenciales']:.1f}%
  - Stock Options: {socio['stock_options']:.1f}%
- **Vesting**: {socio['vesting_total']} años, cliff {socio['cliff_period']} meses
- **Aporte Inicial**: ${socio['aporte_inicial']:,} COP
- **Salario**: ${socio['salario']:,} COP/mes{proteccion_info}{prorata_info}
"""
    
    prompt += f"""

## 🎯 ÁREAS DE ENFOQUE PRIORITARIAS:
{chr(10).join([f'- {area}' for area in areas_focus])}

## 🚨 PROBLEMAS/PREOCUPACIONES ESPECÍFICAS:
{problemas_especificos if problemas_especificos else 'No se especificaron problemas particulares.'}

## 🎯 OBJETIVOS PRINCIPALES:
{objetivos if objetivos else 'Estructuración general y mejores prácticas.'}

## 📋 SOLICITUD ESPECÍFICA:
Por favor proporciona un análisis {detalle_nivel.lower()} con nivel de urgencia {urgencia.lower()} que incluya:

### 1. 🔍 ANÁLISIS DE LA ESTRUCTURA ACTUAL:
- Evaluación de la distribución de equity
- Identificación de problemas potenciales
- Análisis de la estructura de vesting
- Evaluación del balance fundadores vs empleados vs inversores

### 2. ⚖️ RECOMENDACIONES LEGALES:
- **Estatutos**: Cláusulas específicas a incluir para {company_data.get('country', 'Colombia')}
- **Pacto de Socios**: Elementos críticos a documentar
- **Vesting**: Estructura recomendada y cláusulas de protección
- **Cláusulas de Salida**: Mecanismos de salida, drag-along, tag-along, etc.

### 3. 📄 DOCUMENTOS NECESARIOS:
- Lista priorizada de documentos legales a crear/modificar
- Timeline de implementación
- Costos estimados

### 4. 🚀 ESTRATEGIA DE CRECIMIENTO:
- Preparación para futuras rondas de inversión
- Estructura de pool para empleados
- Mecanismos de incentivos

### 5. ⚠️ RIESGOS Y MITIGACIÓN:
- Identificación de riesgos principales
- Estrategias de mitigación
- Señales de alerta temprana

### 6. 📅 PLAN DE ACCIÓN:
- Pasos inmediatos (próximas 2 semanas)
- Mediano plazo (1-3 meses)
- Largo plazo (6+ meses)

## 📝 FORMATO DE RESPUESTA:
- Usa secciones claras con headers
- Incluye ejemplos de cláusulas cuando sea relevante
- Proporciona justificaciones para cada recomendación
- Señala aspectos específicos del derecho {company_data.get('country', 'colombiano')}
- Incluye templates o formatos sugeridos donde aplique

¡Gracias por tu análisis experto!"""

    return prompt

def export_import_section():
    st.markdown('<h2 class="section-header">💾 Export/Import de Datos</h2>', unsafe_allow_html=True)
    
    # Exportar datos
    st.markdown("### 📤 Exportar Configuración")
    
    if st.session_state.socios or st.session_state.company_info:
        export_data = {
            'company_info': st.session_state.company_info,
            'socios': st.session_state.socios,
            'export_date': datetime.now().isoformat()
        }
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            if st.button("📄 Exportar como JSON"):
                st.download_button(
                    label="⬇️ Descargar configuración",
                    data=json.dumps(export_data, indent=2, ensure_ascii=False),
                    file_name=f"startup_equity_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    mime="application/json"
                )
        
        with col_exp2:
            if st.button("📊 Exportar como CSV"):
                if st.session_state.socios:
                    df = pd.DataFrame(st.session_state.socios)
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Descargar CSV",
                        data=csv,
                        file_name=f"socios_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
    else:
        st.info("ℹ️ No hay datos para exportar. Agrega información de la empresa y socios primero.")
    
    # Importar datos
    st.markdown("### 📥 Importar Configuración")
    
    uploaded_file = st.file_uploader("📁 Seleccionar archivo JSON", type=['json'])
    
    if uploaded_file is not None:
        try:
            import_data = json.load(uploaded_file)
            
            col_imp1, col_imp2 = st.columns(2)
            
            with col_imp1:
                st.markdown("**📋 Datos a importar:**")
                st.write(f"- Información empresa: {'✅' if 'company_info' in import_data else '❌'}")
                st.write(f"- Socios: {len(import_data.get('socios', []))} registros")
                st.write(f"- Fecha exportación: {import_data.get('export_date', 'No disponible')}")
            
            with col_imp2:
                if st.button("📥 Importar Datos", type="primary"):
                    if 'company_info' in import_data:
                        st.session_state.company_info = import_data['company_info']
                    if 'socios' in import_data:
                        st.session_state.socios = import_data['socios']
                    
                    # Resetear modo edición al importar
                    st.session_state.edit_mode = False
                    st.session_state.editing_socio = None
                    
                    st.success("✅ Datos importados exitosamente!")
                    st.rerun()
                
                if st.button("🗑️ Limpiar Datos Actuales", type="secondary"):
                    st.session_state.socios = []
                    st.session_state.company_info = {}
                    st.session_state.edit_mode = False
                    st.session_state.editing_socio = None
                    st.success("✅ Datos limpiados!")
                    st.rerun()
                    
        except Exception as e:
            st.error(f"❌ Error al importar archivo: {str(e)}")

    # Información útil
    st.markdown("### 📚 Información Útil")
    
    with st.expander("💡 Consejos de Uso"):
        st.markdown("""
        **🎯 Mejores Prácticas:**
        
        1. **Estructura Típica de Startup:**
           - Fundadores: 60-80%
           - Pool empleados: 15-20%
           - Reserva inversores: 20-25%
        
        2. **Vesting Recomendado:**
           - Período: 4 años
           - Cliff: 12 meses
           - Cronograma: Mensual
        
        3. **Categorías Sugeridas:**
           - **Fundador Principal**: 25-51%
           - **Co-fundadores**: 5-25% cada uno
           - **Early Employees**: 0.1-5%
           - **Advisors**: 0.25-1%
        
        4. **Alertas Importantes:**
           - No asignar más del 85% inicialmente
           - Implementar vesting para todos
           - Documentar todo legalmente
           - Planificar para dilución futura
        """)
    
    with st.expander("🔧 Funcionalidades"):
        st.markdown("""
        **📊 Esta herramienta te permite:**
        
        - ✅ **Agregar socios** con información completa
        - ✅ **Editar socios existentes** - ¡NUEVO!
        - ✅ **Eliminar socios** cuando sea necesario
        - ✅ **Exportar/importar** configuraciones
        - ✅ **Analizar distribución** de equity
        - ✅ **Generar prompts** para Claude
        - ✅ **Simular dilución** por nuevas emisiones
        
        **🛠️ Flujo de edición:**
        1. Haz clic en ✏️ junto al socio que quieres editar
        2. Modifica los datos en el formulario
        3. Guarda cambios o cancela
        4. ¡Los cambios se reflejan inmediatamente!
        
        **🤖 Integración con Claude:**
        - Genera prompts específicos y detallados
        - Incluye toda la información relevante
        - Enfoque en aspectos legales colombianos
        - Recomendaciones personalizadas
        """)

    # Pie de página
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 50px;">
        <p><strong>🚀 Startup Equity Manager</strong> - Herramienta educativa para startups colombianas</p>
        <p>Especializada en SAS (Sociedades por Acciones Simplificadas) • Normatividad Ley 1258 de 2008</p>
        <p style="font-size: 0.8em;">
            ⚖️ No constituye asesoría legal • 🔒 Datos almacenados solo en tu navegador •
            📊 Exporta tu configuración antes de cerrar
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

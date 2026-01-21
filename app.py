import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Churrasco.ai 🥩",
    page_icon="🥩",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================
# CSS DARK PREMIUM - STEAKHOUSE MODERNA
# ============================================
st.markdown("""
<style>
    /* Fontes: Oswald (Títulos) e Inter (Corpo) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Oswald:wght@400;500;700&display=swap');

    /* Geral */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, .main-title, .categoria-header, .metric-value {
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Header Principal */
    .main-header {
        text-align: center;
        padding: 3rem 1rem;
        background: radial-gradient(circle at center, #1E1E1E 0%, #0E1117 100%);
        border-bottom: 2px solid #262730;
        margin-bottom: 2rem;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 700;
        color: #FF4B4B;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 75, 75, 0.3);
    }
    
    .subtitle {
        color: #E0E0E0;
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 10px;
        letter-spacing: 2px;
        opacity: 0.8;
    }

    /* Cards Sólidos */
    .premium-card {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Métricas */
    .metric-card {
        background-color: #262730;
        border-left: 4px solid #FF4B4B;
        border-radius: 4px;
        padding: 1rem;
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        background-color: #2D2E36;
    }
    .metric-value {
        font-size: 2rem;
        color: #FFF;
        font-weight: 500;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #AAA;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Categorias */
    .categoria-header {
        color: #FFAE00;
        border-bottom: 1px solid #333;
        padding-bottom: 5px;
        margin: 2rem 0 1rem 0;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Lista de Itens */
    .item-card {
        background-color: #15161A;
        border: 1px solid #262730;
        padding: 12px 16px;
        margin: 5px 0;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .item-card span {
        font-size: 1rem;
        color: #EEE;
    }

    /* Total Card */
    .total-card {
        background: #FF4B4B;
        color: white;
        padding: 2rem;
        text-align: center;
        margin-top: 2rem;
        border-radius: 0;
        clip-path: polygon(0 0, 100% 0, 100% 85%, 95% 100%, 0 100%);
    }
    .total-label {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        opacity: 0.9;
    }
    .total-value {
        font-size: 3.5rem;
        font-weight: 700;
    }

    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #0E1117 !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 4px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #FF4B4B !important;
        box-shadow: none !important;
    }

    /* Botões */
    .stButton > button {
        background-color: #FF4B4B !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.5rem !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background-color: #D43939 !important;
        color: white !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent;
        border-bottom: 2px solid #333;
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #777;
        font-family: 'Oswald', sans-serif;
        font-size: 1.1rem;
        padding: 10px 0;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #FF4B4B !important;
        border-bottom: 3px solid #FF4B4B;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0E1117;
        border-right: 1px solid #262730;
    }

    /* Upload */
    [data-testid="stFileUploader"] {
        border: 1px dashed #444;
        background-color: #15161A;
        padding: 2rem;
    }

    /* Dividers */
    hr {
        border-color: #333;
    }
    
    /* WhatsApp Msg */
    .whatsapp-msg {
        background-color: #121212;
        border-left: 3px solid #00E676;
        color: #eee;
        padding: 1rem;
        font-family: monospace;
        margin-top: 1rem;
        border-radius: 0 8px 8px 0;
    }
    
    .dica-card {
        background-color: #262730;
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
        border-left: 3px solid #FFAE00;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================
if 'lista_compras' not in st.session_state:
    st.session_state.lista_compras = None
if 'itens_nota' not in st.session_state:
    st.session_state.itens_nota = None
if 'participantes' not in st.session_state:
    st.session_state.participantes = []
if 'divisao' not in st.session_state:
    st.session_state.divisao = None
if 'mensagens_cobranca' not in st.session_state:
    st.session_state.mensagens_cobranca = {}
if 'historico_churrascos' not in st.session_state:
    st.session_state.historico_churrascos = []
if 'templates_salvos' not in st.session_state:
    st.session_state.templates_salvos = []

# ============================================
# SIDEBAR - CONFIGURAÇÕES
# ============================================
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    st.markdown("---")
    
    # API Key Configuration
    if 'use_custom_key' not in st.session_state:
        st.session_state.use_custom_key = False
    if 'custom_api_key' not in st.session_state:
        st.session_state.custom_api_key = ""
    
    use_custom = st.checkbox(
        "🔑 Usar minha própria chave OpenAI",
        value=st.session_state.use_custom_key,
        help="Marque se quiser usar sua própria API key da OpenAI"
    )
    st.session_state.use_custom_key = use_custom
    
    if use_custom:
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=st.session_state.custom_api_key,
            placeholder="sk-...",
            help="Cole sua chave da OpenAI aqui"
        )
        st.session_state.custom_api_key = api_key
        
        if api_key:
            os.environ["CUSTOM_OPENAI_API_KEY"] = api_key
            st.success("✅ Chave configurada!")
        else:
            st.warning("⚠️ Insira sua API key")
    else:
        # Check for environment variable
        if os.environ.get("OPENAI_API_KEY"):
            st.success("✅ Usando chave do sistema")
        else:
            st.info("🤖 Configure sua API key para usar a IA")
    
    st.markdown("---")
    
    # Pix Configuration
    st.markdown("### 💳 Configuração Pix")
    pix_key_default = st.text_input(
        "Sua chave Pix padrão",
        value=os.environ.get("DEFAULT_PIX_KEY", ""),
        placeholder="seupix@email.com"
    )
    
    pix_nome = st.text_input(
        "Nome do recebedor",
        value=os.environ.get("DEFAULT_ORGANIZER_NAME", "Churrasqueiro"),
        placeholder="Seu nome"
    )
    
    pix_cidade = st.text_input(
        "Cidade",
        value="SAO PAULO",
        placeholder="Sua cidade"
    )
    
    st.markdown("---")
    
    # Histórico
    st.markdown("### 📜 Histórico")
    if st.session_state.historico_churrascos:
        st.write(f"🔥 {len(st.session_state.historico_churrascos)} churrascos salvos")
        if st.button("🗑️ Limpar histórico"):
            st.session_state.historico_churrascos = []
            st.rerun()
    else:
        st.caption("Nenhum churrasco salvo ainda")
    
    st.markdown("---")
    
    # About
    st.markdown("### 📌 Sobre")
    st.markdown("""
    **Churrasco.ai** organiza seu rolê:
    - 🥩 Calcula lista de compras
    - 💰 Divide a conta justa
    - 📱 QR Code Pix na hora
    - 🔥 Mensagens de cobrança
    """)
    st.markdown("---")
    st.caption("Feito com 🔥 no Brasil v2.0")

# ============================================
# HEADER PRINCIPAL
# ============================================
st.markdown("""
<div class="main-header">
    <div class="main-title">🥩 Churrasco.ai</div>
    <div class="subtitle">Organize o rolê sem burocracia, parça!</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# TABS PRINCIPAIS
# ============================================
tab1, tab2, tab3 = st.tabs(["🔥 Planejar o Rolê", "💰 Rachar a Conta", "📋 Templates"])

# ============================================
# TAB 1: PLANEJAR O ROLÊ
# ============================================
with tab1:
    st.markdown("### 📝 Conta pra gente como vai ser o churras!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        descricao = st.text_area(
            "Descreva o churrasco:",
            placeholder="Ex: Churrasco sábado às 13h pra 10 amigos, a galera bebe MUITO, vai durar umas 6 horas. Tem 2 vegetarianos e 1 criança.",
            height=150,
            help="Quanto mais detalhes, melhor a lista! Mencione: número de pessoas, duração, se bebem muito, homens/mulheres, restrições alimentares, etc."
        )
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>💡 Dicas para descrição:</h4>
            <ul style="color: #a0a0a0; font-size: 0.9rem;">
                <li>Número de pessoas</li>
                <li>Duração do evento</li>
                <li>Perfil (bebem muito?)</li>
                <li>Restrições alimentares</li>
                <li>Orçamento aproximado</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        calcular_btn = st.button("🤖 Calcular com IA", use_container_width=True, type="primary")
    
    if calcular_btn and descricao.strip():
        with st.spinner("🥩 Consultando o Mestre do Churrasco..."):
            try:
                from utils import gerar_lista_churrasco, salvar_historico_local
                resultado = gerar_lista_churrasco(descricao)
                st.session_state.lista_compras = resultado
                
                # Salvar no histórico
                historico_item = salvar_historico_local({
                    "tipo": "planejamento",
                    "descricao": descricao,
                    "resultado": resultado
                })
                st.session_state.historico_churrascos.append(historico_item)
                
            except Exception as e:
                st.error(f"❌ Ops! Deu ruim: {str(e)}")
    
    # Exibir resultado
    if st.session_state.lista_compras:
        lista = st.session_state.lista_compras
        
        st.markdown("---")
        
        # Resumo
        st.markdown(f"""
        <div class="premium-card">
            <h3>🎉 {lista.get('resumo', 'Lista pronta!')}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">👥 {lista.get('pessoas', 'N/A')}</div>
                <div class="metric-label">Pessoas</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">⏰ {lista.get('duracao_estimada', '4h')}</div>
                <div class="metric-label">Duração</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">🛒 {len(lista.get('carnes', [])) + len(lista.get('bebidas', [])) + len(lista.get('acompanhamentos', []))}</div>
                <div class="metric-label">Itens</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Categorias
        st.markdown('<div class="categoria-header">🥩 CARNES</div>', unsafe_allow_html=True)
        for item in lista.get('carnes', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        st.markdown('<div class="categoria-header categoria-header-blue">🍺 BEBIDAS</div>', unsafe_allow_html=True)
        for item in lista.get('bebidas', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                emoji = "🍺" if item.get('alcoolica') else "🥤"
                st.write(f"{emoji} **{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        st.markdown('<div class="categoria-header categoria-header-green">🥗 ACOMPANHAMENTOS</div>', unsafe_allow_html=True)
        for item in lista.get('acompanhamentos', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        st.markdown('<div class="categoria-header">🔥 CARVÃO & GELO</div>', unsafe_allow_html=True)
        for item in lista.get('carvao_gelo', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        # Total
        st.markdown(f"""
        <div class="total-card">
            <div class="total-label">💸 Total Estimado</div>
            <div class="total-value">R$ {lista.get('total_estimado', 0):.2f}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Dicas
        if lista.get('dicas'):
            st.markdown("### 💡 Dicas do Mestre")
            for dica in lista.get('dicas', []):
                st.markdown(f'<div class="dica-card">{dica}</div>', unsafe_allow_html=True)
        
        # Ações
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📋 Copiar Lista", use_container_width=True):
                lista_texto = "🛒 LISTA DE COMPRAS - CHURRASCO\n\n"
                lista_texto += "🥩 CARNES:\n"
                for item in lista.get('carnes', []):
                    lista_texto += f"  • {item['item']} - {item['quantidade']}\n"
                lista_texto += "\n🍺 BEBIDAS:\n"
                for item in lista.get('bebidas', []):
                    lista_texto += f"  • {item['item']} - {item['quantidade']}\n"
                st.code(lista_texto)
        
        with col2:
            if st.button("💾 Salvar Template", use_container_width=True):
                from utils import criar_template_churrasco
                template = criar_template_churrasco(f"Churras {datetime.now().strftime('%d/%m')}", lista)
                st.session_state.templates_salvos.append(template)
                st.success("✅ Template salvo!")
        
        with col3:
            if st.button("🗑️ Limpar Lista", use_container_width=True):
                st.session_state.lista_compras = None
                st.rerun()

# ============================================
# TAB 2: RACHAR A CONTA
# ============================================
with tab2:
    st.markdown("### 📸 Tire foto da notinha do mercado!")
    
    uploaded_file = st.file_uploader(
        "Upload da nota fiscal",
        type=['png', 'jpg', 'jpeg'],
        help="Pode ser foto do celular mesmo, não precisa ser perfeita!"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            image = Image.open(uploaded_file)
            st.image(image, caption="📄 Sua nota fiscal", use_container_width=True)
        
        with col2:
            st.markdown("""
            <div class="premium-card">
                <h4>🤖 O que vamos fazer:</h4>
                <ol style="color: #a0a0a0;">
                    <li>Ler todos os itens da nota</li>
                    <li>Separar bebidas alcoólicas</li>
                    <li>Calcular divisão justa</li>
                    <li>Gerar cobrança pro Zap</li>
                </ol>
            </div>
            """, unsafe_allow_html=True)
            
            processar_btn = st.button("🔍 Ler Nota com IA", use_container_width=True, type="primary")
        
        if processar_btn:
            with st.spinner("🤖 Lendo os itens da nota..."):
                try:
                    from utils import extrair_itens_nota
                    img_bytes = io.BytesIO()
                    image.save(img_bytes, format='JPEG')
                    resultado = extrair_itens_nota(img_bytes.getvalue())
                    
                    if 'erro' in resultado:
                        st.error(f"❌ {resultado['erro']}")
                    else:
                        st.session_state.itens_nota = resultado
                except Exception as e:
                    st.error(f"❌ Erro ao processar: {str(e)}")
    
    # Exibir itens extraídos
    if st.session_state.itens_nota and 'itens' in st.session_state.itens_nota:
        nota = st.session_state.itens_nota
        
        st.markdown("---")
        st.markdown("### 📋 Itens encontrados:")
        
        # Info do estabelecimento
        if nota.get('estabelecimento') or nota.get('data_compra'):
            col1, col2 = st.columns(2)
            with col1:
                if nota.get('estabelecimento'):
                    st.info(f"🏪 **{nota.get('estabelecimento')}**")
            with col2:
                if nota.get('data_compra'):
                    st.info(f"📅 {nota.get('data_compra')}")
        
        # Lista de itens
        for item in nota['itens']:
            emoji = "🍺" if item.get('alcoolica') else "🛒"
            st.markdown(f"""
            <div class="item-card">
                <span>{emoji} {item['nome']}</span>
                <span style="color: #38ef7d; font-weight: 600;">R$ {item['preco']:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("💰 Total Geral", f"R$ {nota.get('total_nota', sum(i['preco'] for i in nota['itens'])):.2f}")
        with col2:
            st.metric("🍺 Alcoólicos", f"R$ {nota.get('total_alcoolico', 0):.2f}")
        with col3:
            st.metric("🥤 Não-alcoólicos", f"R$ {nota.get('total_nao_alcoolico', 0):.2f}")
        
        st.markdown("---")
        st.markdown("### 👥 Quem participou do rolê?")
        
        nomes_input = st.text_input(
            "Digite os nomes separados por vírgula:",
            placeholder="João, Maria, Pedro, Ana",
            help="Lista todo mundo que tava no churrasco!"
        )
        
        if nomes_input:
            participantes = [nome.strip() for nome in nomes_input.split(',') if nome.strip()]
            st.session_state.participantes = participantes
            
            st.markdown("### 🍺 Quem bebeu álcool?")
            st.caption("Marque quem bebeu pra gente dividir certo!")
            
            quem_bebeu = []
            cols = st.columns(min(len(participantes), 4))
            for i, pessoa in enumerate(participantes):
                with cols[i % len(cols)]:
                    if st.checkbox(f"🍺 {pessoa}", key=f"bebeu_{pessoa}"):
                        quem_bebeu.append(pessoa)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                calcular_div_btn = st.button("💰 Calcular Divisão", use_container_width=True, type="primary")
            
            if calcular_div_btn:
                from utils import calcular_divisao
                divisao = calcular_divisao(nota['itens'], participantes, quem_bebeu)
                st.session_state.divisao = divisao
            
            # Exibir divisão
            if st.session_state.divisao:
                div = st.session_state.divisao
                
                st.markdown("---")
                st.markdown("### 💸 Divisão da Conta")
                
                st.markdown(f"""
                <div class="premium-card">
                    <h4>📊 Resumo:</h4>
                    <ul style="color: #e0e0e0;">
                        <li>Total Geral: <strong>R$ {div['total_geral']:.2f}</strong></li>
                        <li>Parte comum (todos pagam): <strong>R$ {div['valor_base_por_pessoa']:.2f}</strong> por pessoa</li>
                        <li>Bebidas alcoólicas: <strong>R$ {div['valor_alcool_por_bebedor']:.2f}</strong> (só quem bebeu)</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 👤 Valor por pessoa:")
                
                cols = st.columns(min(len(div['divisao']), 3))
                for i, (pessoa, valor) in enumerate(div['divisao'].items()):
                    bebeu = pessoa in quem_bebeu
                    with cols[i % len(cols)]:
                        classe = "pessoa-card pessoa-bebeu" if bebeu else "pessoa-card"
                        emoji = "🍺" if bebeu else "🥤"
                        extra = "<small>(inclui bebida)</small>" if bebeu else ""
                        st.markdown(f"""
                        <div class="{classe}">
                            <div class="pessoa-nome">{emoji} {pessoa}</div>
                            <div class="pessoa-valor">R$ {valor:.2f}</div>
                            {extra}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📱 Gerar Cobranças")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    pessoa_cobrar = st.selectbox(
                        "Escolha quem cobrar:",
                        options=list(div['divisao'].keys())
                    )
                
                with col2:
                    pix_cobranca = st.text_input(
                        "Sua chave Pix:",
                        value=pix_key_default or "seupix@email.com"
                    )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📩 Cobrança Normal", use_container_width=True):
                        with st.spinner("Gerando mensagem..."):
                            try:
                                msg = gerar_cobranca_whatsapp(
                                    pessoa_cobrar,
                                    div['divisao'][pessoa_cobrar],
                                    pix_key=pix_cobranca,
                                    bebeu=(pessoa_cobrar in quem_bebeu)
                                )
                                st.session_state.mensagens_cobranca[pessoa_cobrar] = msg
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")
                
                with col2:
                    if st.button("🔥 Cobrar Caloteiro!", use_container_width=True):
                        with st.spinner("Gerando zoeira..."):
                            try:
                                from utils import gerar_cobranca_caloteiro
                                msg = gerar_cobranca_caloteiro(
                                    pessoa_cobrar,
                                    div['divisao'][pessoa_cobrar]
                                )
                                st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_caloteiro"] = msg
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")
                
                with col3:
                    if st.button("📲 Gerar QR Pix", use_container_width=True):
                        try:
                            from utils import gerar_qrcode_pix, gerar_link_pix_copia_cola, HAS_QRCODE
                            valor_cobrar = div['divisao'][pessoa_cobrar]
                            
                            if HAS_QRCODE:
                                qr_bytes = gerar_qrcode_pix(
                                    pix_cobranca,
                                    pix_nome,
                                    pix_cidade,
                                    valor_cobrar,
                                    f"Churras-{pessoa_cobrar[:10]}"
                                )
                                if qr_bytes:
                                    st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_qr"] = qr_bytes
                            
                            pix_copia_cola = gerar_link_pix_copia_cola(
                                pix_cobranca,
                                pix_nome,
                                pix_cidade,
                                valor_cobrar,
                                f"Churras-{pessoa_cobrar[:10]}"
                            )
                            st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_pix"] = pix_copia_cola
                            
                        except Exception as e:
                            st.error(f"Erro ao gerar Pix: {str(e)}")
                
                # Exibir mensagens geradas
                if pessoa_cobrar in st.session_state.mensagens_cobranca:
                    st.markdown("#### 💬 Mensagem Normal:")
                    st.markdown(
                        f'<div class="whatsapp-msg">{st.session_state.mensagens_cobranca[pessoa_cobrar]}</div>',
                        unsafe_allow_html=True
                    )
                    st.code(st.session_state.mensagens_cobranca[pessoa_cobrar], language=None)
                
                if f"{pessoa_cobrar}_caloteiro" in st.session_state.mensagens_cobranca:
                    st.markdown("#### 🔥 Modo Caloteiro:")
                    st.markdown(
                        f'<div class="whatsapp-msg">{st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_caloteiro"]}</div>',
                        unsafe_allow_html=True
                    )
                    st.code(st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_caloteiro"], language=None)
                
                if f"{pessoa_cobrar}_qr" in st.session_state.mensagens_cobranca:
                    st.markdown("#### 📲 QR Code Pix:")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown('<div class="qrcode-container">', unsafe_allow_html=True)
                        st.image(st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_qr"], width=250)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                if f"{pessoa_cobrar}_pix" in st.session_state.mensagens_cobranca:
                    st.markdown("#### 📋 Pix Copia e Cola:")
                    st.code(st.session_state.mensagens_cobranca[f"{pessoa_cobrar}_pix"], language=None)

# ============================================
# TAB 3: TEMPLATES
# ============================================
with tab3:
    st.markdown("### 📋 Templates de Churrasco")
    st.caption("Use templates prontos ou crie os seus!")
    
    # Templates pré-definidos
    st.markdown("#### 🔥 Templates Populares")
    
    from utils import TEMPLATES_PADRAO
    
    cols = st.columns(4)
    template_icons = {"tradicional": "🥩", "premium": "👑", "economico": "💰", "vegetariano": "🥗"}
    
    for i, (key, template) in enumerate(TEMPLATES_PADRAO.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="template-card">
                <div class="template-icon">{template_icons.get(key, '🔥')}</div>
                <div class="template-name">{template['nome']}</div>
                <div class="template-desc">{template['descricao']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        template_escolhido = st.selectbox(
            "Escolha um template:",
            options=list(TEMPLATES_PADRAO.keys()),
            format_func=lambda x: TEMPLATES_PADRAO[x]['nome']
        )
    
    with col2:
        num_pessoas_template = st.number_input(
            "Número de pessoas:",
            min_value=1,
            max_value=100,
            value=10
        )
    
    if st.button("🚀 Aplicar Template", use_container_width=True):
        template = TEMPLATES_PADRAO[template_escolhido]
        
        # Gerar descrição baseada no template
        descricao_template = f"Churrasco {template['nome']} para {num_pessoas_template} pessoas."
        if template.get('carnes'):
            descricao_template += f" Carnes: {', '.join(template['carnes'][:3])}."
        
        st.success(f"✅ Template aplicado! Use a descrição abaixo na aba 'Planejar o Rolê':")
        st.code(descricao_template)
    
    # Templates salvos pelo usuário
    if st.session_state.templates_salvos:
        st.markdown("---")
        st.markdown("#### 💾 Seus Templates Salvos")
        
        for i, template in enumerate(st.session_state.templates_salvos):
            with st.expander(f"📋 {template['nome']}"):
                st.write(f"Criado em: {template['criado_em']}")
                st.write(f"Pessoas base: {template['pessoas_base']}")
                if st.button(f"🗑️ Remover", key=f"del_template_{i}"):
                    st.session_state.templates_salvos.pop(i)
                    st.rerun()

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>Feito com 🔥 para os churrasqueiros do Brasil</p>
    <p>Churrasco.ai v2.0 | <a href="https://github.com" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)

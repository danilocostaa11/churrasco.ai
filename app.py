import streamlit as st
from PIL import Image
import io
import os

st.set_page_config(
    page_title="Churrasco.ai 🥩",
    page_icon="🥩",
    layout="centered",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    st.markdown("---")
    
    if 'use_custom_key' not in st.session_state:
        st.session_state.use_custom_key = False
    if 'custom_api_key' not in st.session_state:
        st.session_state.custom_api_key = ""
    
    use_custom = st.checkbox(
        "Usar minha própria chave OpenAI",
        value=st.session_state.use_custom_key,
        help="Marque se quiser usar sua própria API key da OpenAI"
    )
    st.session_state.use_custom_key = use_custom
    
    if use_custom:
        api_key = st.text_input(
            "🔑 OpenAI API Key",
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
            st.warning("⚠️ Insira sua API key para continuar")
    else:
        st.info("🤖 Usando IA integrada do Replit (já inclusa nos seus créditos)")
    
    st.markdown("---")
    st.markdown("### 📌 Sobre")
    st.markdown("""
    **Churrasco.ai** organiza seu rolê:
    - 🥩 Calcula lista de compras
    - 💰 Divide a conta justa
    - 📱 Gera cobrança pro Zap
    """)
    st.markdown("---")
    st.caption("Feito com 🔥 no Brasil")

st.markdown("""
<style>
    .stApp {
        max-width: 100%;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-top: 0;
    }
    .categoria-header {
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        margin: 16px 0 8px 0;
    }
    .item-card {
        background: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        margin: 4px 0;
        border-left: 4px solid #ff6b35;
    }
    .total-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        font-size: 1.5rem;
        margin: 20px 0;
    }
    .pessoa-card {
        background: #e8f4ea;
        padding: 16px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 5px solid #28a745;
    }
    .pessoa-bebeu {
        background: #fff3cd;
        border-left-color: #ffc107;
    }
    .whatsapp-msg {
        background: #dcf8c6;
        padding: 16px;
        border-radius: 12px;
        font-family: 'Segoe UI', sans-serif;
        margin: 12px 0;
        white-space: pre-wrap;
    }
</style>
""", unsafe_allow_html=True)

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

st.markdown('<h1 class="main-title">🥩 Churrasco.ai</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Organize o rolê sem burocracia, parça!</p>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2 = st.tabs(["🔥 Planejar o Rolê", "💰 Rachar a Conta"])

with tab1:
    st.markdown("### 📝 Conta pra gente como vai ser o churras!")
    
    descricao = st.text_area(
        "Descreva o churrasco:",
        placeholder="Ex: Churrasco sábado às 13h pra 10 amigos, a galera bebe MUITO, vai durar umas 6 horas. Tem 2 vegetarianos.",
        height=120,
        help="Quanto mais detalhes, melhor a lista! Mencione: número de pessoas, duração, se bebem muito, homens/mulheres, etc."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        calcular_btn = st.button("🤖 Calcular com IA", use_container_width=True, type="primary")
    
    if calcular_btn and descricao.strip():
        with st.spinner("🥩 Consultando o Mestre do Churrasco..."):
            try:
                from utils import gerar_lista_churrasco
                resultado = gerar_lista_churrasco(descricao)
                st.session_state.lista_compras = resultado
            except Exception as e:
                st.error(f"❌ Ops! Deu ruim: {str(e)}")
    
    if st.session_state.lista_compras:
        lista = st.session_state.lista_compras
        
        st.markdown("---")
        st.markdown(f"### 🎉 {lista.get('resumo', 'Lista pronta!')}")
        st.info(f"👥 **Pessoas estimadas:** {lista.get('pessoas', 'N/A')}")
        
        st.markdown('<div class="categoria-header">🥩 CARNES</div>', unsafe_allow_html=True)
        for item in lista.get('carnes', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        st.markdown('<div class="categoria-header">🍺 BEBIDAS</div>', unsafe_allow_html=True)
        for item in lista.get('bebidas', []):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                emoji = "🍺" if item.get('alcoolica') else "🥤"
                st.write(f"{emoji} **{item['item']}**")
            with col2:
                st.write(item['quantidade'])
            with col3:
                st.write(f"R$ {item['preco_estimado']:.2f}")
        
        st.markdown('<div class="categoria-header">🥗 ACOMPANHAMENTOS</div>', unsafe_allow_html=True)
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
        
        st.markdown(
            f'<div class="total-card">💸 Total Estimado: R$ {lista.get("total_estimado", 0):.2f}</div>',
            unsafe_allow_html=True
        )
        
        if st.button("🗑️ Limpar Lista", use_container_width=True):
            st.session_state.lista_compras = None
            st.rerun()

with tab2:
    st.markdown("### 📸 Tire foto da notinha do mercado!")
    
    uploaded_file = st.file_uploader(
        "Upload da nota fiscal",
        type=['png', 'jpg', 'jpeg'],
        help="Pode ser foto do celular mesmo, não precisa ser perfeita!"
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📄 Sua nota fiscal", use_container_width=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
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
    
    if st.session_state.itens_nota and 'itens' in st.session_state.itens_nota:
        nota = st.session_state.itens_nota
        
        st.markdown("---")
        st.markdown("### 📋 Itens encontrados:")
        
        for item in nota['itens']:
            emoji = "🍺" if item.get('alcoolica') else "🛒"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{emoji} {item['nome']}")
            with col2:
                st.write(f"R$ {item['preco']:.2f}")
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Geral", f"R$ {nota.get('total_nota', sum(i['preco'] for i in nota['itens'])):.2f}")
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
            cols = st.columns(2)
            for i, pessoa in enumerate(participantes):
                with cols[i % 2]:
                    if st.checkbox(f"🍺 {pessoa}", key=f"bebeu_{pessoa}"):
                        quem_bebeu.append(pessoa)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                calcular_div_btn = st.button("💰 Calcular Divisão", use_container_width=True, type="primary")
            
            if calcular_div_btn:
                from utils import calcular_divisao
                divisao = calcular_divisao(nota['itens'], participantes, quem_bebeu)
                st.session_state.divisao = divisao
            
            if st.session_state.divisao:
                div = st.session_state.divisao
                
                st.markdown("---")
                st.markdown("### 💸 Divisão da Conta")
                
                st.info(f"""
                📊 **Resumo:**
                - Total Geral: **R$ {div['total_geral']:.2f}**
                - Parte comum (todos pagam): **R$ {div['valor_base_por_pessoa']:.2f}** por pessoa
                - Bebidas alcoólicas: **R$ {div['valor_alcool_por_bebedor']:.2f}** (só quem bebeu)
                """)
                
                st.markdown("### 👤 Valor por pessoa:")
                
                for pessoa, valor in div['divisao'].items():
                    bebeu = pessoa in quem_bebeu
                    emoji = "🍺" if bebeu else "🥤"
                    classe = "pessoa-card pessoa-bebeu" if bebeu else "pessoa-card"
                    
                    st.markdown(f"""
                    <div class="{classe}">
                        <strong>{emoji} {pessoa}</strong><br>
                        <span style="font-size: 1.3rem; color: #28a745;">R$ {valor:.2f}</span>
                        {"<br><small>(inclui bebida alcoólica)</small>" if bebeu else ""}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown("### 📱 Gerar Cobranças pro WhatsApp")
                
                pix_key = st.text_input(
                    "Sua chave Pix:",
                    value="seupix@email.com",
                    help="A chave vai aparecer na mensagem de cobrança"
                )
                
                pessoa_cobrar = st.selectbox(
                    "Escolha quem cobrar:",
                    options=list(div['divisao'].keys())
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📩 Gerar Cobrança Normal", use_container_width=True):
                        with st.spinner("Gerando mensagem..."):
                            try:
                                from utils import gerar_cobranca_whatsapp
                                msg = gerar_cobranca_whatsapp(
                                    pessoa_cobrar,
                                    div['divisao'][pessoa_cobrar],
                                    pix_key=pix_key
                                )
                                st.session_state.mensagens_cobranca[pessoa_cobrar] = msg
                            except Exception as e:
                                st.error(f"Erro: {str(e)}")
                
                with col2:
                    if st.button("🔥 Cobrar Caloteiro!", use_container_width=True, type="secondary"):
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

st.markdown("---")
st.markdown(
    '<p style="text-align: center; color: #888; font-size: 0.9rem;">Feito com 🔥 para os churrasqueiros do Brasil</p>',
    unsafe_allow_html=True
)

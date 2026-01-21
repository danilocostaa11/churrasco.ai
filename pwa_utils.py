import streamlit as st
import json
import base64

def get_pwa_manifest():
    """Retorna o manifesto PWA em formato JSON."""
    return {
        "name": "Churrasco.ai",
        "short_name": "Churrasco",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0E1117",
        "theme_color": "#FF4B4B",
        "orientation": "portrait",
        "icons": [
            {
                "src": "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f969.png",
                "sizes": "72x72",
                "type": "image/png"
            },
            {
                "src": "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f969.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": "https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f969.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ]
    }

def setup_pwa():
    """Injeta as meta tags e scripts necessários para PWA."""
    
    # Gerar Manifesto como Data URI (base64)
    manifest_json = json.dumps(get_pwa_manifest())
    manifest_b64 = base64.b64encode(manifest_json.encode()).decode()
    manifest_href = f"data:application/manifest+json;base64,{manifest_b64}"
    
    # HTML para injetar
    # Meta tags para mobile (Apple Touch Icon + Viewport + Theme Color)
    pwa_html = f"""
    <link rel="manifest" href="{manifest_href}" crossorigin="use-credentials">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme_color" content="#0E1117">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, minimal-ui">
    <link rel="apple-touch-icon" href="https://cdn.jsdelivr.net/gh/twitter/twemoji@14.0.2/assets/72x72/1f969.png">
    
    <script>
        // Forçar atualização do manifesto se necessário
        console.log("🍖 Churrasco.ai PWA Active");
    </script>
    <style>
        /* Ajustes Mobile Específicos */
        @media only screen and (max-width: 600px) {{
            .stApp {{
                padding-top: 1rem;
            }}
            .main-header {{
                padding: 1.5rem 0.5rem;
                margin-bottom: 1rem;
            }}
            .main-title {{
                font-size: 2.5rem !important;
            }}
            .premium-card {{
                padding: 1rem;
            }}
            /* Melhorar toque em botões no mobile */
            button {{
                min-height: 44px;
            }}
        }}
    </style>
    """
    
    # Injetar no head/body
    st.markdown(pwa_html, unsafe_allow_html=True)

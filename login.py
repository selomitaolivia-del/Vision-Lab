import streamlit as st
import base64
import os

def get_base64_image(image_filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, image_filename)
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

def show_login():
    bg_base64 = get_base64_image("background.jpg")
    
    if bg_base64:
        bg_style = f"""
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.55)), 
                        url(data:image/jpeg;base64,{bg_base64}) !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            overflow: hidden !important;
        }}
        """
    else:
        # Fallback to beautiful red-black gradient if image is missing
        bg_style = """
        .stApp {
            background: radial-gradient(circle at 50% 50%, #200202 0%, #050000 100%) !important;
            overflow: hidden !important;
        }
        """

    html_content = """
    <!-- Load modern Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">

    <style>
    /* ── BASE & GLOBAL SETTINGS ── */
    html, body, [data-testid="stAppViewContainer"], .block-container, input, button {
        font-family: 'Outfit', sans-serif !important;
    }

    __BG_STYLE_PLACEHOLDER__

    #MainMenu, header, footer { visibility: hidden; }

    /* Sakura / Sparkle Floating Background canvas */
    #flowerCanvas {
        position: fixed; top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none; z-index: 1;
    }

    /* ── VERTICAL & HORIZONTAL CENTERING ── */
    .stAppViewContainer {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        background: transparent !important;
    }

    .stMain {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
        width: 100% !important;
    }

    /* ── GLASS CARD CONTAINER (Overriding Streamlit's block-container) ── */
    .block-container {
        position: relative !important;
        z-index: 2 !important;
        background: rgba(25, 3, 3, 0.6) !important;
        backdrop-filter: blur(28px) !important;
        -webkit-backdrop-filter: blur(28px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 48px 38px 40px 38px !important;
        border-radius: 24px !important;
        max-width: 430px !important;
        margin: auto !important;
        box-shadow:
            0 24px 50px rgba(0, 0, 0, 0.85),
            0 0 65px rgba(180, 0, 0, 0.22),
            inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    }

    /* ── TITLE & HEADINGS ── */
    .title {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 38px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
        letter-spacing: 2px;
        text-shadow: 0 0 25px rgba(255, 50, 50, 0.4);
        text-align: center;
    }

    .subtitle {
        font-size: 11px;
        color: #ff8080;
        margin-bottom: 22px;
        letter-spacing: 3.5px;
        text-transform: uppercase;
        font-weight: 600;
        text-align: center;
        opacity: 0.85;
    }

    .divider {
        width: 60px;
        height: 2.5px;
        background: linear-gradient(90deg, transparent, #ff3333, transparent);
        margin: -10px auto 25px auto;
        border-radius: 2px;
    }

    /* ── INPUT LABELS WITH ICONS ── */
    .input-label {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        color: #ffa3a3;
        letter-spacing: 2px;
        font-weight: 700;
        text-transform: uppercase;
        margin-top: 14px;
        margin-bottom: 8px;
        padding-left: 2px;
    }

    .input-label svg {
        width: 14px;
        height: 14px;
        fill: #ff4444;
        flex-shrink: 0;
    }

    /* ── TEXT INPUTS OVERRIDES (STREAMLIT) ── */
    /* Target the outermost container wrapper to style the whole box white */
    div[data-testid="stTextInputRootElement"],
    div[data-baseweb="input"],
    div.stTextInput > div {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        height: 46px !important;
    }

    div[data-testid="stTextInputRootElement"]:hover,
    div[data-baseweb="input"]:hover {
        background-color: #ffffff !important;
        border-color: rgba(255, 50, 50, 0.5) !important;
    }

    div[data-testid="stTextInputRootElement"]:focus-within,
    div[data-baseweb="input"]:focus-within {
        background-color: #ffffff !important;
        border-color: #ff3333 !important;
        box-shadow: 
            0 0 0 3px rgba(255, 51, 51, 0.22),
            0 0 15px rgba(255, 51, 51, 0.15) !important;
    }

    /* CRITICAL: Force Typed Text to be solid dark burgundy/black for perfect contrast on white fields */
    input, select, textarea,
    div[data-testid="stTextInputRootElement"] input,
    div[data-baseweb="input"] input,
    div.stTextInput input {
        color: #1a0202 !important;
        -webkit-text-fill-color: #1a0202 !important;
        background: transparent !important; /* CRITICAL: keep input background transparent so the wrapper's white shows through! */
        border: none !important;
        font-size: 14.5px !important;
        padding: 0 14px !important;
        height: 100% !important;
        width: 100% !important;
        box-shadow: none !important;
    }

    /* Placeholder Text - dark grey for white background */
    input::placeholder,
    div[data-testid="stTextInputRootElement"] input::placeholder,
    div[data-baseweb="input"] input::placeholder,
    div.stTextInput input::placeholder {
        color: rgba(26, 2, 2, 0.45) !important;
    }

    /* Style the eye adornment button on the password field to be clean & transparent */
    div[data-testid="stTextInputAdornment"],
    button[data-testid="stTextInputAdornmentButton"],
    div[data-testid="stTextInputAdornment"] button {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        height: 100% !important;
        padding-right: 8px !important;
    }

    div[data-testid="stTextInputAdornment"] svg {
        fill: #444444 !important;
        color: #444444 !important;
    }

    /* ── BUTTON STYLING (STREAMLIT) ── */
    div.stButton {
        margin-top: 24px !important;
        text-align: center;
    }

    .stButton > button {
        background: linear-gradient(135deg, #a30000, #e60000) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 100, 100, 0.2) !important;
        border-radius: 10px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 2px !important;
        width: 100% !important;
        height: 46px !important;
        padding: 0 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 5px 18px rgba(163, 0, 0, 0.3) !important;
        text-transform: uppercase;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #e60000, #ff3333) !important;
        box-shadow: 0 7px 22px rgba(230, 0, 0, 0.45) !important;
        transform: translateY(-1.5px) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 3px 12px rgba(230, 0, 0, 0.25) !important;
    }

    /* ── ALERT & ERROR STYLING ── */
    div[data-testid="stAlert"] {
        margin-top: 16px !important;
        border-radius: 10px !important;
        background-color: rgba(50, 4, 4, 0.75) !important;
        border: 1px solid rgba(255, 68, 68, 0.25) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }
    
    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span {
        color: #ffcccc !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        font-family: 'Outfit', sans-serif !important;
    }
    </style>

    <canvas id="flowerCanvas"></canvas>

    <!-- TITLE & SUBTITLE IN THE CARD -->
    <div class="title">VISION LAB</div>
    <div class="subtitle">IMAGE PROCESSING PLAYGROUND</div>
    <div class="divider"></div>

    <script>
    (function() {
        function init() {
            const canvas = document.getElementById('flowerCanvas');
            if (!canvas) { setTimeout(init, 50); return; }
            const ctx = canvas.getContext('2d');

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }
            resize();
            window.addEventListener('resize', resize);

            const COLORS = [
                { base: '#800000', dark: '#4d0000' },
                { base: '#b30000', dark: '#800000' },
                { base: '#ff4d4d', dark: '#cc0000' }
            ];

            let mouse = { x: -1000, y: -1000, vx: 0, vy: 0 };
            let lastMouse = { x: 0, y: 0 };
            let mouseActive = false;

            class SakuraParticle {
                constructor(x=null, y=null, forcedType=null, fromMouse=false) {
                    this.reset(true, x, y, forcedType, fromMouse);
                }
                reset(initial=false, x=null, y=null, forcedType=null, fromMouse=false) {
                    this.x = x !== null ? x : Math.random() * canvas.width;
                    this.y = y !== null ? y : (initial ? Math.random() * -canvas.height : -20);
                    const r = Math.random();
                    this.type = forcedType || (r < 0.65 ? 'petal' : r < 0.82 ? 'flower' : 'sparkle');
                    this.size = this.type === 'petal' ? Math.random()*5+4 : this.type === 'flower' ? Math.random()*6+6 : Math.random()*2+1;
                    this.speedY = fromMouse ? Math.random()*1.5-0.5 : this.type==='sparkle' ? Math.random()*0.4+0.2 : Math.random()*1.0+0.6;
                    this.speedX = fromMouse ? Math.random()*2-1 : this.type==='sparkle' ? Math.random()*0.3-0.15 : Math.random()*0.5+0.1;
                    this.rotation = Math.random()*Math.PI*2;
                    this.rotSpeed = (Math.random()-0.5)*0.02;
                    this.flip = Math.random()*Math.PI;
                    this.flipSpeed = Math.random()*0.04+0.01;
                    const c = COLORS[Math.floor(Math.random()*COLORS.length)];
                    this.colorBase = c.base; this.colorDark = c.dark;
                    this.alpha = this.type==='sparkle' ? Math.random()*0.7+0.3 : Math.random()*0.65+0.25;
                    this.pulse = Math.random()*Math.PI;
                    this.pulseSpeed = Math.random()*0.05+0.02;
                }
                update() {
                    if (mouseActive) {
                        let dx=this.x-mouse.x, dy=this.y-mouse.y;
                        let dist=Math.sqrt(dx*dx+dy*dy);
                        if (dist<120) {
                            let force=(120-dist)/120;
                            let angle=Math.atan2(dy,dx);
                            this.x+=Math.cos(angle)*force*1.8+mouse.vx*force*0.25;
                            this.y+=Math.sin(angle)*force*1.8+mouse.vy*force*0.25;
                        }
                    }
                    this.y+=this.speedY;
                    this.x+=this.speedX+Math.sin(this.y*0.015)*0.25;
                    this.rotation+=this.rotSpeed;
                    this.flip+=this.flipSpeed;
                    this.pulse+=this.pulseSpeed;
                    if (this.y>canvas.height+20||this.x>canvas.width+20||this.x<-20) this.reset(false);
                }
                draw() {
                    ctx.save();
                    ctx.globalAlpha=this.alpha;
                    ctx.translate(this.x,this.y);
                    ctx.rotate(this.rotation);
                    if (this.type==='petal') {
                        ctx.scale(Math.cos(this.flip),1);
                        let g=ctx.createLinearGradient(0,-this.size,0,this.size);
                        g.addColorStop(0,this.colorBase); g.addColorStop(1,this.colorDark);
                        ctx.fillStyle=g;
                        ctx.beginPath();
                        ctx.moveTo(0,this.size);
                        ctx.bezierCurveTo(-this.size,this.size*0.3,-this.size*0.8,-this.size*0.8,0,-this.size);
                        ctx.bezierCurveTo(this.size*0.8,-this.size*0.8,this.size,this.size*0.3,0,this.size);
                        ctx.closePath(); ctx.fill();
                    } else if (this.type==='flower') {
                        ctx.scale(Math.cos(this.flip*0.3),1);
                        for (let i=0;i<5;i++) {
                            ctx.save(); ctx.rotate(i*Math.PI*2/5);
                            let g=ctx.createLinearGradient(0,-this.size,0,0);
                            g.addColorStop(0,this.colorBase); g.addColorStop(1,this.colorDark);
                            ctx.fillStyle=g;
                            ctx.beginPath(); ctx.moveTo(0,0);
                            ctx.bezierCurveTo(-this.size*0.5,-this.size*0.4,-this.size*0.4,-this.size*1.1,0,-this.size);
                            ctx.bezierCurveTo(this.size*0.4,-this.size*1.1,this.size*0.5,-this.size*0.4,0,0);
                            ctx.closePath(); ctx.fill(); ctx.restore();
                        }
                    } else {
                        ctx.globalAlpha=Math.abs(Math.sin(this.pulse))*this.alpha;
                        let g=ctx.createRadialGradient(0,0,0,0,0,this.size*2.2);
                        g.addColorStop(0,'#ffffff'); g.addColorStop(0.3,'#ff8080'); g.addColorStop(1,'rgba(255,100,100,0)');
                        ctx.fillStyle=g;
                        ctx.beginPath(); ctx.arc(0,0,this.size*2.2,0,Math.PI*2); ctx.fill();
                    }
                    ctx.restore();
                }
            }

            const particles = Array.from({length:85}, ()=>new SakuraParticle());

            window.addEventListener('mousemove', e=>{
                mouse.x=e.clientX; mouse.y=e.clientY;
                if (mouseActive) { mouse.vx=mouse.x-lastMouse.x; mouse.vy=mouse.y-lastMouse.y; }
                mouseActive=true;
                lastMouse.x=mouse.x; lastMouse.y=mouse.y;
                if (Math.random()<0.35) particles.push(new SakuraParticle(mouse.x,mouse.y,'sparkle',true));
            });

            function animate() {
                ctx.clearRect(0,0,canvas.width,canvas.height);
                if (mouseActive) { mouse.vx*=0.94; mouse.vy*=0.94; }
                if (particles.length>150) particles.splice(85,particles.length-85);
                particles.forEach(p=>{p.update();p.draw();});
                window.sakuraAnimationId=requestAnimationFrame(animate);
            }
            if (window.sakuraAnimationId) cancelAnimationFrame(window.sakuraAnimationId);
            animate();
        }
        init();
    })();
    </script>
    """
    
    # Safely substitute the dynamic bg_style in a way that doesn't trigger python f-string errors
    final_html = html_content.replace("__BG_STYLE_PLACEHOLDER__", bg_style)
    st.markdown(final_html, unsafe_allow_html=True)

    # ── Field Nama Label ──
    st.markdown("""
    <div class="input-label">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
        </svg>
        Nama Lengkap
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input(
    "Nama",
    placeholder="Masukkan nama Anda...",
    label_visibility="collapsed",
    key="login_name"
)

    # ── Field Password Label ──
    st.markdown("""
    <div class="input-label">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M18 8h-1V6c0-2.8-2.2-5-5-5S7 3.2 7 6v2H6c-1.1 0-2 .9-2 2v10
                     c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9
                     c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6
                     c0-1.7 1.4-3.1 3.1-3.1 1.7 0 3.1 1.4 3.1 3.1v2z"/>
        </svg>
        Password
    </div>
    """, unsafe_allow_html=True)

    # ── Field Password Input ──
    password = st.text_input(
        "password",
        placeholder="Masukkan password...",
        type="password",
        label_visibility="collapsed",
        key="login_password")
        
          # ── Tombol Login & Logic ──
    if st.button("LOGIN", use_container_width=True):
        if name.strip() == "":
            st.error("⚠ Nama tidak boleh kosong.")
        elif password.strip() == "":
            st.error("⚠ Password tidak boleh kosong.")
        else:
            st.session_state.name = name
            st.session_state.user = name
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
    
            st.rerun()
          
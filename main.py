from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from unidecode import unidecode

app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

perfil = {
    "anos_carreira_dados": 5,
    "empresa_atual": "Sulamérica",
    "ex_empresa": "Terceiro no Banco Santander - Time de Recuperação de Crédito",
    "trajetoria": "Iniciei minha carreira como Estagiário no PagBank PagSeguro, onde fiquei 2 anos. Após isso, entrei como terceiro no Banco Santander no time de recuperação de crédito. Recebi uma proposta estratégica da SulAmérica e decidi dar o próximo passo entrando em uma das maiores seguradoras do país.",
    "cargo": "Analista de Dados Pleno",
    "especialidades": "Power BI, SQL, Python, PySpark",
    "projeto_destaque": "Automação de DRE Financeira integrando Power Query com banco de dados",
    "area_atual": "Análise de sinistros e dados estratégicos"
}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Thiago AI</title>
        <style>
            body {
                background: linear-gradient(135deg, #e0f2ff, #f8fbff);
                font-family: Arial, sans-serif;
                margin: 0;
            }

            .container {
                max-width: 850px;
                margin: 40px auto;
                padding: 20px;
            }

            h1 {
                color: #1e3a8a;
            }

            #chat {
                background: white;
                border-radius: 16px;
                padding: 20px;
                height: 500px;
                overflow-y: auto;
                box-shadow: 0 8px 30px rgba(0,0,0,0.1);
                margin-bottom: 15px;
            }

            .mensagem {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 14px;
                max-width: 70%;
                line-height: 1.5;
                animation: fadeIn 0.3s ease-in-out;
            }

            .usuario {
                background-color: #2563eb;
                color: white;
                margin-left: auto;
            }

            .bot {
                background-color: #e0e7ff;
                color: #1e3a8a;
                margin-right: auto;
            }

            .input-area {
                display: flex;
                gap: 10px;
            }

            input {
                flex: 1;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid #cbd5e1;
                font-size: 16px;
            }

            button {
                padding: 12px 18px;
                border-radius: 10px;
                border: none;
                cursor: pointer;
                font-weight: bold;
                transition: 0.2s;
            }

            .btn-enviar {
                background-color: #2563eb;
                color: white;
            }

            .btn-enviar:hover {
                background-color: #1e40af;
            }

            .sugestoes {
                margin-top: 20px;
            }

            .sugestoes button {
                background-color: #3b82f6;
                color: white;
                margin: 5px 5px 0 0;
            }

            .sugestoes button:hover {
                background-color: #1d4ed8;
            }

            .dots span {
                animation: blink 1.4s infinite both;
            }

            .dots span:nth-child(2) {
                animation-delay: .2s;
            }

            .dots span:nth-child(3) {
                animation-delay: .4s;
            }

            @keyframes blink {
                0% { opacity: .2; }
                20% { opacity: 1; }
                100% { opacity: .2; }
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(5px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>Thiago AI</h1>
            <div id="chat"></div>

            <div class="input-area">
                <input type="text" id="pergunta" placeholder="Digite sua pergunta..."
                    onkeydown="if(event.key==='Enter') enviarPergunta()"/>
                <button class="btn-enviar" onclick="enviarPergunta()">Enviar</button>
            </div>

            <div class="sugestoes">
                <br><strong>Sugestões:</strong><br>
                <button onclick="copiarSugestao(this)">Quais são suas habilidades?</button>
                <button onclick="copiarSugestao(this)">Qual foi seu projeto mais impactante?</button>
                <button onclick="copiarSugestao(this)">Conte sua trajetória profissional</button>
                <button onclick="copiarSugestao(this)">Onde você trabalha atualmente?</button>
                <button onclick="copiarSugestao(this)">Qual seu foco hoje?</button>
            </div>
        </div>

<script>
async function enviarPergunta() {
    const perguntaInput = document.getElementById("pergunta");
    const chat = document.getElementById("chat");
    const pergunta = perguntaInput.value.trim();
    if (!pergunta) return;

    adicionarMensagem(pergunta, "usuario");
    perguntaInput.value = "";

    mostrarPensando();

    const response = await fetch("/perguntar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pergunta: pergunta })
    });

    const data = await response.json();

    setTimeout(() => {
        removerPensando();
        escreverDevagar(data.resposta);
    }, 4000);
}

function adicionarMensagem(texto, tipo) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.classList.add("mensagem", tipo);
    div.innerText = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function escreverDevagar(texto) {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.classList.add("mensagem", "bot");
    chat.appendChild(div);

    let i = 0;

    function digitar() {
        if (i < texto.length) {
            div.innerHTML += texto.charAt(i);
            i++;
            chat.scrollTop = chat.scrollHeight;
            setTimeout(digitar, 45);
        }
    }

    digitar();
}

function mostrarPensando() {
    const chat = document.getElementById("chat");
    const div = document.createElement("div");
    div.classList.add("mensagem", "bot");
    div.id = "pensando";

    div.innerHTML = `
        <span>Pensando</span>
        <span class="dots">
            <span>.</span><span>.</span><span>.</span>
        </span>
    `;

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function removerPensando() {
    const pensando = document.getElementById("pensando");
    if (pensando) pensando.remove();
}

function copiarSugestao(botao) {
    document.getElementById("pergunta").value = botao.innerText;
    document.getElementById("pergunta").focus();
}
</script>

    </body>
    </html>
    """

@app.post("/perguntar")
def responder(dados: Pergunta):
    pergunta = unidecode(dados.pergunta.lower())
    
# @app.post("/perguntar")
# def responder(dados: Pergunta):
#     return {"resposta": "Teste funcionando perfeitamente"}

    palavras_chave = {
        "experiencia": ["anos", "experiencia", "tempo de carreira"],
        "trajetoria": ["trajetoria", "carreira", "comecou", "historia"],
        "projeto": ["projeto", "impactante", "resultado"],
        "habilidades": ["habilidades", "especialidades", "tecnologias", "stack", "ferramentas", "competencias"],
        "empresa": ["empresa", "onde trabalha", "onde atua"],
        "cargo": ["cargo", "posicao"],
        "foco": ["foco", "atualmente", "area atual"],
        "empresas_passadas": ["pagbank", "santander", "sulamerica"]
    }

    def contem(lista):
        return any(p in pergunta for p in lista)

    if contem(palavras_chave["experiencia"]):
        return {"resposta": f"Thiago possui mais de {perfil['anos_carreira_dados']} anos de experiência sólida na área de dados."}

    if contem(palavras_chave["trajetoria"]):
        return {"resposta": perfil["trajetoria"]}

    if contem(palavras_chave["projeto"]):
        return {"resposta": f"Um dos projetos mais estratégicos foi: {perfil['projeto_destaque']}."}

    if contem(palavras_chave["habilidades"]):
        return {"resposta": f"As principais habilidades são: {perfil['especialidades']}."}

    if contem(palavras_chave["empresa"]):
        return {"resposta": f"Atualmente é {perfil['cargo']} na {perfil['empresa_atual']}. Anteriormente atuou no {perfil['ex_empresa']}."}

    if contem(palavras_chave["cargo"]):
        return {"resposta": f"Atua como {perfil['cargo']} com foco em {perfil['area_atual']}."}

    if contem(palavras_chave["foco"]):
        return {"resposta": f"Hoje está focado em {perfil['area_atual']} e evoluindo para projetos com Inteligência Artificial."}

    if contem(palavras_chave["empresas_passadas"]):
        return {"resposta": perfil["trajetoria"]}

    return {"resposta": "Pergunta não encontrada no banco estratégico de Thiago. Reformule a pergunta."}
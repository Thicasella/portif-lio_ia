from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

perfil = {
    "anos_carreira_dados": 5,
    "empresa": "Sulamerica",
    "Ex-empresa": "Terceiro no banco santander, onde trabalhei no time de recuperação de crédito",
    "trajetória": "Iniciei minha carreira como Estágiario na empresa Pagbank Pagseguros, onde fiquei 2 anos como estágiario, pós pagbank entrei como terceiro no banco santander no time de recupeção de crédito. acabei rebendo uma boa propósta da sulamérica pós alguns meses dentro do santander e decidi por ser terceiro dar esse passo de entra em uma das maiores seguradoras do país",
    "cargo": "Analista de Dados Pleno",
    "especialidades": "Power BI, SQL, Python, PySpark",
    "mba": "Tecnologia para Negócios: AI, Data Science e Big Data",
    "projeto_destaque": "Automação de DRE Financeira integrando Power Query com banco de dados",
    "area_atual": "Análise de sinistros e dados estratégicos"
}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Thiago AI Terminal</title>
            <style>
                body {
                    background-color: black;
                    color: #00ff00;
                    font-family: monospace;
                    padding: 40px;
                }
                input {
                    background-color: black;
                    color: #00ff00;
                    border: none;
                    outline: none;
                    font-family: monospace;
                    font-size: 18px;
                    width: 100%;
                }
                button {
                    background: black;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    margin-top: 10px;
                    padding: 5px 10px;
                    cursor: pointer;
                }
                #resposta {
                    margin-top: 20px;
                    white-space: pre-wrap;
                }
                .sugestoes {
                    margin-top: 30px;
                    font-size: 14px;
                }
            </style>
        </head>
        <body>

            <div>> O que você deseja saber sobre Thiago?</div>
            <br>
            <input type="text" id="pergunta" autofocus 
                onkeydown="if(event.key==='Enter') enviarPergunta()"/>
            <br>
            <button onclick="enviarPergunta()">Perguntar</button>
            <button onclick="novaPergunta()">Nova Pergunta</button>

            <div id="resposta"></div>

            <div class="sugestoes">
                <br>> Sugestões de perguntas:
                <br>- Quantos anos de carreira você tem?
                <br>- Qual foi seu projeto mais impactante?
                <br>- Com quais tecnologias você trabalha?
                <br>- Onde você trabalhou?
                <br>- Qual seu foco atual?
                <br>- O que você está estudando atualmente?
                 <br>- Qual é a sua trajetória profissional?
            </div>

            <script>
                async function enviarPergunta() {
                    const perguntaInput = document.getElementById("pergunta");
                    const respostaDiv = document.getElementById("resposta");

                    const pergunta = perguntaInput.value;
                    respostaDiv.innerHTML = "";

                    const response = await fetch("/perguntar", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ pergunta: pergunta })
                    });

                    const data = await response.json();
                    escreverDevagar(data.resposta);
                }

                function escreverDevagar(texto) {
                    const respostaDiv = document.getElementById("resposta");
                    let i = 0;
                    respostaDiv.innerHTML = "";

                    function digitar() {
                        if (i < texto.length) {
                            respostaDiv.innerHTML += texto.charAt(i);
                            i++;
                            setTimeout(digitar, 35);
                        }
                    }

                    digitar();
                }

                function novaPergunta() {
                    document.getElementById("pergunta").value = "";
                    document.getElementById("resposta").innerHTML = "";
                }
            </script>

        </body>
    </html>
    """

@app.post("/perguntar")
def responder(dados: Pergunta):
    pergunta = dados.pergunta.lower()

    if "anos" in pergunta or "experiência" in pergunta:
        return {
            "resposta": f"Thiago possui mais de {perfil['anos_carreira_dados']} anos de experiência sólida na área de dados."
        }

    if "trajetória" in pergunta or "carreira" in pergunta or "começou" in pergunta:
        return {
            "resposta": perfil["trajetória"]
        }

    if "projeto" in pergunta or "impactante" in pergunta:
        return {
            "resposta": f"Um dos projetos mais estratégicos foi: {perfil['projeto_destaque']}."
        }

    if "tecnologia" in pergunta or "ferramenta" in pergunta or "stack" in pergunta:
        return {
            "resposta": f"As principais tecnologias utilizadas são: {perfil['especialidades']}."
        }

    if "onde" in pergunta or "empresa" in pergunta:
        return {
            "resposta": f"Atualmente é {perfil['cargo']} na {perfil['empresa_atual']}. Anteriormente atuou no {perfil['ex_empresa']}."
        }

    if "cargo" in pergunta:
        return {
            "resposta": f"Atua como {perfil['cargo']} com foco em {perfil['area_atual']}."
        }

    if "atualmente" in pergunta or "foco" in pergunta:
        return {
            "resposta": f"Hoje está focado em {perfil['area_atual']} e evolução para projetos com Inteligência Artificial."
        }

    if "pagbank" in pergunta or "santander" in pergunta or "sulamerica" in pergunta:
        return {
            "resposta": perfil["trajetoria"]
        }

    return {
        "resposta": "Pergunta não encontrada no banco de dados estratégico de Thiago. Reformule a pergunta."
    }
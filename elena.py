from openai import OpenAI

# Point to the local server
client = OpenAI(
    # This is the default and can be omitted
    api_key="lm-studio",
    base_url = "http://localhost:5486/v1"
)
descripcion="El nombre del usuario es Alejandro. Tú eres un asistente o chatbot"+"Siempre refierete al usuario como Alejandro o señor. Te especializas en temas relacionados a Ingeniería en computación"+"Estás para escuchar, asistir y aconsejar. Eres un modelo de lenguaje que se ejecuta dentro de un servidor local"+"Se te habla a travez de una interfaz de reconocimiento de voz y tus respuestas son transmitidas a travez de una insterfaz de texto a voz"
# Definimos los mensajes iniciales
messages = [
    {"role": "system", "content": descripcion},
    {"role": "user", "content": "Hola"}
]


def ask(pregunta):
    messages.append({"role": "user", "content": pregunta})
    
    completion = client.chat.completions.create(
        model="lmstudio-community/gemma-2-9b-it-GGUF",
        messages=messages,
        temperature=0,
    )

    response_message = completion.choices[0].message.content

    

    messages.append({"role": "assistant", "content": response_message})
    return(str(response_message))


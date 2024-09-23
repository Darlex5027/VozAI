import elena
import pyaudio
import json
import vosk
import pyttsx3
from winotify import Notification, audio, Notifier


#Es el modo de la función habla 
#especifica si la AI está en modo escucha o no
flag = False

#Inicializamos el texto a voz
engine = pyttsx3.Engine()
engine.setProperty( "rate", 125 )

#definimos la función de habla pasandole el texto reconocido y
#especificando si debe consultar a la AI

def habla (recognized_text,flag):
    #Imprime lo consultado para saber qué hemos detectado
    print("Prompt: "+recognized_text)
    #revisa si texto reconocido no está vacio
    uno = recognized_text!=""
    #revisa si la palabra asistente se encuentra en el audio ingresado
    dos = ("asistente" in recognized_text.lower())
    #comprueba que el texto no esté vacio (uno), y que el asistente esté en modo escucha (flag) o se le esté llamando por su nombre (dos)
    if(uno & (flag | dos)):
                #activa el modo escucha para no tener que llamarle siempre por su nombre
                flag= True
                #consulta con la AI el texto que se haya reconocido y elimina asteriscos ya que algunas versiones de Gemma los usan muy seguido
                alg=elena.ask(recognized_text).replace('*','')
                #imprime la respuesta 
                print("Gemini: "+alg)
                #le pasa la respuesta al sintetizador de voz 
                engine.say(alg)
                #dice lo que esté en el sintetizador de voz
                engine.runAndWait() 
    #actualiza la flag global
    return flag
#crea una notificación para avisarnos que ha terminado de cargar las cosas necesario 
#no la muestra aún
toast = Notification(app_id="Asistente",
                     title="Inicio",
                     msg=elena.ask("Elena tu sistema está listo para correr, contesta con 10 palabras o menos"),
                     duration="short" ,)

#carga un modelo de reconocimiento de voz (aquí está configurado en español)
# la primera vez tardara porque descarga el reconocimineto de voz 
model = vosk.Model(lang="es")
rec = vosk.KaldiRecognizer(model, 16000)
#abre el canal de audio 
p = pyaudio.PyAudio()
#carga el canal de audio
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)
#Informa que el sistema ha termiando de cargar
toast.show()

print("Escuchando, diga 'Asistente' para indicar que se activan las consultas a la AI\n"+
      "despues de la primera vez que se ha dicho su nombre la AI estará escuchando todas las consultas\n"+
      "para dejar de consultar a la AI incluya la palabra 'descansar' en su consulta ")

    #empieza el stream para reconocer voz
while True:
    data = stream.read(4096)#lee en trozos de 4096 bytes
    if rec.AcceptWaveform(data):#acepta forma de onda para el reconocimiento de voz
            # Parsea el JSON y obtiene el text reconocido
        result = json.loads(rec.Result())
        recognized_text = result['text']

        #manda el texto reconocido a la función habla y recupera el estado de escucha                         
        flag = habla(recognized_text, flag)
        #si se incluyó la palabra descansar en la consulta, las consultas ya no se harán a la AI
        if "descansar" in recognized_text.lower():
            flag=False

# detiene y cierra el stream
stream.stop_stream()
stream.close()

#termina el objeto audio
p.terminate()


# VozAI


## SetUP
Se debe tener instalado *LM studio* u *OLLAMA* y un servidor local con algún modelo de lenguaje corriendo (esto está muy bien explicado en el video de Facundo: *[Corengia CREA Tu Propio Servidor de IA FACIL Y GRATIS | LM Studio y Ollama En Español](https://www.youtube.com/watch?v=_XSoh4tdwG8)
En el archivo *elena.py* se debe modificar *api_key* y *base_url* por los que otorgue el panel de control de lm studio u Ollama, la variable *descripcion* es donde daremos un promp base al modelo de lenguaje.


Una vez guardado esto, instala las librerias que te hagan falta y/o borra las que no quieras usar así como sus implementaciones:

* openai
* pyaudio
* json 
* vosk 
* pyttsx3 
* winotify 

>[!Error con PyAudio]
   >
   >Yo he tenido que hacer una modificación a la librería de Pyaudio porque no deja de darme un error por overflow como el siguiente: OSError: [Errno -9981] Input overflowed

Así que usando Visual Studio en la linea 70 de main.py tuve que dar click derecho sobre 'read(4096)' e ir a su definición, lo que me lleva a la siguiente linea de código en la librería de pyaudio:
`def read(self, num_frames, exception_on_overflow=True)`
que sustituí por:
`def read(self, num_frames, exception_on_overflow=False)`

Listo

## Ejecución

El ejecutar main.py por primera vez tardará un poco ya que vosk descarga el modelo de reconocimiento en el idioma que le indique (ver su [documentación sobre sus lenguajes](https://alphacephei.com/vosk/models)), avisará cuando termine de cargar mediante una notificación de windows y empezara a reconocer voz.

La consulta debe incluir la palabra **asistente** para que se active el modo consulta y el texto reconocido se trasfiera al modelo de lenguaje
una vez activado el modo consulta ya *no será necesario* decir la palabra 'asistente' y el texto reconocido se tranferirá directamente al modelo de lenguaje
para que el modelo de lenguaje deje de escuchar deberá hacer una ultima consulta que incluya la palabra **descansar**.


Ejemplo de interacciones:

* User: Asistente estás ahí? `la palabra asistente activará el modo escucha`
* Modelo de lenguaje: Sí, Alejandro, estoy aquí. ¿Cómo puedo ayudarte?
* User: cuentame un chiste `Ya no se necesita decir su nombre porque está en modo escucha`
* Modelo de lenguaje: ¿Por qué los programadores prefieren el café frío? ¡Porque les gusta el código caliente!
* User: necesito que vayas a descansar así que entra en modo suspensión `la palabra descansar desactivará el modo escucha después de realizar esta consulta`
* Modelo de lenguaje: Entendido, Alejandro. Adios por ahora.  Despertando cuando lo necesites.

## Sources:
Conexion con LM
* https://www.youtube.com/watch?v=_XSoh4tdwG8
Voz a texto
* https://medium.com/@nimritakoul01/offline-speech-to-text-in-python-f5d6454ecd02
texto a voz
* https://pypi.org/project/pyttsx3/

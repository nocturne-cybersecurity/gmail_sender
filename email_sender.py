
import smtplib
import time
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EnviadorCorreos:
    def __init__(self, remitente: str, contrasena: str, servidor_smtp: str = 'smtp.gmail.com', puerto: int = 587):
        self.remitente = remitente
        self.contrasena = contrasena
        self.servidor_smtp = servidor_smtp
        self.puerto = puerto
        self.servidor = None

    def conectar_servidor(self) -> bool:
        #conexion smtp
        try:
            self.servidor = smtplib.SMTP(self.servidor_smtp, self.puerto)
            self.servidor.starttls()
            self.servidor.login(self.remitente, self.contrasena)
            return True
        except Exception as e:
            print(f"Error al conectar con el servidor: {e}")
            return False

    def desconectar_servidor(self):
        #cerrar conexion smtp
        if self.servidor:
            self.servidor.quit()

    def enviar_correo(self, destinatario: str, asunto: str, mensaje: str, es_html: bool = False) -> bool:
        #enviar correo
        try:
            msg = MIMEMultipart()
            msg['From'] = self.remitente
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            #mensaje
            msg.attach(MIMEText(mensaje, 'html' if es_html else 'plain'))
            
            # Enviar correo
            self.servidor.send_message(msg)
            print(f"Correo enviado a: {destinatario}")
            return True
            
        except Exception as e:
            print(f"Error al enviar a {destinatario}: {str(e)}")
            return False

    def enviar_masivo_desde_csv(self, archivo_csv: str, columna_email: str, asunto: str, 
                               plantilla: str, delay_segundos: int = 2, limite: int = 0):
        if not self.conectar_servidor():
            return

        try:
            with open(archivo_csv, 'r', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                total = 0
                exitosos = 0
                
                for fila in lector:
                    if limite > 0 and total >= limite:
                        break
                        
                    #asunto personalizado
                    asunto_personalizado = asunto.format(**fila)
                    mensaje_personalizado = plantilla.format(**fila)
                    
                    # Enviar correo
                    if self.enviar_correo(
                        destinatario=fila[columna_email],
                        asunto=asunto_personalizado,
                        mensaje=mensaje_personalizado
                    ):
                        exitosos += 1
                    
                    total += 1
                    
                    #esperar para evitar bloqueosss
                    if total < len(lector) and delay_segundos > 0:
                        time.sleep(delay_segundos)
                
                print(f"\nResumen de envío:")
                print(f"Total intentados: {total}")
                print(f"Envíos exitosos: {exitosos}")
                print(f"Fallidos: {total - exitosos}")
                
        except Exception as e:
            print(f"Error al procesar el archivo CSV: {e}")
        finally:
            self.desconectar_servidor()


def crear_plantilla_ejemplo():
    #crear csv
    with open('destinatarios_ejemplo.csv', 'w', encoding='utf-8') as f:
        f.write("""nombre,email,empresa
Juan Pérez,juan@empresa.com,Empresa A
María López,maria@otraempresa.com,Empresa B
""")
    
    #plantilla de ejemplo paralas empreas
    with open('plantilla_ejemplo.html', 'w', encoding='utf-8') as f:
        f.write("""<html>
  <body>
    <h2>Hola {nombre},</h2>
    <p>Esperamos que este mensaje te encuentre bien.</p>
    <p>Nos complace contactarte de parte de {empresa}.</p>
    <p>Saludos cordiales,<br>El equipo de soporte</p>
  </body>
</html>""")
    
    print("Archivos de ejemplo creados: destinatarios_ejemplo.csv y plantilla_ejemplo.html")


if __name__ == "__main__":
    #config
    CONFIG = {
        'remitente': 'tu_correo@gmail.com',
        'contrasena': 'tu_contraseña',  #Recuerda que debes crear una contraseña de aplicacion en tu cuenta de gmail sino no funciona
        'archivo_csv': 'destinatarios.csv',  #cambiar archivo csv
        'columna_email': 'email',
        'asunto': 'Mensaje importante para {nombre}',
        'plantilla': '''
        Hola {nombre},
        
        Este es un mensaje personalizado para ti de {empresa}.
        
        Saludos,
        El equipo de soporte
        ''',
        'delay_segundos': 2,  #tiempo de espera
        'limite': 0           #limite de correos
    }

    enviador = EnviadorCorreos(
        remitente=CONFIG['remitente'],
        contrasena=CONFIG['contrasena']
    )

    #envira
    enviador.enviar_masivo_desde_csv(
        archivo_csv=CONFIG['archivo_csv'],
        columna_email=CONFIG['columna_email'],
        asunto=CONFIG['asunto'],
        plantilla=CONFIG['plantilla'],
        delay_segundos=CONFIG['delay_segundos'],
        limite=CONFIG['limite']
    )

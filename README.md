# Enviador de Correos Masivos

Este script permite enviar correos electrónicos de manera masiva utilizando una cuenta de Gmail y un archivo CSV con los destinatarios.

## Requisitos

- Python 3.6 o superior
- Cuenta de Gmail
- Contraseña de aplicación de Google

## Configuración

1. Genera una contraseña de aplicación en tu cuenta de Google:
   - Ve a [Seguridad de Google](https://myaccount.google.com/security)
   - Activa la verificación en dos pasos si no está activada
   - Crea una contraseña de aplicación

2. Prepara tu archivo CSV con los destinatarios:
   ```
   nombre,email,empresa
   Ejemplo,ejemplo@dominio.com,Empresa X
   ```

3. Configura el archivo `email_sender.py` con tus datos:
   - `remitente`: Tu correo de Gmail
   - `contrasena`: La contraseña de aplicación generada
   - `archivo_csv`: Ruta a tu archivo CSV
   - `columna_email`: Nombre de la columna que contiene los correos
   - `asunto`: Asunto del correo (puedes usar {nombre}, {empresa}, etc.)
   - `plantilla`: Cuerpo del mensaje (también soporta variables)
   - `delay_segundos`: Tiempo de espera entre envíos (recomendado: 2 segundos)
   - `limite`: Número máximo de correos a enviar (0 para sin límite)

## Uso

1. Ejecuta el script:
   ```
   python email_sender.py
   ```

2. Si necesitas un ejemplo, descomenta la línea `crear_plantilla_ejemplo()` para generar archivos de ejemplo.

## Limitaciones

- Gmail tiene un límite de envíos diarios (alrededor de 100-150 correos/día)
- Para envíos masivos, considera usar un servicio profesional como SendGrid o Amazon SES

## Notas de Seguridad

- Nunca compartas tu contraseña de aplicación
- No subas el archivo de configuración con tus credenciales a repositorios públicos
- Usa siempre contraseñas de aplicación en lugar de contraseñas normales

## Personalización

Puedes personalizar las plantillas HTML en la función `crear_plantilla_ejemplo()` según tus necesidades.

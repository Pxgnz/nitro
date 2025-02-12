import random
import string
from flask import Flask, request, send_file
import os

app = Flask(__name__)

# Directorio para guardar los archivos generados
UPLOAD_FOLDER = 'downloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Función para generar códigos Nitro aleatorios
def generar_nitro(cantidad):
    return [f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=19))}" for _ in range(cantidad)]

# Página principal con botones
@app.route('/')
def home():
    return '''
    <html>
    <head>
        <title>NITRO GEN</title>
        <style>
            body { text-align: center; font-family: Arial, sans-serif; background-color: #36393f; color: white; padding: 50px; }
            .button { display: inline-block; padding: 10px 20px; margin: 10px; background: #5865F2; color: white; border: none; border-radius: 5px; text-decoration: none; font-size: 18px; cursor: pointer; }
            .button:hover { background: #4752c4; }
            .nitro { margin-top: 20px; font-size: 18px; color: #43b581; }
        </style>
    </head>
    <body>
        <h1>NITRO GENERATOR</h1>
        <form action="/generate" method="post">
            <label for="cantidad">Cantidad de Nitro (máx 500,000):</label>
            <input type="number" id="cantidad" name="cantidad" min="1" max="500000" value="1" required>
            <button class="button" type="submit">Generate</button>
        </form>
        <h5> Esta página web fue desarrollada por @pxgnz 
        de forma legal para un uso legítimo sin causar daños a la aplicación de Discord. Es un generador de nitros al azar no verificados. Por favor, no nos hacemos responsables de su uso.</h5>
        <br>
        <a href="https://discord.gg/pfhXRUmuF2" class="button">Unirse a Discord</a>
    </body>
    </html>
    '''

# Ruta para generar códigos Nitro
@app.route('/generate', methods=['POST'])
def generate():
    cantidad = int(request.form.get("cantidad", 100))  # Obtener cantidad de códigos
    if cantidad > 500000:  # Límite de 500,000
        cantidad = 500000

    nitro_codes = generar_nitro(cantidad)
    nitro_list = "<br>".join(nitro_codes)  # Convertir en lista HTML
    
    # Crear el archivo nitro.txt con los códigos generados
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'nitro.txt')
    with open(file_path, 'w') as f:
        for code in nitro_codes:
            f.write(f"{code}\n")
    
    # Enlace para descargar el archivo y mostrar los códigos en la página
    return f'''
    <html>
    <head><title>Generación de Nitro</title></head>
    <body style="text-align: center; font-family: Arial, sans-serif; background-color: #36393f; color: white; padding: 50px;">
        <h1>🚀 ¡Códigos Nitro Generados! 🚀</h1>
        <a href="/download/nitro.txt" class="button">Descargar Nitro.txt</a>
        <p class="nitro">Aquí están los códigos Nitro generados:</p>
        <p class="nitro">{nitro_list}</p>
        <br>
        <br><br>
        <a href="/" class="button">Volver</a>
        <br><br>
        <h5>Únete a nuestro servidor: <a href="https://discord.gg/pfhXRUmuF2" style="color: #5865F2;">discord.gg/pfhXRUmuF2</a></h5>
    </body>
    </html>
    '''

# Ruta para descargar el archivo nitro.txt
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

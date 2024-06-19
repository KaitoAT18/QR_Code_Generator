from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
import datetime

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/qrcodes'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    qr_code_filename = None
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        qr_data = None

        if form_type == 'url':
            qr_data = request.form.get('url')
        elif form_type == 'email':
            email = request.form.get('email')
            subject = request.form.get('subject')
            message = request.form.get('message')
            qr_data = f"mailto:{email}?subject={subject}&body={message}"
        elif form_type == 'contact':
            contact_name = request.form.get('contact_name')
            contact_phone = request.form.get('contact_phone')
            qr_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{contact_name}\nTEL:{contact_phone}\nEND:VCARD"

        if qr_data:
            qr = qrcode.make(qr_data)
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            qr_code_filename = f'qrcode_{timestamp}.png'
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_code_filename)
            qr.save(file_path)

    return render_template('index.html', qr_code_filename=qr_code_filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


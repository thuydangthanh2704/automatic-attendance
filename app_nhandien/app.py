from flask import Flask, render_template, request, send_from_directory
import os
import cv2
import pytesseract
import re
import uuid  # for generating unique filenames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Define a regular expression pattern to match the student ID format
pattern = r'MSV:\s*(\d+)'

def process_image(image):
    # Perform image processing
    image = cv2.resize(image, None, fx=6, fy=6, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Fix the color conversion
    image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)[1]
    image = cv2.medianBlur(image, 7)
    return image

def extract_student_id(image):
    # Use Tesseract OCR to extract text
    text = pytesseract.image_to_string(image)
    pattern = r'MSV:\s*(\d+)'

    # Use re.search to find the pattern in the text
    match = re.search(pattern, text)

    # Check if a match is found
    if match:
        student_id = match.group(1)
        return student_id, text
    else:
        return "Student ID not found in the text."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was submitted
        if 'file' not in request.files:
            return render_template('index.html', error='No file provided')

        file = request.files['file']

        # Check if the file has a valid extension
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        if file.filename.split('.')[-1].lower() not in allowed_extensions:
            return render_template('index.html', error='Invalid file format')

        # Generate a unique filename
        filename = str(uuid.uuid4()) + '.' + file.filename.split('.')[-1].lower()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the 'uploads' directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save the file to the server
        file.save(filepath)

        # Load the uploaded image
        image = cv2.imread(filepath)

        # Process the image
        processed_image = process_image(image)

        # Extract student ID
        student_id, raw_text = extract_student_id(processed_image)

        # Save the processed image
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        cv2.imwrite(processed_image_path, processed_image)

        # Render the result
        return render_template('result.html', student_id=student_id, raw_text=raw_text, 
                               processed_image=os.path.basename(processed_image_path),
                               filename='processed_' + filename)

    return render_template('index.html')

# Serve processed images

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static',filename='uploads/'+filename), code=301)
    
@app.route('/uploads/<filename>')
def processed_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)

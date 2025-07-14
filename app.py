from flask import Flask, render_template, request, redirect, url_for
import os
import time
import tracemalloc
import uuid
from werkzeug.utils import secure_filename

from utils.detect import detect_objects
from utils.spatial import describe_spatial_relationships
from utils.caption import build_prompt, generate_caption
from utils.environment import get_environmental_cue

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    caption = None
    image_url = None
    object_labels = []
    spatial_descriptions = []
    timing = {}

    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{uuid.uuid4()}_{filename}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Start performance tracking
            total_start = time.time()
            tracemalloc.start()

            # Object detection
            detect_start = time.time()
            detections = detect_objects(image_path)
            timing['detection'] = time.time() - detect_start

            object_labels = [d["label"] for d in detections]
            spatial_descriptions = describe_spatial_relationships(detections)
            environment = get_environmental_cue(image_path, object_labels)

            # Caption generation
            prompt = build_prompt(object_labels, spatial_descriptions, environment)
            caption_start = time.time()
            caption = generate_caption(prompt)
            timing['caption'] = time.time() - caption_start

            # Total time and memory
            timing['total'] = time.time() - total_start
            current, peak = tracemalloc.get_traced_memory()
            timing['memory'] = peak / (1024 * 1024)  # MB
            tracemalloc.stop()

            image_url = url_for('static', filename=f'uploads/{filename}')

    return render_template(
        'index.html',
        caption=caption,
        image_url=image_url,
        detected_objects=object_labels,
        spatial_relationships=spatial_descriptions,
        timing=timing
    )

if __name__ == '__main__':
    app.run(debug=True)

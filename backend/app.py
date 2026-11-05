#!/usr/bin/env python3
"""
AI-Based Smart Garbage Waste Segregator — Main Flask REST Backend
Coordinates:
- YOLO Model Management & Real-Time Inference Engine
- Waste Segregation Recommendation Engine
- SQLite Session History & Analytical Storage
- Upload and Result Image Management
"""

import os
import uuid
import shutil
import base64
from pathlib import Path
from datetime import datetime

# Configure Ultralytics cache directory
os.environ.setdefault('YOLO_CONFIG_DIR', '/tmp/ultralytics')

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
from PIL import Image

# Import internal modules
try:
    from model_manager import (
        run_inference,
        get_model_information,
        generate_annotated_image,
        TARGET_15_CLASSES
    )
    from recommendation_engine import (
        get_recommendation_for_class,
        analyze_detections_summary
    )
    from db import (
        init_db,
        save_detection_session,
        get_history,
        get_session_by_id,
        delete_session,
        get_analytics_summary
    )
except ImportError:
    from backend.model_manager import (
        run_inference,
        get_model_information,
        generate_annotated_image,
        TARGET_15_CLASSES
    )
    from backend.recommendation_engine import (
        get_recommendation_for_class,
        analyze_detections_summary
    )
    from backend.db import (
        init_db,
        save_detection_session,
        get_history,
        get_session_by_id,
        delete_session,
        get_analytics_summary
    )

app = Flask(__name__)
CORS(app)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = Path(__file__).resolve().parent
UPLOADS_DIR = BACKEND_DIR / "uploads"
RESULTS_DIR = BACKEND_DIR / "results"
SAMPLES_DIR = PROJECT_ROOT / "test_images"

# Ensure storage directories exist
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Initialize database schema on startup
init_db()

# --- Health & System Endpoints ---

@app.route('/')
def root_status_report():
    """Serve visual Backend Health & Status Dashboard for localhost:5000."""
    model_info = get_model_information()
    now_str = datetime.now().strftime("%B %d, %Y - %I:%M:%S %p")
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WasteSegregator AI — Backend Status Report</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #F8FAFC;
      color: #0F172A;
      padding: 32px 20px;
      line-height: 1.5;
    }
    .container {
      max-width: 1180px;
      margin: 0 auto;
    }
    .hero-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 16px;
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .hero-top {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 16px;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .logo {
      width: 44px;
      height: 44px;
      background: linear-gradient(135deg, #2563EB 0%, #10B981 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.25);
      flex-shrink: 0;
    }
    .logo svg {
      width: 24px;
      height: 24px;
      stroke: #FFFFFF;
    }
    .brand-title {
      font-size: 20px;
      font-weight: 800;
      color: #0F172A;
      letter-spacing: -0.02em;
      line-height: 1.2;
    }
    .brand-title span {
      color: #2563EB;
    }
    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      color: #1D4ED8;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
    }
    .hero-desc {
      font-size: 13px;
      color: #64748B;
      line-height: 1.6;
      max-w-2xl;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      background: #ECFDF5;
      color: #047857;
      border: 1px solid #A7F3D0;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10B981;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
    }
    .meta-bar {
      margin-top: 20px;
      padding-top: 18px;
      border-top: 1px solid #F1F5F9;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      font-size: 12px;
    }
    .meta-item span.label {
      color: #94A3B8;
      font-size: 11px;
      display: block;
      font-weight: 600;
      margin-bottom: 2px;
    }
    .meta-item span.val {
      font-weight: 700;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }
    .card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 14px;
      padding: 22px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .card-label {
      font-size: 11px;
      font-weight: 700;
      color: #94A3B8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 6px;
    }
    .card-value {
      font-size: 16px;
      font-weight: 800;
      color: #0F172A;
      margin-bottom: 4px;
    }
    .card-desc {
      font-size: 12px;
      color: #64748B;
    }
    .section-title {
      font-size: 14px;
      font-weight: 800;
      color: #0F172A;
      letter-spacing: -0.01em;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .endpoints-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }
    .endpoints-table th {
      background: #F8FAFC;
      padding: 11px 14px;
      text-align: left;
      font-weight: 600;
      color: #475569;
      border-bottom: 1px solid #E2E8F0;
    }
    .endpoints-table td {
      padding: 11px 14px;
      border-bottom: 1px solid #F1F5F9;
    }
    .endpoints-table tr:hover td {
      background: #F8FAFC;
    }
    .method {
      display: inline-block;
      padding: 2px 8px;
      border-radius: 6px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 10px;
    }
    .get { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; }
    .post { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
    .endpoint-link {
      color: #2563EB;
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
    }
    .endpoint-link:hover { text-decoration: underline; }
    .cta-banner {
      background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%);
      color: #FFFFFF;
      border-radius: 14px;
      padding: 24px 28px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-top: 24px;
      box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    .cta-btn {
      background: #FFFFFF;
      color: #1D4ED8;
      padding: 10px 20px;
      border-radius: 10px;
      font-weight: 700;
      font-size: 13px;
      text-decoration: none;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .cta-btn:hover { background: #F8FAFC; transform: translateY(-1px); }
    .classes-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
    }
    .class-pill {
      font-size: 11px;
      padding: 5px 11px;
      border-radius: 8px;
      background: #F1F5F9;
      color: #334155;
      font-weight: 600;
      border: 1px solid #E2E8F0;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }
    .class-pill span.num {
      color: #94A3B8;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Hero Card — Matched with Frontend Layout Architecture -->
    <div class="hero-card">
      <div class="badge-pill">
        <span>Inference Engine &amp; API Service</span>
        <span>•</span>
        <span>Port 5000</span>
      </div>

      <div class="hero-top">
        <div class="brand">
          <div class="logo">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
              <path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/>
              <path d="m14 16-3 3 3 3"/>
              <path d="M8.293 13.596 7.196 9.5 3.1 10.598"/>
              <path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843"/>
              <path d="m13.378 9.633 4.096 1.098 1.097-4.096"/>
            </svg>
          </div>
          <div>
            <div class="brand-title">WasteSegregator <span>AI</span> — Backend Service</div>
            <div class="hero-desc">High-performance computer vision inference runtime and municipal classification API.</div>
          </div>
        </div>

        <div class="status-badge">
          <span class="pulse-dot"></span>
          <span>BACKEND OPERATIONAL</span>
        </div>
      </div>

      <!-- 4-Column Metadata Strip -->
      <div class="meta-bar">
        <div class="meta-item">
          <span class="label">ACTIVE NEURAL NETWORK</span>
          <span class="val" style="color: #2563EB;">{{ model_name }}</span>
        </div>
        <div class="meta-item">
          <span class="label">HARDWARE ACCELERATION</span>
          <span class="val" style="color: #059669;">{{ hardware }}</span>
        </div>
        <div class="meta-item">
          <span class="label">REGISTERED TAXONOMY</span>
          <span class="val" style="color: #059669;">{{ classes_count }} Categories</span>
        </div>
        <div class="meta-item">
          <span class="label">DATABASE STORAGE</span>
          <span class="val" style="color: #0F172A;">SQLite Connected</span>
        </div>
      </div>
    </div>

    <!-- 3 Key Metric Cards -->
    <div class="grid">
      <div class="card">
        <div class="card-label">Detection Architecture</div>
        <div class="card-value">{{ model_name }}</div>
        <div class="card-desc">{{ classes_count }} Registered Waste Categories Active</div>
      </div>

      <div class="card">
        <div class="card-label">Compute Device</div>
        <div class="card-value">{{ hardware }}</div>
        <div class="card-desc">Low-Latency Real-Time Tensor Inference</div>
      </div>

      <div class="card">
        <div class="card-label">Database &amp; Audit Logs</div>
        <div class="card-value">SQLite WAL Storage</div>
        <div class="card-desc">Persistent Session History &amp; Analytical Records</div>
      </div>
    </div>

    <!-- 15 Supported Categories -->
    <div class="card" style="margin-bottom: 24px;">
      <div class="section-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2H2v10l9.29 9.29c.94.94 2.48.94 3.42 0l6.58-6.58c.94-.94.94-2.48 0-3.42L12 2Z"/>
          <path d="M7 7h.01"/>
        </svg>
        <span>15-Class Waste Taxonomy</span>
      </div>
      <div class="classes-grid">
        {% for cls in target_classes %}
          <span class="class-pill"><span class="num">#{{ cls.id }}</span> {{ cls.display }}</span>
        {% endfor %}
      </div>
    </div>

    <!-- Core API Endpoints Table -->
    <div class="card">
      <div class="section-title">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
        </svg>
        <span>Available REST API Endpoints</span>
      </div>
      <table class="endpoints-table">
        <thead>
          <tr>
            <th>Method</th>
            <th>Endpoint</th>
            <th>Description</th>
            <th>Format</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/health" class="endpoint-link">/api/health</a></td>
            <td>System status, active model &amp; hardware info</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/classes" class="endpoint-link">/api/classes</a></td>
            <td>15-Class waste taxonomy &amp; bin mapping</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/model-info" class="endpoint-link">/api/model-info</a></td>
            <td>Model checkpoints, resolution &amp; accuracy metrics</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method post">POST</span></td>
            <td><span class="endpoint-link">/api/detect</span></td>
            <td>Waste detection, localization &amp; segregation recommendations</td>
            <td>Multipart / JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/history" class="endpoint-link">/api/history</a></td>
            <td>Saved detection sessions &amp; audit records</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/analytics" class="endpoint-link">/api/analytics</a></td>
            <td>Material distribution &amp; recyclability statistics</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/training/runs" class="endpoint-link">/api/training/runs</a></td>
            <td>Model training runs &amp; empirical loss curves</td>
            <td>JSON</td>
          </tr>
          <tr>
            <td><span class="method get">GET</span></td>
            <td><a href="/api/sample-images" class="endpoint-link">/api/sample-images</a></td>
            <td>Pre-loaded test verification images</td>
            <td>JSON</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Frontend Client CTA Banner -->
    <div class="cta-banner">
      <div>
        <div style="font-size: 16px; font-weight: 800; margin-bottom: 4px;">Web Application Client (Port 3000)</div>
        <div style="font-size: 12px; opacity: 0.9;">Interactive waste scanner, live webcam detection, analytics dashboard, and printable audit certificates.</div>
      </div>
      <a href="http://localhost:3000" target="_blank" class="cta-btn">
        <span>Open Web Client</span>
        <span>→</span>
      </a>
    </div>

    <div style="text-align: center; margin-top: 24px; font-size: 11px; color: #94A3B8;">
      WasteSegregator AI Backend • Port 5000 • SQLite Storage • {{ timestamp }}
    </div>
  </div>
</body>
</html>"""

    return render_template_string(
        html,
        model_name=model_info.get("active_model_name", "YOLO11n Waste-15 Flagship"),
        classes_count=model_info.get("supported_classes_count", 15),
        hardware=model_info.get("device_display", "GPU Accelerated"),
        target_classes=TARGET_15_CLASSES,
        timestamp=now_str
    )

@app.route('/api/health')
def health():
    """Health check endpoint providing system status and environment info."""
    model_info = get_model_information()
    return jsonify({
        "status": "healthy",
        "project": "AI-Based Smart Garbage Waste Segregator",
        "version": "2.0.0",
        "device": model_info["device_display"],
        "active_model": model_info["active_model_name"],
        "is_final_15_class": model_info["is_final_15_class"],
        "supported_classes_count": model_info["supported_classes_count"],
        "database": "SQLite (Connected)"
    })


@app.route('/api/classes')
def list_classes():
    """Return both the target 15-class taxonomy and the currently active model's classes."""
    model_info = get_model_information()
    return jsonify({
        "target_15_classes": TARGET_15_CLASSES,
        "target_count": len(TARGET_15_CLASSES),
        "active_model_supported_classes": model_info["supported_classes"],
        "active_count": model_info["supported_classes_count"],
        "is_baseline_model": not model_info["is_final_15_class"],
        "notice": "The model currently detects the 10-class baseline. The recommendation engine supports all 15 target categories."
    })


@app.route('/api/model-info')
@app.route('/api/model/info')
def model_information():
    """Detailed model metadata, performance metrics, and configuration options."""
    return jsonify(get_model_information())


@app.route('/api/model/switch', methods=['POST'])
def switch_active_model():
    """
    Dynamically switch active detection model:
    - tri_model_ensemble: Tri-Model Consensus Ensemble (Highest Accuracy)
    - yolo11n_15class_target: 100-Epoch Flagship Master (Fast single model)
    - yolo11n_15class_kaggle_master: 100-Epoch Kaggle Master (800px)
    - yolo11s_15class_high_precision: 100-Epoch YOLO11s (800px)
    """
    from model_manager import set_active_model
    data = request.get_json(silent=True) or request.form
    target_id = data.get('model_id') if data else None
    if not target_id:
        return jsonify({"error": "Missing 'model_id' parameter in request"}), 400

    success = set_active_model(target_id)
    if not success:
        return jsonify({"error": f"Invalid model_id: '{target_id}'"}), 400

    info = get_model_information()
    return jsonify({
        "status": "success",
        "active_model_id": info["active_model_id"],
        "active_model_name": info["active_model_name"],
        "message": f"Successfully activated {info['active_model_name']}"
    })


# --- Detection Endpoint ---

@app.route('/api/detect', methods=['POST'])
@app.route('/api/predict', methods=['POST'])
def detect_waste():
    """
    Main detection workflow:
    1. Validate image upload or sample reference
    2. Store original image in backend/uploads/
    3. Run YOLO inference with hardware acceleration
    4. Pass detected objects to the rule-based recommendation engine
    5. Generate high-resolution annotated image in backend/results/
    6. Persist detection session to SQLite database
    7. Return full structured result to frontend
    """
    try:
        conf_threshold = float(request.form.get('conf', request.args.get('conf', 0.10)))
        model_id = request.form.get('model_id', request.args.get('model_id', None))

        session_id = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        original_filename = "upload.jpg"
        temp_input_path = None

        # 1. Check for quick sample name
        sample_name = request.form.get('sample_name')
        if not sample_name and request.is_json:
            sample_name = request.json.get('sample_name')

        if sample_name:
            source_sample = SAMPLES_DIR / sample_name
            if not source_sample.exists():
                return jsonify({"error": f"Sample image '{sample_name}' not found."}), 404

            original_filename = sample_name
            stored_upload_path = UPLOADS_DIR / f"{session_id}_{original_filename}"
            shutil.copy2(source_sample, stored_upload_path)
            temp_input_path = str(stored_upload_path)

        # 2. Check for uploaded file
        elif 'image' in request.files and request.files['image'].filename != '':
            file = request.files['image']
            original_filename = file.filename
            ext = Path(original_filename).suffix.lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.bmp']:
                return jsonify({"error": "Unsupported image format. Allowed formats: JPG, PNG, WEBP, BMP."}), 400

            stored_upload_path = UPLOADS_DIR / f"{session_id}_{original_filename}"
            file.save(str(stored_upload_path))
            temp_input_path = str(stored_upload_path)

        # 3. Check for base64 JSON payload
        elif request.is_json and 'image_base64' in request.json:
            b64_str = request.json['image_base64']
            if ',' in b64_str:
                b64_str = b64_str.split(',')[1]
            img_bytes = base64.b64decode(b64_str)
            original_filename = request.json.get('filename', 'captured_image.jpg')
            stored_upload_path = UPLOADS_DIR / f"{session_id}_{original_filename}"
            with open(stored_upload_path, 'wb') as f:
                f.write(img_bytes)
            temp_input_path = str(stored_upload_path)

        else:
            return jsonify({"error": "No image provided. Please select an image or sample to detect."}), 400

        # Validate file size
        file_size = os.path.getsize(temp_input_path)
        if file_size > 16 * 1024 * 1024:
            return jsonify({"error": "File size exceeds 16MB limit."}), 400

        # Validate image integrity with PIL
        with Image.open(temp_input_path) as pil_img:
            img_width, img_height = pil_img.size

        # Run YOLO inference
        detections, model_meta, latency_ms = run_inference(
            temp_input_path,
            conf_threshold=conf_threshold,
            model_id=model_id
        )

        # Enhance each detection with rule-based recommendations
        for det in detections:
            rec = get_recommendation_for_class(det["class_name"])
            det["recommendation"] = rec

        # Generate summary analytics
        summary = analyze_detections_summary(detections)

        # Generate annotated image
        annotated_filename = f"{session_id}_annotated.jpg"
        annotated_path = RESULTS_DIR / annotated_filename
        generate_annotated_image(temp_input_path, detections, str(annotated_path))

        # Build base64 preview for instant rendering
        annotated_b64 = None
        if annotated_path.exists():
            with open(annotated_path, 'rb') as f:
                annotated_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')

        # Persist session to SQLite database
        session_record = {
            "id": session_id,
            "created_at": datetime.utcnow().isoformat(),
            "original_filename": original_filename,
            "original_image_path": str(stored_upload_path),
            "annotated_image_path": str(annotated_path),
            "thumbnail_path": str(annotated_path),
            "file_size_bytes": file_size,
            "image_width": img_width,
            "image_height": img_height,
            "total_objects": len(detections),
            "primary_category": detections[0]["class_name"] if detections else "None",
            "primary_disposal": summary["primary_disposal"],
            "recyclability_rate": summary["recyclability_rate"],
            "processing_time_ms": latency_ms,
            "model_name": model_meta["name"],
            "confidence_threshold": conf_threshold,
            "summary_advice": summary["summary_advice"]
        }
        save_detection_session(session_record, detections)

        return jsonify({
            "success": True,
            "session_id": session_id,
            "created_at": session_record["created_at"],
            "original_filename": original_filename,
            "original_image_url": f"/api/uploads/{stored_upload_path.name}",
            "annotated_image_url": f"/api/results/{annotated_filename}",
            "annotated_image_b64": annotated_b64,
            "image_width": img_width,
            "image_height": img_height,
            "total_detections": len(detections),
            "processing_time_ms": latency_ms,
            "model_used": model_meta["name"],
            "confidence_threshold": conf_threshold,
            "detections": detections,
            "summary": summary
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Detection failed: {str(e)}"}), 500


# --- History Endpoints ---

@app.route('/api/history')
def list_history():
    """Retrieve paginated detection history with search and category filters."""
    try:
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        search = request.args.get('search', None)
        category = request.args.get('category', None)
        disposal = request.args.get('disposal', None)

        records, total = get_history(limit=limit, offset=offset, search=search,
                                     category=category, disposal=disposal)
        return jsonify({
            "history": records,
            "total": total,
            "limit": limit,
            "offset": offset
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/history/<session_id>')
def get_history_detail(session_id):
    """Retrieve full detail for a specific historical detection session."""
    session_data = get_session_by_id(session_id)
    if not session_data:
        return jsonify({"error": f"Session '{session_id}' not found."}), 404
    return jsonify(session_data)


@app.route('/api/history/<session_id>', methods=['DELETE'])
def remove_history_entry(session_id):
    """Delete a detection session and remove its image files from disk."""
    success = delete_session(session_id)
    if not success:
        return jsonify({"error": f"Session '{session_id}' not found."}), 404
    return jsonify({"success": True, "message": f"Session '{session_id}' deleted."})


# --- Analytics Endpoint ---

@app.route('/api/analytics')
def analytics():
    """Retrieve real aggregated statistics calculated from SQLite detection records."""
    summary = get_analytics_summary()
    return jsonify(summary)


# --- Recommendation Endpoint ---

@app.route('/api/recommendations/<class_name>')
def get_class_recommendation(class_name):
    """Retrieve recommendation guidelines for any specific waste class."""
    rec = get_recommendation_for_class(class_name)
    return jsonify(rec)


# --- Sample Images Endpoints ---

@app.route('/api/sample-images')
def list_samples():
    """List sample test images available for 1-click testing."""
    samples = []
    descriptions = {
        "11.png": "Bottles & Cans (Recyclable Mixed Packaging)",
        "12.png": "Litter Collection (Plastic Bags, Wrappers & Bottles)",
        "13.png": "Glass Jars & Small Metal Scrap"
    }

    if SAMPLES_DIR.exists():
        for f in sorted(SAMPLES_DIR.glob("*.png")):
            samples.append({
                "id": f.name,
                "filename": f.name,
                "title": descriptions.get(f.name, f.name),
                "url": f"/api/sample-images/{f.name}",
                "size_kb": round(f.stat().st_size / 1024, 1)
            })

    return jsonify({"samples": samples, "total": len(samples)})


@app.route('/api/sample-images/<filename>')
def serve_sample(filename):
    """Serve sample image file."""
    if SAMPLES_DIR.exists():
        return send_from_directory(str(SAMPLES_DIR), filename)
    return jsonify({"error": "Sample image not found"}), 404


# --- Static Media Serving (Uploads & Results) ---

@app.route('/api/uploads/<path:filename>')
def serve_upload(filename):
    """Serve original uploaded images."""
    return send_from_directory(str(UPLOADS_DIR), filename)


@app.route('/api/results/<path:filename>')
def serve_result(filename):
    """Serve annotated output images."""
    return send_from_directory(str(RESULTS_DIR), filename)


# --- Research Views Endpoints (Datasets, Training, Files) ---

@app.route('/api/datasets')
def list_datasets():
    datasets = []

    waste_15 = PROJECT_ROOT / "datasets" / "waste_15class_master"
    if waste_15.exists():
        split_stats = {}
        total_images = 0
        total_objects = 0
        for split in ["train", "val", "test"]:
            img_dir = waste_15 / "images" / split
            lbl_dir = waste_15 / "labels" / split
            if img_dir.exists() and lbl_dir.exists():
                images = [f for f in img_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
                labels = [f for f in lbl_dir.glob('*.txt')]
                obj_count = sum(len([line for line in open(lbl).read().splitlines() if line.strip()]) for lbl in labels)
                split_stats[split] = {"images": len(images), "labels": len(labels), "objects": obj_count}
                total_images += len(images)
                total_objects += obj_count
            else:
                split_stats[split] = {"images": 0, "labels": 0, "objects": 0}

        datasets.append({
            "id": "waste_15class_master",
            "name": "15-Class Master Waste Dataset (Flagship)",
            "description": "Consolidated, balanced multi-source dataset (TACO + Roboflow V7 + YOLO Waste + E-Waste)",
            "splits": split_stats,
            "classes": [c["name"] for c in TARGET_15_CLASSES],
            "total_images": total_images,
            "total_objects": total_objects,
            "class_count": 15
        })

    taco_yolo = PROJECT_ROOT / "datasets" / "taco_yolo"
    if taco_yolo.exists():
        split_stats = {}
        total_images = 0
        total_objects = 0
        for split in ["train", "val", "test"]:
            img_dir = taco_yolo / "images" / split
            lbl_dir = taco_yolo / "labels" / split
            if img_dir.exists() and lbl_dir.exists():
                images = [f for f in img_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
                labels = [f for f in lbl_dir.glob('*.txt')]
                obj_count = sum(len([line for line in open(lbl).read().splitlines() if line.strip()]) for lbl in labels)
                split_stats[split] = {"images": len(images), "labels": len(labels), "objects": obj_count}
                total_images += len(images)
                total_objects += obj_count
            else:
                split_stats[split] = {"images": 0, "labels": 0, "objects": 0}

        datasets.append({
            "id": "taco_yolo",
            "name": "TACO YOLO Dataset",
            "description": "Base TACO dataset converted into YOLO format",
            "splits": split_stats,
            "classes": [c["name"] for c in TARGET_15_CLASSES[:10]],
            "total_images": total_images,
            "total_objects": total_objects,
            "class_count": 10
        })

    taco_plus = PROJECT_ROOT / "datasets" / "taco_plus_waste_v1"
    if taco_plus.exists():
        datasets.append({
            "id": "taco_plus_waste_v1",
            "name": "TACO Plus Waste v1",
            "description": "Multi-source consolidated waste dataset",
            "splits": {},
            "classes": [c["name"] for c in TARGET_15_CLASSES[:10]],
            "total_images": 3120,
            "class_count": 10
        })

    return jsonify({"datasets": datasets, "total": len(datasets)})


@app.route('/api/datasets/<dataset_id>/stats')
def dataset_stats(dataset_id):
    ds_path = PROJECT_ROOT / "datasets" / dataset_id
    if not ds_path.exists():
        return jsonify({"error": "Dataset not found"}), 404

    yaml_p = ds_path / "data.yaml"
    class_count = 15 if "15class" in dataset_id else 10
    if yaml_p.exists():
        try:
            import yaml
            with open(yaml_p) as yf:
                yd = yaml.safe_load(yf)
                if yd and 'nc' in yd:
                    class_count = int(yd['nc'])
        except Exception:
            pass

    stats = {"total_images": 0, "total_objects": 0, "class_count": class_count}
    for split in ["train", "val", "test"]:
        img_dir = ds_path / "images" / split
        lbl_dir = ds_path / "labels" / split
        if img_dir.exists() and lbl_dir.exists():
            images = [f for f in img_dir.iterdir() if f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
            labels = [f for f in lbl_dir.glob('*.txt')]
            obj_count = 0
            for lbl in labels:
                try:
                    obj_count += len([l for l in open(lbl).read().splitlines() if l.strip()])
                except Exception:
                    pass
            stats[f"{split}_images"] = len(images)
            stats[f"{split}_labels"] = len(labels)
            stats[f"{split}_objects"] = obj_count
            stats["total_images"] += len(images)
            stats["total_objects"] += obj_count

    return jsonify(stats)


@app.route('/api/datasets/<dataset_id>/images/<split>/<filename>')
def serve_dataset_image(dataset_id, split, filename):
    img_dir = PROJECT_ROOT / "datasets" / dataset_id / "images" / split
    if img_dir.exists():
        return send_from_directory(str(img_dir), filename)
    return jsonify({"error": "Image not found"}), 404


@app.route('/api/training/runs')
def list_training_runs():
    import csv
    runs_dir = PROJECT_ROOT / "runs" / "detect" / "runs" / "garbage"
    if not runs_dir.exists():
        return jsonify({"runs": []})

    runs = []
    # Known run descriptions and hardware tags
    run_meta_overrides = {
        "yolo11n_15class_colab": {
            "name": "YOLO11n 15-Class Flagship Master Model (100 Epochs)",
            "hardware": "High-Performance GPU Training (100 Epochs Full Master)",
            "dataset": "waste_15class_master (6,349 images, 19,722 objects)",
            "classes_count": 15,
            "badge": "100-Epoch Flagship Master",
            "is_best": True
        },
        "yolo11s_15class_high_precision": {
            "name": "YOLO11s High-Precision Master (100 Epochs @ 800px)",
            "hardware": "High-Performance GPU Training (100 Epochs @ 800px)",
            "dataset": "waste_15class_master (6,349 images, 19,722 objects)",
            "classes_count": 15,
            "badge": "100-Epoch High-Precision (800px)",
            "is_best": False
        },
        "yolo11n_15class_kaggle_master": {
            "name": "YOLO11n 15-Class Kaggle Master (100 Epochs @ 800px)",
            "hardware": "NVIDIA Tesla T4 GPU (100 Epochs Full Master @ 800px)",
            "dataset": "waste_15class_master (8,718 images, 32,900+ objects)",
            "classes_count": 15,
            "badge": "100-Epoch Kaggle Master (800px)",
            "is_best": False
        },
        "yolo11n_15class_balanced_boost": {
            "name": "YOLO11n 15-Class Balanced Boost (30 Epochs)",
            "hardware": "GPU Fine-Tuning (30 Epochs Rebalanced Boost)",
            "dataset": "waste_15class_master (8,574 images, 32,000+ objects)",
            "classes_count": 15,
            "badge": "30-Epoch Balanced Boost",
            "is_best": False
        },
        "yolo11n_15class_master": {
            "name": "YOLO11n 15-Class Validation Run",
            "hardware": "GPU Accelerated",
            "dataset": "waste_15class_master (6,349 images)",
            "classes_count": 15,
            "badge": "15-Class Validation",
            "is_best": False
        },
        "yolo11n_768_experiment": {
            "name": "YOLO11n Waste-768 Baseline",
            "hardware": "GPU Accelerated",
            "dataset": "TACO Waste Baseline (1,500 images)",
            "classes_count": 10,
            "badge": "10-Class Baseline",
            "is_best": False
        },
        "yolo11n_fresh": {
            "name": "YOLO11n Waste-640 Baseline",
            "hardware": "GPU Accelerated",
            "dataset": "TACO Waste Baseline (1,500 images)",
            "classes_count": 10,
            "badge": "10-Class Baseline",
            "is_best": False
        }
    }

    for r in sorted(runs_dir.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
        if r.is_dir():
            weights_file = None
            for w in [r / "weights" / "best.pt", r / "weights" / "last.pt"]:
                if w.exists():
                    weights_file = str(w)
                    break

            res_csv = r / "results.csv"
            # Only include valid training runs that have weights or training metrics
            if not weights_file and not res_csv.exists():
                continue

            final_metrics = {}
            if res_csv.exists():
                try:
                    with open(res_csv, 'r') as f:
                        rows = list(csv.DictReader(f))
                        if rows:
                            # Clean keys
                            cleaned_rows = [{k.strip(): v for k, v in row.items()} for row in rows]
                            # Best row according to mAP50
                            best_row = max(cleaned_rows, key=lambda r: float(r.get('metrics/mAP50(B)', 0)))
                            for k in ['metrics/mAP50(B)', 'metrics/precision(B)', 'metrics/recall(B)', 'train/box_loss', 'train/cls_loss', 'metrics/mAP50-95(B)']:
                                if k in best_row and best_row[k]:
                                    final_metrics[k] = round(float(best_row[k].strip()), 4)
                except Exception:
                    pass

            # Detect available plots
            available_plots = []
            for p_file in sorted(r.iterdir()):
                if p_file.is_file() and p_file.suffix.lower() in ('.png', '.jpg', '.jpeg'):
                    available_plots.append(p_file.name)

            override = run_meta_overrides.get(r.name, {})

            runs.append({
                "id": r.name,
                "name": override.get("name", r.name.replace('_', ' ').title()),
                "path": str(r),
                "status": "completed" if weights_file else "in_progress",
                "final_metrics": final_metrics,
                "weights": weights_file,
                "hardware": override.get("hardware", "GPU Accelerated"),
                "dataset": override.get("dataset", "Waste Dataset"),
                "classes_count": override.get("classes_count", 15 if "15class" in r.name else 10),
                "badge": override.get("badge", "YOLO Model"),
                "is_best": override.get("is_best", False),
                "available_plots": available_plots
            })

    # Sort runs so best runs come first
    runs.sort(key=lambda x: (1 if x.get("is_best") else 0, x.get("final_metrics", {}).get("metrics/mAP50(B)", 0)), reverse=True)

    return jsonify({"runs": runs, "total": len(runs)})


@app.route('/api/training/runs/<run_id>/plots/<filename>')
def serve_run_plot(run_id, filename):
    """Serve training evaluation plots (loss curves, confusion matrix, PR curves)."""
    run_dir = PROJECT_ROOT / "runs" / "detect" / "runs" / "garbage" / run_id
    if not run_dir.exists():
        return jsonify({"error": "Run not found"}), 404

    target = (run_dir / filename).resolve()
    # Path traversal protection
    if not str(target).startswith(str(run_dir.resolve())):
        return jsonify({"error": "Access denied"}), 403

    if not target.exists() or not target.is_file():
        return jsonify({"error": "Plot not found"}), 404

    return send_from_directory(str(run_dir), filename)


@app.route('/api/files/list/<path:directory>')
def list_files(directory):
    target = (PROJECT_ROOT / directory).resolve()
    if not str(target).startswith(str(PROJECT_ROOT)):
        return jsonify({"error": "Access denied"}), 403
    if not target.exists():
        return jsonify({"error": "Directory not found"}), 404

    items = []
    for item in sorted(target.iterdir()):
        if item.is_file():
            items.append({"name": item.name, "path": str(item.relative_to(PROJECT_ROOT)), "type": "file", "size": item.stat().st_size})
        elif item.is_dir():
            items.append({"name": item.name, "path": str(item.relative_to(PROJECT_ROOT)), "type": "directory"})

    return jsonify({"items": items, "path": directory})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() in ('true', '1')
    print("\n" + "=" * 65)
    print("♻️  WasteSegregator AI — Backend REST Service")
    print("=" * 65)
    print(f"Server Port: {port}")
    print(f"Health API:  http://localhost:{port}/api/health")
    print(f"Classes API: http://localhost:{port}/api/classes")
    print(f"History API: http://localhost:{port}/api/history")
    print(f"Analytics:   http://localhost:{port}/api/analytics")
    print(f"Detection:   POST http://localhost:{port}/api/detect")
    print("=" * 65 + "\n")
    app.run(host='0.0.0.0', port=port, debug=debug_mode, use_reloader=False)

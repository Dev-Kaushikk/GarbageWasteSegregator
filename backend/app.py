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
    """Serve visual Backend Health & Status Dashboard for localhost:5000 matched to HomePage layout."""
    model_info = get_model_information()
    now_str = datetime.now().strftime("%B %d, %Y - %I:%M:%S %p")
    
    # 15 Target Classes with full metadata for visual taxonomy display
    taxonomy_cards = [
        {"id": 0, "name": "plastic_bottle", "display": "Plastic Bottle", "category": "Plastics", "bin": "Blue (Recyclable)", "color": "#2563EB", "icon": "🍾"},
        {"id": 1, "name": "plastic_wrapper", "display": "Plastic Wrapper", "category": "Plastics", "bin": "Grey (RDF / General)", "color": "#475569", "icon": "🍬"},
        {"id": 2, "name": "plastic_bag", "display": "Plastic Bag", "category": "Plastics", "bin": "Soft Plastic Depot", "color": "#6366F1", "icon": "🛍️"},
        {"id": 3, "name": "plastic_container", "display": "Plastic Container", "category": "Plastics", "bin": "Blue (Recyclable)", "color": "#0284C7", "icon": "🥡"},
        {"id": 4, "name": "paper", "display": "Paper", "category": "Paper & Fiber", "bin": "Blue (Paper)", "color": "#16A34A", "icon": "📄"},
        {"id": 5, "name": "cardboard_carton", "display": "Cardboard Carton", "category": "Paper & Fiber", "bin": "Blue (Cardboard)", "color": "#D97706", "icon": "📦"},
        {"id": 6, "name": "glass", "display": "Glass", "category": "Glass", "bin": "Teal/Blue (Glass)", "color": "#0284C7", "icon": "🥛"},
        {"id": 7, "name": "metal_can", "display": "Metal Can", "category": "Metals", "bin": "Blue (Metals)", "color": "#D97706", "icon": "🥫"},
        {"id": 8, "name": "metal_scrap", "display": "Metal Scrap", "category": "Metals", "bin": "Scrap Metal Depot", "color": "#EA580C", "icon": "🔩"},
        {"id": 9, "name": "styrofoam", "display": "Styrofoam (EPS)", "category": "Polystyrene", "bin": "EPS Depot / Grey", "color": "#64748B", "icon": "🧊"},
        {"id": 10, "name": "food_waste", "display": "Food Waste", "category": "Organics", "bin": "Green (Compost)", "color": "#16A34A", "icon": "🍎"},
        {"id": 11, "name": "fruit_vegetable_peel", "display": "Fruit / Vegetable Peel", "category": "Organics", "bin": "Green (Compost)", "color": "#16A34A", "icon": "🍌"},
        {"id": 12, "name": "garden_waste", "display": "Garden Waste", "category": "Organics", "bin": "Green (Yard Waste)", "color": "#15803D", "icon": "🌿"},
        {"id": 13, "name": "textile", "display": "Textile", "category": "Textiles", "bin": "Clothing Donation", "color": "#7C3AED", "icon": "👕"},
        {"id": 14, "name": "e_waste", "display": "E-Waste", "category": "Electronics", "bin": "E-Waste Depot", "color": "#DC2626", "icon": "🔋"},
    ]
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WasteSegregator AI — Backend Service</title>
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
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
    }
    .top-nav {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid #E2E8F0;
      position: sticky;
      top: 0;
      z-index: 40;
    }
    .nav-container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px;
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }
    .nav-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #0F172A;
    }
    .nav-logo {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #2563EB 0%, #10B981 100%);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    .nav-logo svg {
      width: 20px;
      height: 20px;
      stroke: #FFFFFF;
    }
    .nav-title {
      font-size: 16px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .nav-title span {
      color: #2563EB;
    }
    .nav-tag {
      font-size: 11px;
      font-weight: 600;
      color: #64748B;
      background: #F1F5F9;
      padding: 2px 8px;
      border-radius: 6px;
      margin-left: 4px;
    }
    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .status-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      background: #ECFDF5;
      color: #047857;
      border: 1px solid #A7F3D0;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10B981;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
      100% { opacity: 1; transform: scale(1); }
    }
    .nav-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #2563EB;
      color: #FFFFFF;
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      transition: background 0.15s ease;
    }
    .nav-btn:hover {
      background: #1D4ED8;
    }
    .main-wrap {
      max-width: 1280px;
      margin: 0 auto;
      padding: 28px 24px 60px 24px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }
    /* Hero Section — Exact match to HomePage.jsx */
    .hero-section {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 32px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .hero-content {
      max-width: 768px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .badge-pill {
      align-self: flex-start;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 4px 12px;
      border-radius: 6px;
      background: #EFF6FF;
      border: 1px solid #BFDBFE;
      color: #1D4ED8;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .hero-title {
      font-size: 28px;
      font-weight: 800;
      color: #0F172A;
      letter-spacing: -0.03em;
      line-height: 1.2;
    }
    .hero-title span {
      color: #2563EB;
    }
    .hero-desc {
      color: #475569;
      font-size: 15px;
      line-height: 1.6;
    }
    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px;
      padding-top: 4px;
    }
    .btn-primary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #2563EB;
      color: #FFFFFF;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      text-decoration: none;
      box-shadow: 0 1px 2px rgba(37, 99, 235, 0.15);
      transition: background 0.15s ease;
    }
    .btn-primary:hover {
      background: #1D4ED8;
    }
    .btn-secondary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #FFFFFF;
      color: #334155;
      border: 1px solid #CBD5E1;
      padding: 9px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      text-decoration: none;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
      transition: all 0.15s ease;
    }
    .btn-secondary:hover {
      background: #F8FAFC;
      border-color: #94A3B8;
    }
    .btn-text {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: #64748B;
      font-size: 13px;
      font-weight: 500;
      text-decoration: none;
      padding: 8px 12px;
      transition: color 0.15s ease;
    }
    .btn-text:hover {
      color: #0F172A;
    }
    .status-meta-bar {
      margin-top: 24px;
      padding-top: 20px;
      border-top: 1px solid #F1F5F9;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      font-size: 12px;
    }
    @media (max-width: 768px) {
      .status-meta-bar { grid-template-columns: repeat(2, 1fr); }
    }
    .meta-col .meta-label {
      color: #94A3B8;
      display: block;
      font-size: 11px;
      font-weight: 500;
      margin-bottom: 2px;
    }
    .meta-col .meta-val {
      font-weight: 700;
      font-size: 13px;
    }
    /* Section Headers */
    .sec-header {
      margin-bottom: 14px;
    }
    .sec-title {
      font-size: 18px;
      font-weight: 800;
      color: #0F172A;
      letter-spacing: -0.02em;
    }
    .sec-subtitle {
      font-size: 12px;
      color: #64748B;
      margin-top: 2px;
    }
    /* Workflow Grid — Matching HomePage.jsx */
    .workflow-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }
    @media (max-width: 900px) {
      .workflow-grid { grid-template-columns: repeat(2, 1fr); }
    }
    @media (max-width: 600px) {
      .workflow-grid { grid-template-columns: 1fr; }
    }
    .workflow-card {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 18px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .wf-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .wf-icon-box {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: #EFF6FF;
      border: 1px solid #DBEAFE;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #2563EB;
    }
    .wf-icon-box svg {
      width: 16px;
      height: 16px;
      stroke: #2563EB;
    }
    .wf-step {
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      color: #94A3B8;
    }
    .wf-title {
      font-size: 14px;
      font-weight: 700;
      color: #0F172A;
      margin-bottom: 2px;
    }
    .wf-desc {
      font-size: 12px;
      color: #64748B;
      line-height: 1.5;
    }
    /* Taxonomy Section — Matching HomePage.jsx */
    .taxonomy-section {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 22px 24px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .taxonomy-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid #F1F5F9;
      padding-bottom: 14px;
      margin-bottom: 18px;
    }
    .tax-badge {
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      background: #ECFDF5;
      color: #047857;
      border: 1px solid #A7F3D0;
      border-radius: 6px;
    }
    .taxonomy-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
    }
    @media (max-width: 1024px) {
      .taxonomy-grid { grid-template-columns: repeat(3, 1fr); }
    }
    @media (max-width: 640px) {
      .taxonomy-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .tax-card {
      position: relative;
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 10px;
      padding: 14px;
      box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
      transition: all 0.15s ease;
    }
    .tax-card:hover {
      border-color: #60A5FA;
      box-shadow: 0 4px 8px rgba(37, 99, 235, 0.08);
      transform: translateY(-1px);
    }
    .tax-stripe {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 4px;
    }
    .tax-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
      padding-top: 2px;
    }
    .tax-id {
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      font-weight: 700;
      background: #F1F5F9;
      color: #475569;
      padding: 2px 6px;
      border-radius: 4px;
    }
    .tax-icon {
      font-size: 15px;
    }
    .tax-cat {
      font-size: 10px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: #94A3B8;
      margin-bottom: 2px;
    }
    .tax-name {
      font-size: 12px;
      font-weight: 700;
      color: #0F172A;
      line-height: 1.3;
    }
    .tax-bottom {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid #F1F5F9;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 4px;
    }
    .tax-bin-pill {
      font-size: 9px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
      color: #FFFFFF;
      white-space: nowrap;
    }
    .tax-bin-sub {
      font-size: 10px;
      color: #94A3B8;
      font-weight: 500;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    /* API Endpoints Section */
    .endpoints-section {
      background: #FFFFFF;
      border: 1px solid #E2E8F0;
      border-radius: 12px;
      padding: 22px 24px;
      box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    }
    .endpoints-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 8px;
    }
    .endpoints-table th {
      background: #F8FAFC;
      padding: 10px 14px;
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
    /* Footer */
    .footer {
      border-top: 1px solid #E2E8F0;
      padding: 24px;
      text-align: center;
      font-size: 12px;
      color: #64748B;
    }
  </style>
</head>
<body>

  <!-- Top Navbar Symmetrical with Frontend -->
  <header class="top-nav">
    <div class="nav-container">
      <a href="/" class="nav-brand">
        <div class="nav-logo">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/>
            <path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/>
            <path d="m14 16-3 3 3 3"/>
            <path d="M8.293 13.596 7.196 9.5 3.1 10.598"/>
            <path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843"/>
            <path d="m13.378 9.633 4.096 1.098 1.097-4.096"/>
          </svg>
        </div>
        <div class="nav-title">WasteSegregator <span>AI</span> <span class="nav-tag">Backend Service</span></div>
      </a>

      <div class="nav-actions">
        <div class="status-badge">
          <span class="pulse-dot"></span>
          <span>OPERATIONAL</span>
        </div>
        <a href="http://localhost:3000" target="_blank" class="nav-btn">
          <span>Web Client (Port 3000)</span>
          <span>→</span>
        </a>
      </div>
    </div>
  </header>

  <main class="main-wrap">

    <!-- Hero Section — Matched to HomePage.jsx -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="badge-pill">
          <span>Computer Vision &amp; Municipal Waste Sorting</span>
          <span>•</span>
          <span>Production Engine</span>
        </div>

        <h1 class="hero-title">
          WasteSegregator <span>AI</span>
        </h1>

        <p class="hero-desc">
          Real-time computer vision system that localizes waste items, identifies material types,
          and provides practical disposal and recycling recommendations to support municipal circularity.
        </p>

        <div class="hero-actions">
          <a href="http://localhost:3000/detect" target="_blank" class="btn-primary">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 7V5a2 2 0 0 1 2-2h2"/>
              <path d="M17 3h2a2 2 0 0 1 2 2v2"/>
              <path d="M21 17v2a2 2 0 0 1-2 2h-2"/>
              <path d="M7 21H5a2 2 0 0 1-2-2v-2"/>
              <line x1="7" x2="17" y1="12" y2="12"/>
            </svg>
            <span>Start Waste Detection</span>
            <span>→</span>
          </a>

          <a href="http://localhost:3000/dashboard" target="_blank" class="btn-secondary">
            View Analytics Dashboard
          </a>

          <a href="/api/health" class="btn-text">
            <span>System Architecture &amp; Health</span>
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>
              <polyline points="15 3 21 3 21 9"/>
              <line x1="10" x2="21" y1="14" y2="3"/>
            </svg>
          </a>
        </div>
      </div>

      <!-- Status Callout Bar — 4-Column Metadata Strip -->
      <div class="status-meta-bar">
        <div class="meta-col">
          <span class="meta-label">Model Architecture</span>
          <span class="meta-val" style="color: #1D4ED8;">{{ model_name }}</span>
        </div>
        <div class="meta-col">
          <span class="meta-label">Active Taxonomy</span>
          <span class="meta-val" style="color: #059669;">{{ classes_count }} / 15 Target Classes</span>
        </div>
        <div class="meta-col">
          <span class="meta-label">Hardware Acceleration</span>
          <span class="meta-val" style="color: #059669;">{{ hardware }}</span>
        </div>
        <div class="meta-col">
          <span class="meta-label">Database Storage</span>
          <span class="meta-val" style="color: #0F172A;">SQLite Connected</span>
        </div>
      </div>
    </section>

    <!-- System Workflow — Exact match to HomePage.jsx -->
    <section>
      <div class="sec-header">
        <h2 class="sec-title">System Workflow</h2>
        <p class="sec-subtitle">From image capture to automated sorting recommendations</p>
      </div>

      <div class="workflow-grid">
        <div class="workflow-card">
          <div class="wf-top">
            <div class="wf-icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><line x1="7" x2="17" y1="12" y2="12"/>
              </svg>
            </div>
            <span class="wf-step">01</span>
          </div>
          <div>
            <h3 class="wf-title">Image Acquisition</h3>
            <p class="wf-desc">Upload single or multi-object waste imagery via drag-and-drop, camera capture, or sample datasets.</p>
          </div>
        </div>

        <div class="workflow-card">
          <div class="wf-top">
            <div class="wf-icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" x2="9" y1="1" y2="4"/><line x1="15" x2="15" y1="1" y2="4"/><line x1="9" x2="9" y1="20" y2="23"/><line x1="15" x2="15" y1="20" y2="23"/><line x1="20" x2="23" y1="9" y2="9"/><line x1="20" x2="23" y1="14" y2="14"/><line x1="1" x2="4" y1="9" y2="9"/><line x1="1" x2="4" y1="14" y2="14"/>
              </svg>
            </div>
            <span class="wf-step">02</span>
          </div>
          <div>
            <h3 class="wf-title">YOLO Detection</h3>
            <p class="wf-desc">Inference engine localizes bounding boxes, material labels, and confidence metrics in real time.</p>
          </div>
        </div>

        <div class="workflow-card">
          <div class="wf-top">
            <div class="wf-icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M7 19H4.815a1.83 1.83 0 0 1-1.57-.881 1.785 1.785 0 0 1-.004-1.784L7.196 9.5"/><path d="M11 19h8.203a1.83 1.83 0 0 0 1.556-.89 1.784 1.784 0 0 0 0-1.775l-1.226-2.12"/><path d="m14 16-3 3 3 3"/><path d="M8.293 13.596 7.196 9.5 3.1 10.598"/><path d="m9.344 5.811 1.093-1.892A1.83 1.83 0 0 1 11.985 3a1.784 1.784 0 0 1 1.546.888l3.943 6.843"/><path d="m13.378 9.633 4.096 1.098 1.097-4.096"/>
              </svg>
            </div>
            <span class="wf-step">03</span>
          </div>
          <div>
            <h3 class="wf-title">Recommendation Engine</h3>
            <p class="wf-desc">Independent rule-based intelligence classifies objects into Recycle, Compost, Reuse, RDF, or Special Disposal.</p>
          </div>
        </div>

        <div class="workflow-card">
          <div class="wf-top">
            <div class="wf-icon-box">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>
              </svg>
            </div>
            <span class="wf-step">04</span>
          </div>
          <div>
            <h3 class="wf-title">Audit &amp; Analytics</h3>
            <p class="wf-desc">Structured sessions and metrics are committed to local SQLite storage for longitudinal environmental tracking.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 15-Class Target Taxonomy Overview — Exact match to HomePage.jsx -->
    <section class="taxonomy-section">
      <div class="taxonomy-head">
        <div>
          <h2 class="sec-title" style="font-size: 17px;">Standardized 15-Class Waste Taxonomy</h2>
          <p class="sec-subtitle">Ontology structure designed for automated waste sorting and circular materials recovery</p>
        </div>
        <span class="tax-badge">15 Active Categories</span>
      </div>

      <div class="taxonomy-grid">
        {% for cls in target_classes %}
          <div class="tax-card">
            <div class="tax-stripe" style="background-color: {{ cls.color }};"></div>
            <div>
              <div class="tax-top">
                <span class="tax-id">#{{ cls.id }}</span>
                <span class="tax-icon">{{ cls.icon }}</span>
              </div>
              <div class="tax-cat">{{ cls.category }}</div>
              <div class="tax-name">{{ cls.display }}</div>
            </div>
            <div class="tax-bottom">
              <span class="tax-bin-pill" style="background-color: {{ cls.color }};">
                {{ cls.bin.split('(')[0].strip() }}
              </span>
              <span class="tax-bin-sub">
                {% if '(' in cls.bin %}{{ cls.bin.split('(')[1].replace(')', '') }}{% endif %}
              </span>
            </div>
          </div>
        {% endfor %}
      </div>
    </section>

    <!-- Core API Endpoints Table -->
    <section class="endpoints-section">
      <div class="sec-header">
        <h2 class="sec-title" style="font-size: 17px;">Available REST API Endpoints</h2>
        <p class="sec-subtitle">Standard JSON and multipart endpoints exposed on port 5000</p>
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
            <td>Saved detection sessions &amp; audit records (paginated)</td>
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
    </section>

  </main>

  <footer class="footer">
    WasteSegregator AI • Municipal Circularity &amp; Computer Vision Engine • {{ timestamp }}
  </footer>

</body>
</html>"""

    return render_template_string(
        html,
        model_name=model_info.get("active_model_name", "YOLO11n Waste-15 Flagship"),
        classes_count=model_info.get("supported_classes_count", 15),
        hardware=model_info.get("device_display", "GPU Accelerated"),
        target_classes=taxonomy_cards,
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

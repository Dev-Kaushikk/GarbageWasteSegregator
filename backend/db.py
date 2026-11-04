"""
SQLite Database Layer for AI-Based Smart Garbage Waste Segregator
Handles persistence of detection sessions, detected objects, disposal recommendations,
and real analytical aggregations.
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

DB_DIR = Path(__file__).resolve().parent / "database"
DB_PATH = DB_DIR / "waste_segregator.db"

def get_db_connection() -> sqlite3.Connection:
    """Establish connection with row factory and foreign keys enabled."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialize database tables with indexes."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # 1. Detection Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detection_sessions (
                id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                original_image_path TEXT NOT NULL,
                annotated_image_path TEXT,
                thumbnail_path TEXT,
                file_size_bytes INTEGER DEFAULT 0,
                image_width INTEGER DEFAULT 0,
                image_height INTEGER DEFAULT 0,
                total_objects INTEGER DEFAULT 0,
                primary_category TEXT,
                primary_disposal TEXT,
                recyclability_rate REAL DEFAULT 0.0,
                processing_time_ms REAL DEFAULT 0.0,
                model_name TEXT,
                confidence_threshold REAL DEFAULT 0.20,
                summary_advice TEXT
            )
        """)

        # 2. Detected Objects Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detected_objects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                detection_order INTEGER DEFAULT 1,
                class_id INTEGER NOT NULL,
                class_name TEXT NOT NULL,
                confidence REAL NOT NULL,
                bbox_x1 REAL NOT NULL,
                bbox_y1 REAL NOT NULL,
                bbox_x2 REAL NOT NULL,
                bbox_y2 REAL NOT NULL,
                disposal_action TEXT NOT NULL,
                material TEXT,
                recommendation_json TEXT,
                FOREIGN KEY (session_id) REFERENCES detection_sessions(id) ON DELETE CASCADE
            )
        """)

        # Indexes for fast querying & analytics
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON detection_sessions(created_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_objects_session_id ON detected_objects(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_objects_class_name ON detected_objects(class_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_objects_disposal_action ON detected_objects(disposal_action)")

        conn.commit()

def save_detection_session(session_data: Dict[str, Any], detections: List[Dict[str, Any]]) -> str:
    """Save an entire detection session and its detected objects in a single transaction."""
    session_id = session_data["id"]
    now_iso = session_data.get("created_at") or datetime.utcnow().isoformat()

    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO detection_sessions (
                id, created_at, original_filename, original_image_path, annotated_image_path,
                thumbnail_path, file_size_bytes, image_width, image_height, total_objects,
                primary_category, primary_disposal, recyclability_rate, processing_time_ms,
                model_name, confidence_threshold, summary_advice
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            now_iso,
            session_data.get("original_filename", "image.jpg"),
            session_data.get("original_image_path", ""),
            session_data.get("annotated_image_path", ""),
            session_data.get("thumbnail_path", ""),
            session_data.get("file_size_bytes", 0),
            session_data.get("image_width", 0),
            session_data.get("image_height", 0),
            len(detections),
            session_data.get("primary_category", "Mixed Waste"),
            session_data.get("primary_disposal", "General waste"),
            session_data.get("recyclability_rate", 0.0),
            session_data.get("processing_time_ms", 0.0),
            session_data.get("model_name", "YOLO11n Baseline"),
            session_data.get("confidence_threshold", 0.20),
            session_data.get("summary_advice", "")
        ))

        for idx, det in enumerate(detections):
            bbox = det.get("bounding_box", {})
            rec = det.get("recommendation", {})
            cursor.execute("""
                INSERT INTO detected_objects (
                    session_id, detection_order, class_id, class_name, confidence,
                    bbox_x1, bbox_y1, bbox_x2, bbox_y2, disposal_action, material,
                    recommendation_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session_id,
                idx + 1,
                det.get("class_id", -1),
                det.get("class_name", "unknown"),
                float(det.get("confidence", 0.0)),
                float(bbox.get("x1", 0.0)),
                float(bbox.get("y1", 0.0)),
                float(bbox.get("x2", 0.0)),
                float(bbox.get("y2", 0.0)),
                rec.get("primary_action", "General waste"),
                rec.get("material_description", ""),
                json.dumps(rec)
            ))

        conn.commit()

    return session_id

def get_history(limit: int = 50, offset: int = 0, search: Optional[str] = None,
                category: Optional[str] = None, disposal: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """Retrieve paginated detection history with optional search and filters."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        query = "SELECT * FROM detection_sessions WHERE 1=1"
        params: List[Any] = []

        if search:
            query += " AND (original_filename LIKE ? OR summary_advice LIKE ?)"
            params.extend([f"%{search}%", f"%{search}%"])

        if category:
            query += " AND id IN (SELECT session_id FROM detected_objects WHERE class_name = ?)"
            params.append(category)

        if disposal:
            query += " AND primary_disposal = ?"
            params.append(disposal)

        # Count total matches
        count_query = query.replace("SELECT *", "SELECT COUNT(*)")
        cursor.execute(count_query, params)
        total_count = cursor.fetchone()[0]

        # Fetch records
        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()

        results = []
        for r in rows:
            session_id = r["id"]
            # Fetch distinct detected categories for this session
            cursor.execute("SELECT DISTINCT class_name, disposal_action FROM detected_objects WHERE session_id = ?", (session_id,))
            obj_rows = cursor.fetchall()
            categories = [o["class_name"] for o in obj_rows]

            results.append({
                "id": r["id"],
                "created_at": r["created_at"],
                "original_filename": r["original_filename"],
                "original_image_url": f"/api/uploads/{Path(r['original_image_path']).name}" if r["original_image_path"] else None,
                "annotated_image_url": f"/api/results/{Path(r['annotated_image_path']).name}" if r["annotated_image_path"] else None,
                "total_objects": r["total_objects"],
                "primary_category": r["primary_category"],
                "primary_disposal": r["primary_disposal"],
                "recyclability_rate": r["recyclability_rate"],
                "processing_time_ms": r["processing_time_ms"],
                "model_name": r["model_name"],
                "confidence_threshold": r["confidence_threshold"],
                "summary_advice": r["summary_advice"],
                "detected_categories": categories
            })

        return results, total_count

def get_session_by_id(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve single detection session with all detected objects and recommendations."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM detection_sessions WHERE id = ?", (session_id,))
        s_row = cursor.fetchone()
        if not s_row:
            return None

        cursor.execute("""
            SELECT * FROM detected_objects WHERE session_id = ? ORDER BY detection_order ASC
        """, (session_id,))
        obj_rows = cursor.fetchall()

        detections = []
        for o in obj_rows:
            rec = {}
            if o["recommendation_json"]:
                try:
                    rec = json.loads(o["recommendation_json"])
                except Exception:
                    pass

            detections.append({
                "detection_id": o["detection_order"],
                "class_id": o["class_id"],
                "class_name": o["class_name"],
                "confidence": o["confidence"],
                "bounding_box": {
                    "x1": o["bbox_x1"],
                    "y1": o["bbox_y1"],
                    "x2": o["bbox_x2"],
                    "y2": o["bbox_y2"]
                },
                "disposal_action": o["disposal_action"],
                "material": o["material"],
                "recommendation": rec
            })

        return {
            "id": s_row["id"],
            "created_at": s_row["created_at"],
            "original_filename": s_row["original_filename"],
            "original_image_url": f"/api/uploads/{Path(s_row['original_image_path']).name}" if s_row["original_image_path"] else None,
            "annotated_image_url": f"/api/results/{Path(s_row['annotated_image_path']).name}" if s_row["annotated_image_path"] else None,
            "image_width": s_row["image_width"],
            "image_height": s_row["image_height"],
            "total_objects": s_row["total_objects"],
            "primary_category": s_row["primary_category"],
            "primary_disposal": s_row["primary_disposal"],
            "recyclability_rate": s_row["recyclability_rate"],
            "processing_time_ms": s_row["processing_time_ms"],
            "model_name": s_row["model_name"],
            "confidence_threshold": s_row["confidence_threshold"],
            "summary_advice": s_row["summary_advice"],
            "detections": detections
        }

def delete_session(session_id: str) -> bool:
    """Delete session from SQLite and remove files on disk."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_image_path, annotated_image_path FROM detection_sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        if not row:
            return False

        orig_path = row["original_image_path"]
        annot_path = row["annotated_image_path"]

        # Delete database row (cascades to detected_objects)
        cursor.execute("DELETE FROM detection_sessions WHERE id = ?", (session_id,))
        conn.commit()

        # Delete files safely
        for p in [orig_path, annot_path]:
            if p and os.path.exists(p):
                try:
                    os.unlink(p)
                except Exception:
                    pass

        return True

def get_analytics_summary() -> Dict[str, Any]:
    """Calculate aggregated analytics across all recorded detection sessions."""
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Overall counts
        cursor.execute("""
            SELECT
                COUNT(id) as total_images,
                COALESCE(SUM(total_objects), 0) as total_objects,
                COALESCE(AVG(recyclability_rate), 0.0) as avg_recyclability,
                COALESCE(AVG(processing_time_ms), 0.0) as avg_latency
            FROM detection_sessions
        """)
        totals = cursor.fetchone()
        total_images = totals["total_images"]
        total_objects = totals["total_objects"]
        avg_recyclability = round(totals["avg_recyclability"], 1)
        avg_latency = round(totals["avg_latency"], 1)

        # Class frequency distribution
        cursor.execute("""
            SELECT class_name, COUNT(*) as count
            FROM detected_objects
            GROUP BY class_name
            ORDER BY count DESC
        """)
        class_distribution = [
            {"name": r["class_name"].replace("_", " ").title(), "class_name": r["class_name"], "count": r["count"]}
            for r in cursor.fetchall()
        ]

        # Disposal action distribution
        cursor.execute("""
            SELECT disposal_action, COUNT(*) as count
            FROM detected_objects
            GROUP BY disposal_action
            ORDER BY count DESC
        """)
        disposal_distribution = [
            {"action": r["disposal_action"], "count": r["count"]}
            for r in cursor.fetchall()
        ]

        # Top disposal actions count for dashboard cards
        disposal_map = {d["action"]: d["count"] for d in disposal_distribution}
        recycle_count = disposal_map.get("Recycle", 0)
        compost_count = disposal_map.get("Compost", 0)
        special_count = disposal_map.get("Special disposal", 0) + disposal_map.get("RDF potential", 0)

        # Daily detection trends (last 14 days with activity)
        cursor.execute("""
            SELECT
                SUBSTR(created_at, 1, 10) as date_str,
                COUNT(id) as session_count,
                SUM(total_objects) as object_count
            FROM detection_sessions
            GROUP BY date_str
            ORDER BY date_str ASC
            LIMIT 14
        """)
        daily_trends = [
            {"date": r["date_str"], "sessions": r["session_count"], "objects": r["object_count"]}
            for r in cursor.fetchall()
        ]

        # Recent 5 activity sessions
        cursor.execute("""
            SELECT id, created_at, original_filename, total_objects, primary_disposal, recyclability_rate
            FROM detection_sessions
            ORDER BY created_at DESC
            LIMIT 5
        """)
        recent_activity = [
            {
                "id": r["id"],
                "created_at": r["created_at"],
                "filename": r["original_filename"],
                "total_objects": r["total_objects"],
                "primary_disposal": r["primary_disposal"],
                "recyclability_rate": r["recyclability_rate"]
            }
            for r in cursor.fetchall()
        ]

        return {
            "total_images": total_images,
            "total_objects": total_objects,
            "avg_recyclability_rate": avg_recyclability,
            "avg_latency_ms": avg_latency,
            "recycle_count": recycle_count,
            "compost_count": compost_count,
            "special_disposal_count": special_count,
            "class_distribution": class_distribution,
            "disposal_distribution": disposal_distribution,
            "daily_trends": daily_trends,
            "recent_activity": recent_activity
        }


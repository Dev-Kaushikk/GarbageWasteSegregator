# Garbage Waste Segregator - Deployment Guide

## Deploying the Backend API

### Option 1: Docker Deployment (Recommended)
Create a `Dockerfile` in the project root:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ app.py ./app.py
COPY ../datasets/ ./datasets/
EXPOSE 5000
CMD ["python", "app.py"]
```
Build and run:
```bash
docker build -t garbage-waste-segregator-api .
docker run -p 5000:5000 garbage-waste-segregator-api
```

### Option 2: Systemd Service (Linux)
Create a systemd service file at `/etc/systemd/system/garbage-waste-segregator.service`:
```ini
[Unit]
Description=Garbage Waste Segregator API
After=network.target

[Service]
WorkingDirectory=/Users/devkaushik/Desktop/GarbageWasteSegregator/backend
ExecStart=/Users/devkaushik/Desktop/GarbageWasteSegregator/backend/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```
Enable with:
```bash
sudo systemctl enable garbage-waste-segregator.service
sudo systemctl start garbage-waste-segregator.service
```

### Option 3: Flask Run in Production
```bash
# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export JINJA_ENV=production

# Run with gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

## Deploying the Frontend

### Production Build
```bash
cd frontend
npm run build
```
Output will be in `frontend/build/`. Copy to your web server static directory.

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /path/to/garbage-waste-segregator/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Deploying to Cloud Services

### AWS Elastic Beanstalk
1. Navigate to `backend/` directory
2. Create `Procfile`:
   ```
   web: python app.py
   ```
3. Package with all dependencies
4. Upload to Elastic Beanstalk
5. Configure instance type and security groups
6. Set environment variables for DATABASE_URL, etc.

### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
2. Add `requirements.txt` dependencies
3. Push to Heroku:
   ```bash
   heroku create garbage-waste-segregator-api
   git push heroku main
   heroku config:set PORT=5000
   ```

### Render Platform
1. Create free tier account
2. Select Python + Flask platform
3. Connect GitHub repository
4. Set build command and start command
5. Configure environment variables

## Monitoring & Logging

### Enable CORS Debugging
Add logging middleware to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
app.logger.info('API started successfully')
```

### Performance Metrics
Monitor these key metrics:
- **API response time**: Should be < 100ms for data access
- **Training duration**: Based on epochs and batch size
- **Model size**: YOLO11n.pt is ~5.6MB (nano variant)
- **Memory usage**: Monitor during training runs

## Scaling Considerations

### Horizontal Scaling
- Backend: Multiple Flask instances behind nginx
- Database: PostgreSQL or SQLite for experiment tracking
- Load balancing: Nginx or HAProxy

### Vertical Scaling
- GPU: Use NVIDIA RTX 3090/4090 for faster training
- RAM: Minimum 16GB for 768px training batches
- Storage: SSD recommended for dataset loading speed

## Backup Strategy

### Dataset Backups
```bash
# Backup datasets directory
tar -czvf datasets_backup_$(date +%Y%m%d).tar.gz datasets/
```
Schedule via cron:
```bash
0 2 * * * tar -czvf /backups/datasets_$(date +\%Y\%m\%d).tar.gz /home/user/Desktop/GarbageWasteSegregator/datasets/
```

### Model Backups
```bash
# Backup model weights
cp models/yolo11n.pt /backups/yolo11n_backup_$(date +%Y%m%d).pt
```

## Security Considerations

### API Rate Limiting
Add rate limiting to prevent abuse:
```python
from flask_limiter import Limiter

limiter = Limiter(app, app.config['RATELIMIT_EX'] or '10 per minute')
```

### File Upload Validation
The predict endpoint should validate file types and sizes:
```python
ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']
MAX_SIZE = 10 * 1024 * 1024  # 10MB

if extension not in ALLOWED_EXTENSIONS:
    return jsonify({"error": "Invalid file type"}), 400
```

### CORS Configuration
Currently configured for same-origin development. For production, restrict origins:
```python
CORS(app, resources={r"/api/*": {"origins": ["https://yourdomain.com"]}})
```

import json
import os
import sys
from pathlib import Path

image_path = sys.argv[1] if len(sys.argv) > 1 else ''
model_path = sys.argv[2] if len(sys.argv) > 2 else ''

if not image_path or not os.path.exists(image_path):
    print(json.dumps({"detections": []}))
    sys.exit(0)

candidate_paths = []
if model_path:
    candidate_paths.append(model_path)

project_root = Path(__file__).resolve().parent.parent
candidate_paths.extend([
    str(project_root / 'models' / 'resistor_classifier.pt'),
    str(project_root / 'models' / 'resistor_detector.pt'),
    str(project_root / 'models' / 'best.pt'),
])

resolved_model = next((value for value in candidate_paths if value and os.path.exists(value)), '')
if not resolved_model:
    print(json.dumps({"detections": []}))
    sys.exit(0)

try:
    from ultralytics import YOLO

    model = YOLO(resolved_model)
    image_size = 224 if model.task == 'classify' else 640
    results = model(str(image_path), conf=0.25, imgsz=image_size, verbose=False)

    detections = []
    classification = None
    for result in results:
        if result.probs is not None:
            class_id = int(result.probs.top1)
            classification = {
                'label': str(result.names[class_id]),
                'confidence': float(result.probs.top1conf),
            }
            continue

        if result.boxes is None:
            continue

        boxes = result.boxes
        for index in range(len(boxes)):
            box = boxes[index]
            xyxy = box.xyxy[0].tolist()
            detections.append({
                'classId': int(box.cls[0]),
                'confidence': float(box.conf[0]),
                'box': {
                    'x1': float(xyxy[0]),
                    'y1': float(xyxy[1]),
                    'x2': float(xyxy[2]),
                    'y2': float(xyxy[3]),
                },
            })

    print(json.dumps({"detections": detections, "classification": classification}))
except Exception:
    print(json.dumps({"detections": []}))
    sys.exit(0)

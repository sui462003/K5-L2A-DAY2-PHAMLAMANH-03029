import sys, yaml
from pathlib import Path
from ultralytics import YOLO

img_dir = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

names = yaml.safe_load(open("data.yaml"))["names"]
if isinstance(names, list):
    names = dict(enumerate(names))
my_id = {v: k for k, v in names.items()}

COCO = {2: "car", 5: "bus", 7: "truck"}

model = YOLO("yolov8s.pt")
for p in sorted(list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))):
    r = model(str(p), conf=0.45, verbose=False)[0]
    lines = []
    for b in r.boxes:
        name = COCO.get(int(b.cls[0]))
        if name in my_id:
            x, y, w, h = b.xywhn[0].tolist()
            lines.append(f"{my_id[name]} {x:.6f} {y:.6f} {w:.6f} {h:.6f}")
    (out_dir / (p.stem + ".txt")).write_text("\n".join(lines))
    print(p.stem, len(lines))

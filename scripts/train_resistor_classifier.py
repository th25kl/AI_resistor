import argparse
import csv
import random
import shutil
from pathlib import Path

from ultralytics import YOLO


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
PROJECT_ROOT = Path(__file__).resolve().parent.parent


def discover_classes(source: Path, labels_file: Path) -> dict[str, list[Path]]:
    if not source.is_dir():
        raise FileNotFoundError(f'Image folder not found: {source}')
    if not labels_file.is_file():
        raise FileNotFoundError(f'Class labels CSV not found: {labels_file}')

    classes: dict[str, list[Path]] = {}
    with labels_file.open(newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if not {'image', 'class'}.issubset(reader.fieldnames or []):
            raise ValueError('The labels CSV must have image and class columns.')

        for row in reader:
            image_name = (row.get('image') or '').strip()
            class_name = (row.get('class') or '').strip()
            if not image_name or not class_name or Path(image_name).name != image_name:
                raise ValueError(f'Invalid image/class row in {labels_file}: {row}')

            image_path = source / image_name
            if image_path.suffix.lower() not in IMAGE_EXTENSIONS or not image_path.is_file():
                raise FileNotFoundError(f'Labeled image is missing: {image_path}')
            classes.setdefault(class_name, []).append(image_path)

    classes = {name: sorted(images) for name, images in classes.items()}
    if not classes:
        raise RuntimeError(f'No labeled images found in {labels_file}')

    too_small = [name for name, images in classes.items() if len(images) < 3]
    if too_small:
        raise RuntimeError(f'Each class needs at least 3 images; too few: {", ".join(too_small)}')

    return classes


def prepare_dataset(classes: dict[str, list[Path]], output: Path, seed: int, rebuild: bool) -> None:
    if output.exists():
        if not rebuild:
            raise FileExistsError(f'{output} already exists. Pass --rebuild to regenerate this dataset.')
        shutil.rmtree(output)

    rng = random.Random(seed)
    for class_name, images in classes.items():
        shuffled = list(images)
        rng.shuffle(shuffled)
        test_count = max(1, round(len(shuffled) * 0.1))
        val_count = max(1, round(len(shuffled) * 0.1))
        splits = {
            'test': shuffled[:test_count],
            'val': shuffled[test_count:test_count + val_count],
            'train': shuffled[test_count + val_count:],
        }

        for split_name, split_images in splits.items():
            destination = output / split_name / class_name
            destination.mkdir(parents=True, exist_ok=True)
            for source_image in split_images:
                target = destination / source_image.name
                try:
                    target.hardlink_to(source_image)
                except OSError:
                    shutil.copy2(source_image, target)

        print(f'{class_name}: {len(splits["train"])} train, {len(splits["val"])} val, {len(splits["test"])} test')


def main() -> None:
    parser = argparse.ArgumentParser(description='Train a resistor-value classifier from a flat image folder and labels CSV.')
    parser.add_argument('--source', type=Path, default=PROJECT_ROOT / 'resistor_dataset', help='Folder containing the resistor images.')
    parser.add_argument('--labels', type=Path, default=PROJECT_ROOT / 'resistor_dataset_labels.csv', help='CSV file with image and class columns.')
    parser.add_argument('--data', type=Path, default=PROJECT_ROOT / 'training-data' / 'resistor-values', help='Generated train/val/test dataset directory.')
    parser.add_argument('--weights', type=Path, default=PROJECT_ROOT / 'models' / 'resistor_classifier.pt', help='Output model weights path.')
    parser.add_argument('--epochs', type=int, default=50)
    parser.add_argument('--imgsz', type=int, default=224)
    parser.add_argument('--batch', type=int, default=16)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--rebuild', action='store_true', help='Recreate the generated dataset directory if it already exists.')
    args = parser.parse_args()

    source = args.source.resolve()
    labels_file = args.labels.resolve()
    data_dir = args.data.resolve()
    weights_path = args.weights.resolve()
    classes = discover_classes(source, labels_file)
    print(f'Found {len(classes)} resistor classes and {sum(map(len, classes.values()))} images.')
    prepare_dataset(classes, data_dir, args.seed, args.rebuild)

    model = YOLO('yolo11n-cls.pt')
    model.train(
        data=str(data_dir),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        patience=10,
        seed=args.seed,
        project=str(PROJECT_ROOT / 'runs' / 'classify'),
        name='resistor-values',
        exist_ok=True,
    )

    best_weights = PROJECT_ROOT / 'runs' / 'classify' / 'resistor-values' / 'weights' / 'best.pt'
    if not best_weights.is_file():
        raise FileNotFoundError(f'Training finished without producing {best_weights}')

    weights_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best_weights, weights_path)
    print(f'Trained classifier saved to: {weights_path}')

    trained_model = YOLO(str(weights_path))
    metrics = trained_model.val(data=str(data_dir), split='test', imgsz=args.imgsz)
    print(f'Test top-1 accuracy: {metrics.top1:.4f}')


if __name__ == '__main__':
    main()
from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("yolo11n-obb.yalm")

# Train the model on the COCO8 dataset for 100 epochs
train_results = model.train(
    data="./yolu_dataset/data.yaml",  # Path to dataset configuration file
    epochs=30,  # Number of training epochs
    imgsz=1280,  # Image size for training
    device="cpu",  # Device to run on (e.g., 'cpu', 0, [0,1,2,3])
    workers=8,  # Number of data loading workers
    pretreined=True,  # Use a pretrained model
    
)

# Evaluate the model's performance on the validation set
metrics = model.val()

# Perform object detection on an image
results = model("path/to/image.jpg")  # Predict on an image
results[0].show()  # Display results

# Export the model to ONNX format for deployment
path = model.export(format="onnx")  # Returns the path to the exported model
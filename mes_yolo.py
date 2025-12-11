# from ultralytics import YOLO
# model = YOLO(model= 'yolo11n.pt', task='detect')

# model.train(data="C:\\Users\\user\\Desktop\\masterHyun\\project\\python\\visionServer\\MES_lower_frame-2\\data.yaml",
#             epochs=30, batch=16, device="cpu")


from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(model='yolov8n.pt', task='detect')

    model.train(
        data="C:\\Users\\user\\Desktop\\masterHyun\\project\\python\\visionServer\\MES_lower_frame-2\\data.yaml",
        epochs=30,
        batch=16,
        device=0  # GPU 사용
    )

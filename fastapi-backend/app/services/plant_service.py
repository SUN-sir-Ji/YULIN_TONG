from ultralytics import YOLO
import os
from app.config.config import UPLOAD_DIR

# 加载YOLO模型（在应用启动时只加载一次）
model = YOLO("best.pt")  # 确保模型文件在正确路径

# 图片处理函数
def process_image_recognition(file_path: str):
    # 使用模型进行预测
    results = model.predict(source=file_path, save=False, conf=0)  # conf是置信度阈值
    
    # 处理预测结果
    recognition_results = []
    for result in results:
        # 优先尝试获取分类结果（适用于分类模型）
        if hasattr(result, 'probs') and result.probs is not None:
            # 获取所有类别的概率，确保转换为Python原生类型
            probs = result.probs.data.cpu().numpy().tolist()
            # 获取类别名称
            names = result.names
            
            # 获取置信度最高的前5个类别及其索引
            top5_indices = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)[:5]
            
            # 提取前5个结果
            for idx in top5_indices:
                class_id = names[idx]
                # 确保confidence是Python原生float类型
                confidence = float(probs[idx])
                
                # 只添加置信度大于0的结果
                if confidence > 0:
                    recognition_results.append({
                        "class": str(class_id),  # 确保class_id是字符串类型
                        "confidence": round(confidence, 2)  # 四舍五入保留2位小数
                    })
        # 同时保留原有的目标检测逻辑作为备选
        elif hasattr(result, 'boxes') and result.boxes is not None:
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                confidence = float(box.conf[0].item())  # 转换为Python float
                
                recognition_results.append({
                    "class": str(class_id),  # 确保是字符串类型
                    "confidence": round(confidence, 2)
                })
        
        # 如果没有检测到任何结果，添加默认提示
        if not recognition_results:
            recognition_results.append({
                "class": "未检测到对象",
                "confidence": 0.0,  # 使用浮点数0.0而不是整数0
            })
    
    # 添加打印语句，在控制台查看recognition_results的值
    print("=== 识别结果信息 ===")
    print(f"检测到的对象数量: {len(recognition_results)}")
    for i, item in enumerate(recognition_results):
        print(f"对象 {i+1}:")
        print(f"  类别: {item['class']}")
        print(f"  置信度: {item['confidence']}")
    print("====================")
    
    return recognition_results
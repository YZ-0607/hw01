# 1. 导入依赖库
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import seaborn as sns
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# ---------------------- 2. 路径配置 ----------------------
# Kaggle环境数据集路径，本地运行修改为你的文件夹路径
root_path = "/kaggle/input/chest-xray-pneumonia/chest_xray"
train_dir = os.path.join(root_path, "train")
test_dir = os.path.join(root_path, "test")

# 超参数设置
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15

# ---------------------- 3. 数据增强与预处理 ----------------------
# 训练集增强：缓解过拟合
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=15,
    horizontal_flip=True,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    validation_split=0.2 # 直接划分20%为验证集，替代原生val
)

# 测试集仅归一化，不增强
test_datagen = ImageDataGenerator(rescale=1./255)

# 加载训练+自建验证集
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training",
    shuffle=True
)

val_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation",
    shuffle=False
)

# 独立测试集
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="binary",
    shuffle=False
)

# ---------------------- 4. 搭建简易CNN模型 ----------------------
model = Sequential([
    # 卷积块1
    Conv2D(32, (3,3), activation="relu", input_shape=(224,224,3)),
    MaxPooling2D(2,2),
    # 卷积块2
    Conv2D(64, (3,3), activation="relu"),
    MaxPooling2D(2,2),
    # 卷积块3
    Conv2D(128, (3,3), activation="relu"),
    MaxPooling2D(2,2),
    # 卷积块4
    Conv2D(256, (3,3), activation="relu"),
    MaxPooling2D(2,2),
    # 全连接层
    Flatten(),
    Dropout(0.4),
    Dense(128, activation="relu"),
    Dense(1, activation="sigmoid") # 二分类输出
])

# 模型编译
model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)
model.summary()

# ---------------------- 5. 模型训练 ----------------------
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator
)

# ---------------------- 6. 绘制Loss/Acc曲线并保存 ----------------------
plt.figure(figsize=(12,4))
# 损失曲线
plt.subplot(1,2,1)
plt.plot(history.history["loss"], label="Train Loss")
plt.plot(history.history["val_loss"], label="Val Loss")
plt.title("Loss Curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
# 准确率曲线
plt.subplot(1,2,2)
plt.plot(history.history["accuracy"], label="Train Acc")
plt.plot(history.history["val_accuracy"], label="Val Acc")
plt.title("Accuracy Curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.tight_layout()
plt.savefig("output_plots/loss_acc_curve.png", dpi=300)
plt.show()

# ---------------------- 7. 测试集预测与指标计算 ----------------------
y_true = test_generator.classes
y_pred_prob = model.predict(test_generator)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# 计算四大指标
acc = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)

print("===== 测试集评估指标 =====")
print(f"准确率Accuracy: {acc:.4f}")
print(f"精确率Precision: {precision:.4f}")
print(f"召回率Recall: {recall:.4f}")
print(f"F1分数: {f1:.4f}")

# 绘制混淆矩阵
cm = confusion_matrix(y_true, y_pred)
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Normal","Pneumonia"], yticklabels=["Normal","Pneumonia"])
plt.xlabel("预测标签")
plt.ylabel("真实标签")
plt.title("Confusion Matrix")
plt.savefig("output_plots/confusion_matrix.png", dpi=300)
plt.show()
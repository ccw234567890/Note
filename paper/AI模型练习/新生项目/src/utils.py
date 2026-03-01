# Copyright 2020 Huawei Technologies Co., Ltd
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Utility functions for training and inference."""

import os
import random
import numpy as np
import mindspore as ms
from mindspore import context, Tensor
from mindspore.train.serialization import export
from mindspore import ops
import matplotlib.pyplot as plt
from PIL import Image

def context_device_init(config):
    """Initialize context and device."""
    context.set_context(mode=config.mode, device_target=config.device_target, device_id=config.device_id)
    print(f"Context initialized: mode={config.mode}, device_target={config.device_target}, device_id={config.device_id}")


def export_mindir(net, model_name):
    """Export model to MindIR format."""
    print(f"Exporting model to {model_name}.mindir...")
    
    # 创建输入数据
    input_data = Tensor(np.random.randn(1, 3, 224, 224), ms.float32)
    
    # 导出模型
    export(net, input_data, file_name=model_name, file_format="MINDIR")
    print(f"Model exported successfully: {model_name}.mindir")


def predict_from_net(net, test_list, config, show_title="prediction"):
    """Predict and visualize results from network."""
    print(f"Making predictions: {show_title}")
    
    # 设置网络为评估模式
    net.set_train(False)
    
    # 随机选择几张图片进行预测
    num_samples = min(4, len(test_list))
    sample_indices = random.sample(range(len(test_list)), num_samples)
    
    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    axes = axes.flatten()
    
    for i, idx in enumerate(sample_indices):
        if i >= 4:
            break
            
        # 加载图片
        img_path = test_list[idx]
        img = Image.open(img_path)
        
        # 预处理图片
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = (img_array - np.array([0.485, 0.456, 0.406])) / np.array([0.229, 0.224, 0.225])
        img_tensor = Tensor(img_array.transpose(2, 0, 1), ms.float32).unsqueeze(0)
        
        # 预测
        output = net(img_tensor)
        probabilities = ops.Softmax()(output)
        predicted_class = probabilities.argmax(axis=1).asnumpy()[0]
        confidence = probabilities.max(axis=1).asnumpy()[0]
        
        # 显示结果
        class_names = ['Cat', 'Dog']
        predicted_name = class_names[predicted_class]
        
        axes[i].imshow(img)
        axes[i].set_title(f'{predicted_name} ({confidence:.2f})')
        axes[i].axis('off')
    
    # 隐藏多余的子图
    for i in range(num_samples, 4):
        axes[i].axis('off')
    
    plt.suptitle(show_title)
    plt.tight_layout()
    plt.show()
    
    print(f"Prediction completed: {show_title}")


def get_samples_from_eval_dataset(dataset_path):
    """Get sample images from evaluation dataset."""
    eval_path = os.path.join(dataset_path, "eval")
    sample_list = []
    
    # 获取猫的图片
    cat_path = os.path.join(eval_path, "cat")
    if os.path.exists(cat_path):
        cat_files = [os.path.join(cat_path, f) for f in os.listdir(cat_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        sample_list.extend(cat_files[:2])  # 取前2张
    
    # 获取狗的图片
    dog_path = os.path.join(eval_path, "dog")
    if os.path.exists(dog_path):
        dog_files = [os.path.join(dog_path, f) for f in os.listdir(dog_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        sample_list.extend(dog_files[:2])  # 取前2张
    
    return sample_list


def save_checkpoint(net, epoch, loss, checkpoint_path):
    """Save model checkpoint."""
    os.makedirs(checkpoint_path, exist_ok=True)
    checkpoint_file = os.path.join(checkpoint_path, f"checkpoint_epoch_{epoch}.ckpt")
    ms.save_checkpoint(net, checkpoint_file)
    print(f"Checkpoint saved: {checkpoint_file}")


def load_checkpoint(net, checkpoint_path):
    """Load model checkpoint."""
    if os.path.exists(checkpoint_path):
        param_dict = ms.load_checkpoint(checkpoint_path)
        ms.load_param_into_net(net, param_dict)
        print(f"Checkpoint loaded: {checkpoint_path}")
        return True
    else:
        print(f"Checkpoint not found: {checkpoint_path}")
        return False


def calculate_accuracy(predictions, labels):
    """Calculate accuracy."""
    predictions = predictions.asnumpy()
    labels = labels.asnumpy()
    
    if len(predictions.shape) > 1:
        predictions = predictions.argmax(axis=1)
    
    correct = (predictions == labels).sum()
    total = len(labels)
    accuracy = correct / total
    
    return accuracy


def plot_training_curves(train_losses, val_losses, train_accs, val_accs, save_path=None):
    """Plot training curves."""
    epochs = range(1, len(train_losses) + 1)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # 损失曲线
    ax1.plot(epochs, train_losses, 'b-', label='Training Loss')
    ax1.plot(epochs, val_losses, 'r-', label='Validation Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)
    
    # 准确率曲线
    ax2.plot(epochs, train_accs, 'b-', label='Training Accuracy')
    ax2.plot(epochs, val_accs, 'r-', label='Validation Accuracy')
    ax2.set_title('Training and Validation Accuracy')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        print(f"Training curves saved to: {save_path}")
    
    plt.show()


def convert_to_onnx(net, model_name, input_shape=(1, 3, 224, 224)):
    """Convert model to ONNX format."""
    print(f"Converting model to ONNX format: {model_name}.onnx")
    
    # 创建输入数据
    input_data = Tensor(np.random.randn(*input_shape), ms.float32)
    
    # 导出为ONNX
    export(net, input_data, file_name=model_name, file_format="ONNX")
    print(f"ONNX model exported: {model_name}.onnx")


def benchmark_model(net, input_shape=(1, 3, 224, 224), num_iterations=100):
    """Benchmark model inference speed."""
    print(f"Benchmarking model with {num_iterations} iterations...")
    
    # 创建输入数据
    input_data = Tensor(np.random.randn(*input_shape), ms.float32)
    
    # 预热
    for _ in range(10):
        _ = net(input_data)
    
    # 计时
    import time
    start_time = time.time()
    
    for _ in range(num_iterations):
        _ = net(input_data)
    
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time / num_iterations
    fps = 1.0 / avg_time
    
    print(f"Benchmark results:")
    print(f"  Total time: {total_time:.4f}s")
    print(f"  Average time per inference: {avg_time:.4f}s")
    print(f"  FPS: {fps:.2f}")
    
    return avg_time, fps

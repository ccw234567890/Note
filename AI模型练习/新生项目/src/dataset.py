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

"""Dataset processing utilities."""

import os
import numpy as np
import mindspore as ms
import mindspore.dataset as ds
from mindspore import Tensor
from mindspore.dataset.vision import RandomCropDecodeResize, RandomHorizontalFlip, Normalize, HWC2CHW
from mindspore.dataset.transforms import TypeCast

def create_dataset(dataset_path, config, is_training=True):
    """Create dataset for training or evaluation."""
    
    # 数据增强配置
    if is_training:
        transforms = [
            RandomCropDecodeResize(size=config.image_size, scale=(0.08, 1.0), ratio=(0.75, 1.333)),
            RandomHorizontalFlip(prob=0.5),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            HWC2CHW(),
            TypeCast(ms.float32)
        ]
    else:
        transforms = [
            RandomCropDecodeResize(size=config.image_size),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            HWC2CHW(),
            TypeCast(ms.float32)
        ]
    
    # 创建数据集
    dataset = ds.ImageFolderDataset(
        dataset_path,
        num_parallel_workers=config.num_parallel_workers,
        shuffle=is_training,
        decode=True
    )
    
    # 应用变换
    dataset = dataset.map(operations=transforms, input_columns="image")
    dataset = dataset.batch(config.batch_size, drop_remainder=True)
    
    return dataset


def extract_features(backbone_net, dataset_path, config):
    """Extract features using backbone network and cache them."""
    print("Extracting features...")
    
    # 创建数据集
    train_dataset = create_dataset(os.path.join(dataset_path, "train"), config, is_training=False)
    eval_dataset = create_dataset(os.path.join(dataset_path, "eval"), config, is_training=False)
    
    # 设置网络为评估模式
    backbone_net.set_train(False)
    
    # 提取训练集特征
    train_features = []
    train_labels = []
    for data, label in train_dataset:
        features = backbone_net(data)
        train_features.append(features.asnumpy())
        train_labels.append(label.asnumpy())
    
    # 提取验证集特征
    eval_features = []
    eval_labels = []
    for data, label in eval_dataset:
        features = backbone_net(data)
        eval_features.append(features.asnumpy())
        eval_labels.append(label.asnumpy())
    
    # 合并所有特征
    train_features = np.concatenate(train_features, axis=0)
    train_labels = np.concatenate(train_labels, axis=0)
    eval_features = np.concatenate(eval_features, axis=0)
    eval_labels = np.concatenate(eval_labels, axis=0)
    
    print(f"Extracted features - Train: {train_features.shape}, Eval: {eval_features.shape}")
    
    # 计算步数
    step_size = len(train_features) // config.batch_size
    
    return (train_features, train_labels, eval_features, eval_labels), step_size


def preprocess_dataset(dataset_path, output_path):
    """Preprocess dataset: clean and split data."""
    import shutil
    from PIL import Image
    
    # 创建输出目录
    os.makedirs(os.path.join(output_path, "train", "cat"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "train", "dog"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "eval", "cat"), exist_ok=True)
    os.makedirs(os.path.join(output_path, "eval", "dog"), exist_ok=True)
    
    # 处理猫的图片
    cat_dir = os.path.join(dataset_path, "Cat")
    dog_dir = os.path.join(dataset_path, "Dog")
    
    # 清理和分割猫的图片
    cat_files = [f for f in os.listdir(cat_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    np.random.shuffle(cat_files)
    
    train_cat = cat_files[:int(len(cat_files) * 0.8)]
    eval_cat = cat_files[int(len(cat_files) * 0.8):]
    
    for i, filename in enumerate(train_cat):
        try:
            img_path = os.path.join(cat_dir, filename)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(os.path.join(output_path, "train", "cat", f"cat_{i:04d}.jpg"))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    for i, filename in enumerate(eval_cat):
        try:
            img_path = os.path.join(cat_dir, filename)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(os.path.join(output_path, "eval", "cat", f"cat_{i:04d}.jpg"))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    # 清理和分割狗的图片
    dog_files = [f for f in os.listdir(dog_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    np.random.shuffle(dog_files)
    
    train_dog = dog_files[:int(len(dog_files) * 0.8)]
    eval_dog = dog_files[int(len(dog_files) * 0.8):]
    
    for i, filename in enumerate(train_dog):
        try:
            img_path = os.path.join(dog_dir, filename)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(os.path.join(output_path, "train", "dog", f"dog_{i:04d}.jpg"))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    for i, filename in enumerate(eval_dog):
        try:
            img_path = os.path.join(dog_dir, filename)
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(os.path.join(output_path, "eval", "dog", f"dog_{i:04d}.jpg"))
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    print("Dataset preprocessing completed!")
    print(f"Train cats: {len(train_cat)}, Train dogs: {len(train_dog)}")
    print(f"Eval cats: {len(eval_cat)}, Eval dogs: {len(eval_dog)}")

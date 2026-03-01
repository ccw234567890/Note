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

"""Dataset preprocessing script for cat-dog classification."""

import os
import shutil
import random
from PIL import Image
import argparse

def clean_and_split_dataset(input_path, output_path, train_ratio=0.8):
    """
    Clean and split the cat-dog dataset.
    
    Args:
        input_path: Path to the original dataset
        output_path: Path to save the processed dataset
        train_ratio: Ratio of training data
    """
    print("Starting dataset preprocessing...")
    
    # 创建输出目录结构
    train_cat_dir = os.path.join(output_path, "train", "cat")
    train_dog_dir = os.path.join(output_path, "train", "dog")
    eval_cat_dir = os.path.join(output_path, "eval", "cat")
    eval_dog_dir = os.path.join(output_path, "eval", "dog")
    
    for dir_path in [train_cat_dir, train_dog_dir, eval_cat_dir, eval_dog_dir]:
        os.makedirs(dir_path, exist_ok=True)
    
    # 处理猫的图片
    cat_dir = os.path.join(input_path, "Cat")
    if os.path.exists(cat_dir):
        process_cat_images(cat_dir, train_cat_dir, eval_cat_dir, train_ratio)
    else:
        print(f"Warning: Cat directory not found at {cat_dir}")
    
    # 处理狗的图片
    dog_dir = os.path.join(input_path, "Dog")
    if os.path.exists(dog_dir):
        process_dog_images(dog_dir, train_dog_dir, eval_dog_dir, train_ratio)
    else:
        print(f"Warning: Dog directory not found at {dog_dir}")
    
    print("Dataset preprocessing completed!")


def process_cat_images(input_dir, train_dir, eval_dir, train_ratio):
    """Process cat images."""
    print("Processing cat images...")
    
    # 获取所有图片文件
    image_files = [f for f in os.listdir(input_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    
    print(f"Found {len(image_files)} cat images")
    
    # 随机打乱
    random.shuffle(image_files)
    
    # 分割训练和验证集
    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    eval_files = image_files[split_idx:]
    
    # 处理训练集
    train_count = 0
    for filename in train_files:
        if process_image(os.path.join(input_dir, filename), 
                        os.path.join(train_dir, f"cat_{train_count:04d}.jpg")):
            train_count += 1
    
    # 处理验证集
    eval_count = 0
    for filename in eval_files:
        if process_image(os.path.join(input_dir, filename), 
                        os.path.join(eval_dir, f"cat_{eval_count:04d}.jpg")):
            eval_count += 1
    
    print(f"Cat images processed - Train: {train_count}, Eval: {eval_count}")


def process_dog_images(input_dir, train_dir, eval_dir, train_ratio):
    """Process dog images."""
    print("Processing dog images...")
    
    # 获取所有图片文件
    image_files = [f for f in os.listdir(input_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
    
    print(f"Found {len(image_files)} dog images")
    
    # 随机打乱
    random.shuffle(image_files)
    
    # 分割训练和验证集
    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    eval_files = image_files[split_idx:]
    
    # 处理训练集
    train_count = 0
    for filename in train_files:
        if process_image(os.path.join(input_dir, filename), 
                        os.path.join(train_dir, f"dog_{train_count:04d}.jpg")):
            train_count += 1
    
    # 处理验证集
    eval_count = 0
    for filename in eval_files:
        if process_image(os.path.join(input_dir, filename), 
                        os.path.join(eval_dir, f"dog_{eval_count:04d}.jpg")):
            eval_count += 1
    
    print(f"Dog images processed - Train: {train_count}, Eval: {eval_count}")


def process_image(input_path, output_path):
    """
    Process a single image: resize, convert format, and save.
    
    Args:
        input_path: Path to input image
        output_path: Path to save processed image
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # 打开图片
        with Image.open(input_path) as img:
            # 转换为RGB格式
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 调整大小到224x224
            img = img.resize((224, 224), Image.Resampling.LANCZOS)
            
            # 保存图片
            img.save(output_path, 'JPEG', quality=95)
            
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Preprocess cat-dog dataset')
    parser.add_argument('--input_path', type=str, required=True,
                       help='Path to the original dataset directory')
    parser.add_argument('--output_path', type=str, required=True,
                       help='Path to save the processed dataset')
    parser.add_argument('--train_ratio', type=float, default=0.8,
                       help='Ratio of training data (default: 0.8)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility (default: 42)')
    
    args = parser.parse_args()
    
    # 设置随机种子
    random.seed(args.seed)
    
    # 验证输入路径
    if not os.path.exists(args.input_path):
        print(f"Error: Input path {args.input_path} does not exist")
        return
    
    # 创建输出目录
    os.makedirs(args.output_path, exist_ok=True)
    
    # 开始处理
    clean_and_split_dataset(args.input_path, args.output_path, args.train_ratio)
    
    print(f"Dataset preprocessing completed!")
    print(f"Processed dataset saved to: {args.output_path}")


if __name__ == '__main__':
    main()


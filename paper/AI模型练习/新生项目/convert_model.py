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

"""Model conversion script for deployment."""

import os
import argparse
import mindspore as ms
from mindspore import context, Tensor
from mindspore.train.serialization import load_checkpoint, load_param_into_net
from src.models import define_net, define_net_resnet, define_net_vit
from src.config import Config

def convert_to_mindir(model_path, output_path, model_type="mobilenetv2"):
    """
    Convert trained model to MindIR format.
    
    Args:
        model_path: Path to the trained model checkpoint
        output_path: Path to save the converted model
        model_type: Type of model (mobilenetv2, resnet, vit)
    """
    print(f"Converting {model_type} model to MindIR format...")
    
    # 设置上下文
    context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
    
    # 创建配置
    config = Config()
    config.num_classes = 2
    config.image_size = 224
    
    # 根据模型类型选择网络定义函数
    if model_type == "mobilenetv2":
        _, _, net = define_net(config, activation="Softmax")
    elif model_type == "resnet":
        _, _, net = define_net_resnet(config, activation="Softmax")
    elif model_type == "vit":
        _, _, net = define_net_vit(config, activation="Softmax")
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    # 加载训练好的权重
    if os.path.exists(model_path):
        param_dict = load_checkpoint(model_path)
        load_param_into_net(net, param_dict)
        print(f"Loaded checkpoint from {model_path}")
    else:
        print(f"Warning: Checkpoint {model_path} not found, using pretrained weights")
    
    # 创建输入数据
    input_data = Tensor(ms.numpy.random.randn(1, 3, 224, 224), ms.float32)
    
    # 导出为MindIR格式
    ms.export(net, input_data, file_name=output_path, file_format="MINDIR")
    print(f"Model converted successfully: {output_path}.mindir")


def convert_to_onnx(model_path, output_path, model_type="mobilenetv2"):
    """
    Convert trained model to ONNX format.
    
    Args:
        model_path: Path to the trained model checkpoint
        output_path: Path to save the converted model
        model_type: Type of model (mobilenetv2, resnet, vit)
    """
    print(f"Converting {model_type} model to ONNX format...")
    
    # 设置上下文
    context.set_context(mode=context.GRAPH_MODE, device_target="CPU")
    
    # 创建配置
    config = Config()
    config.num_classes = 2
    config.image_size = 224
    
    # 根据模型类型选择网络定义函数
    if model_type == "mobilenetv2":
        _, _, net = define_net(config, activation="Softmax")
    elif model_type == "resnet":
        _, _, net = define_net_resnet(config, activation="Softmax")
    elif model_type == "vit":
        _, _, net = define_net_vit(config, activation="Softmax")
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    # 加载训练好的权重
    if os.path.exists(model_path):
        param_dict = load_checkpoint(model_path)
        load_param_into_net(net, param_dict)
        print(f"Loaded checkpoint from {model_path}")
    else:
        print(f"Warning: Checkpoint {model_path} not found, using pretrained weights")
    
    # 创建输入数据
    input_data = Tensor(ms.numpy.random.randn(1, 3, 224, 224), ms.float32)
    
    # 导出为ONNX格式
    ms.export(net, input_data, file_name=output_path, file_format="ONNX")
    print(f"Model converted successfully: {output_path}.onnx")


def convert_to_lite(model_path, output_path, model_type="mobilenetv2"):
    """
    Convert MindIR model to MindSpore Lite format.
    
    Args:
        model_path: Path to the MindIR model file
        output_path: Path to save the Lite model
        model_type: Type of model (mobilenetv2, resnet, vit)
    """
    print(f"Converting {model_type} model to MindSpore Lite format...")
    
    # 检查MindIR文件是否存在
    mindir_path = f"{model_path}.mindir"
    if not os.path.exists(mindir_path):
        print(f"Error: MindIR file {mindir_path} not found")
        return
    
    # 使用converter_lite工具进行转换
    # 这里需要调用MindSpore Lite的转换工具
    # 实际使用时需要根据MindSpore Lite的文档进行配置
    
    print("Note: MindSpore Lite conversion requires converter_lite tool")
    print(f"Please use converter_lite to convert {mindir_path} to {output_path}.ms")
    print("Example command:")
    print(f"converter_lite --fmk=MINDIR --modelFile={mindir_path} --outputFile={output_path}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Convert trained models for deployment')
    parser.add_argument('--model_path', type=str, required=True,
                       help='Path to the trained model checkpoint')
    parser.add_argument('--output_path', type=str, required=True,
                       help='Path to save the converted model')
    parser.add_argument('--model_type', type=str, default='mobilenetv2',
                       choices=['mobilenetv2', 'resnet', 'vit'],
                       help='Type of model to convert')
    parser.add_argument('--format', type=str, default='mindir',
                       choices=['mindir', 'onnx', 'lite'],
                       help='Output format for conversion')
    
    args = parser.parse_args()
    
    # 验证输入路径
    if not os.path.exists(args.model_path):
        print(f"Error: Model path {args.model_path} does not exist")
        return
    
    # 创建输出目录
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    
    # 根据格式进行转换
    if args.format == 'mindir':
        convert_to_mindir(args.model_path, args.output_path, args.model_type)
    elif args.format == 'onnx':
        convert_to_onnx(args.model_path, args.output_path, args.model_type)
    elif args.format == 'lite':
        convert_to_lite(args.model_path, args.output_path, args.model_type)
    else:
        print(f"Error: Unsupported format {args.format}")


if __name__ == '__main__':
    main()


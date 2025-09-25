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

"""Learning rate generation utilities."""

import math
import numpy as np

def get_lr(global_step, lr_init, lr_end, lr_max, warmup_epochs, total_epochs, steps_per_epoch):
    """
    Generate learning rate array.
    
    Args:
        global_step: Current global step
        lr_init: Initial learning rate
        lr_end: Final learning rate
        lr_max: Maximum learning rate
        warmup_epochs: Number of warmup epochs
        total_epochs: Total number of epochs
        steps_per_epoch: Number of steps per epoch
    
    Returns:
        Learning rate array
    """
    lr = []
    total_steps = steps_per_epoch * total_epochs
    warmup_steps = steps_per_epoch * warmup_epochs
    
    for i in range(total_steps):
        if i < warmup_steps:
            # Warmup阶段：线性增长
            lr.append(lr_init + (lr_max - lr_init) * i / warmup_steps)
        else:
            # 余弦退火阶段
            progress = (i - warmup_steps) / (total_steps - warmup_steps)
            lr.append(lr_end + (lr_max - lr_end) * 0.5 * (1 + math.cos(math.pi * progress)))
    
    return np.array(lr, dtype=np.float32)


def get_lr_cosine(global_step, lr_init, lr_end, total_epochs, steps_per_epoch):
    """
    Generate cosine annealing learning rate.
    
    Args:
        global_step: Current global step
        lr_init: Initial learning rate
        lr_end: Final learning rate
        total_epochs: Total number of epochs
        steps_per_epoch: Number of steps per epoch
    
    Returns:
        Learning rate array
    """
    lr = []
    total_steps = steps_per_epoch * total_epochs
    
    for i in range(total_steps):
        progress = i / total_steps
        lr.append(lr_end + (lr_init - lr_end) * 0.5 * (1 + math.cos(math.pi * progress)))
    
    return np.array(lr, dtype=np.float32)


def get_lr_step(global_step, lr_init, lr_end, decay_epochs, steps_per_epoch):
    """
    Generate step decay learning rate.
    
    Args:
        global_step: Current global step
        lr_init: Initial learning rate
        lr_end: Final learning rate
        decay_epochs: List of epochs to decay learning rate
        steps_per_epoch: Number of steps per epoch
    
    Returns:
        Learning rate array
    """
    lr = []
    total_steps = steps_per_epoch * max(decay_epochs)
    current_lr = lr_init
    
    for i in range(total_steps):
        current_epoch = i // steps_per_epoch
        if current_epoch in decay_epochs:
            current_lr *= 0.1
        lr.append(current_lr)
    
    return np.array(lr, dtype=np.float32)


def get_lr_polynomial(global_step, lr_init, lr_end, total_epochs, steps_per_epoch, power=2.0):
    """
    Generate polynomial decay learning rate.
    
    Args:
        global_step: Current global step
        lr_init: Initial learning rate
        lr_end: Final learning rate
        total_epochs: Total number of epochs
        steps_per_epoch: Number of steps per epoch
        power: Power of polynomial decay
    
    Returns:
        Learning rate array
    """
    lr = []
    total_steps = steps_per_epoch * total_epochs
    
    for i in range(total_steps):
        progress = i / total_steps
        lr.append(lr_end + (lr_init - lr_end) * (1 - progress) ** power)
    
    return np.array(lr, dtype=np.float32)


def get_lr_exponential(global_step, lr_init, lr_end, total_epochs, steps_per_epoch, decay_rate=0.96):
    """
    Generate exponential decay learning rate.
    
    Args:
        global_step: Current global step
        lr_init: Initial learning rate
        lr_end: Final learning rate
        total_epochs: Total number of epochs
        steps_per_epoch: Number of steps per epoch
        decay_rate: Decay rate for exponential decay
    
    Returns:
        Learning rate array
    """
    lr = []
    total_steps = steps_per_epoch * total_epochs
    
    for i in range(total_steps):
        current_epoch = i // steps_per_epoch
        lr.append(lr_init * (decay_rate ** current_epoch))
    
    return np.array(lr, dtype=np.float32)


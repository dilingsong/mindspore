/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#include "src/runtime/kernel/arm/base/reshape_base.h"
#include <vector>
#include "src/runtime/kernel/arm/int8/reshape_int8.h"
#include "src/runtime/kernel/arm/fp32/reshape.h"
#include "schema/model_generated.h"
#include "src/kernel_factory.h"
#include "include/errorcode.h"
#include "include/context.h"

using mindspore::lite::KernelRegistrar;
using mindspore::lite::RET_ERROR;
using mindspore::lite::RET_OK;
using mindspore::schema::PrimitiveType_Reshape;

namespace mindspore::kernel {
int ReshapeBaseCPUKernel::Init() {
  reshape_param_->thread_count_ = thread_count_;
  return RET_OK;
}

kernel::LiteKernel *CpuReshapeInt8KernelCreator(const std::vector<lite::tensor::Tensor *> &inputs,
                                                const std::vector<lite::tensor::Tensor *> &outputs,
                                                OpParameter *opParameter, const Context *ctx,
                                                const kernel::KernelKey &desc, const lite::Primitive *primitive) {
  if (opParameter == nullptr) {
    MS_LOG(ERROR) << "Input opParameter is nullptr!";
    return nullptr;
  }
  MS_ASSERT(desc.type == schema::PrimitiveType_Reshape);
  auto *kernel = new (std::nothrow) ReshapeInt8CPUKernel(opParameter, inputs, outputs, ctx, primitive);
  if (kernel == nullptr) {
    MS_LOG(ERROR) << "new ReshapeInt8CPUKernel fail!";
    return nullptr;
  }
  auto ret = kernel->Init();
  if (ret != RET_OK) {
    delete kernel;
    MS_LOG(ERROR) << "Init kernel failed, name: " << opParameter->name_ << ", type: "
                  << schema::EnumNamePrimitiveType(static_cast<schema::PrimitiveType>(opParameter->type_));
    return nullptr;
  }
  return kernel;
}

kernel::LiteKernel *CpuReshapeInt32KernelCreator(const std::vector<lite::tensor::Tensor *> &inputs,
                                                 const std::vector<lite::tensor::Tensor *> &outputs,
                                                 OpParameter *opParameter, const Context *ctx,
                                                 const kernel::KernelKey &desc, const lite::Primitive *primitive) {
  if (opParameter == nullptr) {
    MS_LOG(ERROR) << "Input opParameter is nullptr!";
    return nullptr;
  }
  MS_ASSERT(desc.type == schema::PrimitiveType_Reshape);
  auto *kernel = new (std::nothrow) ReshapeCPUKernel(opParameter, inputs, outputs, ctx, primitive);
  if (kernel == nullptr) {
    MS_LOG(ERROR) << "new ReshapeCPUKernel fail!";
    return nullptr;
  }
  auto ret = kernel->Init();
  if (ret != RET_OK) {
    delete kernel;
    MS_LOG(ERROR) << "Init kernel failed, name: " << opParameter->name_ << ", type: "
                  << schema::EnumNamePrimitiveType(static_cast<schema::PrimitiveType>(opParameter->type_));
    return nullptr;
  }
  return kernel;
}

kernel::LiteKernel *CpuReshapeFp32KernelCreator(const std::vector<lite::tensor::Tensor *> &inputs,
                                                const std::vector<lite::tensor::Tensor *> &outputs,
                                                OpParameter *opParameter, const Context *ctx,
                                                const kernel::KernelKey &desc, const lite::Primitive *primitive) {
  if (opParameter == nullptr) {
    MS_LOG(ERROR) << "Input opParameter is nullptr!";
    return nullptr;
  }
  MS_ASSERT(desc.type == schema::PrimitiveType_Reshape);
  auto *kernel = new (std::nothrow) ReshapeCPUKernel(opParameter, inputs, outputs, ctx, primitive);
  if (kernel == nullptr) {
    MS_LOG(ERROR) << "new ReshapeCPUKernel fail!";
    return nullptr;
  }
  auto ret = kernel->Init();
  if (ret != RET_OK) {
    delete kernel;
    MS_LOG(ERROR) << "Init kernel failed, name: " << opParameter->name_ << ", type: "
                  << schema::EnumNamePrimitiveType(static_cast<schema::PrimitiveType>(opParameter->type_));
    return nullptr;
  }
  return kernel;
}

REG_KERNEL(kCPU, kNumberTypeInt8, PrimitiveType_Reshape, CpuReshapeInt8KernelCreator)
REG_KERNEL(kCPU, kNumberTypeInt32, PrimitiveType_Reshape, CpuReshapeInt32KernelCreator)
REG_KERNEL(kCPU, kNumberTypeFloat32, PrimitiveType_Reshape, CpuReshapeFp32KernelCreator)
}  // namespace mindspore::kernel

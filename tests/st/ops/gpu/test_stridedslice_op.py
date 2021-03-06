# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

import numpy as np
import pytest

import mindspore.context as context
from mindspore import Tensor
from mindspore.ops import operations as P

context.set_context(mode=context.GRAPH_MODE, device_target='GPU')


@pytest.mark.level0
@pytest.mark.platform_x86_gpu_training
@pytest.mark.env_onecard
def test_stridedslice():
    x = Tensor(np.arange(0, 2*3*4*5).reshape(2, 3, 4, 5).astype(np.float32))
    y = P.StridedSlice()(x, (1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1))
    expect = np.array([[[[62, 63],
                         [67, 68]],
                        [[82, 83],
                         [87, 88]]]])
    assert np.allclose(y.asnumpy(), expect)

    y = P.StridedSlice()(x, (1, 0, 0, 5), (2, 2, 2, 1), (1, 1, 1, -2))
    expect = np.array([[[[64, 62],
                         [69, 67]],
                        [[84, 82],
                         [89, 87]]]])
    assert np.allclose(y.asnumpy(), expect)

    y = P.StridedSlice()(x, (1, 0, 0, -1), (2, 2, 2, 1), (1, 1, 1, -1))
    expect = np.array([[[[64, 63, 62],
                         [69, 68, 67]],
                        [[84, 83, 82],
                         [89, 88, 87]]]])
    assert np.allclose(y.asnumpy(), expect)

    # ME infer fault
    # y = P.StridedSlice()(x, (1, 0, -1, -2), (2, 2, 0, -5), (1, 1, -1, -2))
    # expect = np.array([[[[78, 76],
    #                      [73, 71],
    #                      [68, 66]],
    #                     [[98, 96],
    #                      [93, 91],
    #                      [88, 86]]]])
    # assert np.allclose(y.asnumpy(), expect)

    # y = P.StridedSlice(begin_mask=0b1000, end_mask=0b0010)(x, (1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1))
    # expect = np.array([[[[ 62,  63],
    #                      [ 67,  68]],
    #                     [[ 82,  83],
    #                      [ 87,  88]],
    #                     [[102, 103],
    #                      [107, 108]]]])
    # assert np.allclose(y.asnumpy(), expect)

    op = P.StridedSlice(begin_mask=0b1000, end_mask=0b0010, ellipsis_mask=0b0100)
    y = op(x, (1, 0, 0, 2), (2, 2, 2, 4), (1, 1, 1, 1))
    expect = np.array([[[[60, 61, 62, 63],
                         [65, 66, 67, 68],
                         [70, 71, 72, 73],
                         [75, 76, 77, 78]],
                        [[80, 81, 82, 83],
                         [85, 86, 87, 88],
                         [90, 91, 92, 93],
                         [95, 96, 97, 98]],
                        [[100, 101, 102, 103],
                         [105, 106, 107, 108],
                         [110, 111, 112, 113],
                         [115, 116, 117, 118]]]])
    assert np.allclose(y.asnumpy(), expect)

    x = Tensor(np.arange(0, 3*4*5).reshape(3, 4, 5).astype(np.float32))
    y = P.StridedSlice()(x, (1, 0, 0), (2, -3, 3), (1, 1, 3))
    expect = np.array([[[20]]])
    assert np.allclose(y.asnumpy(), expect)

    x_np = np.arange(0, 4*5).reshape(4, 5).astype(np.float32)
    y = Tensor(x_np)[:, ::-1]
    expect = x_np[:, ::-1]
    assert np.allclose(y.asnumpy(), expect)

    x = Tensor(np.arange(0, 2 * 3 * 4 * 5 * 4 * 3 * 2).reshape(2, 3, 4, 5, 4, 3, 2).astype(np.float32))
    y = P.StridedSlice()(x, (1, 0, 0, 2, 1, 2, 0), (2, 2, 2, 4, 2, 3, 2), (1, 1, 1, 1, 1, 1, 2))
    expect = np.array([[[[[[[1498.]]],
                          [[[1522.]]]],
                         [[[[1618.]]],
                          [[[1642.]]]]],
                        [[[[[1978.]]],
                          [[[2002.]]]],
                         [[[[2098.]]],
                          [[[2122.]]]]]]])
    assert np.allclose(y.asnumpy(), expect)

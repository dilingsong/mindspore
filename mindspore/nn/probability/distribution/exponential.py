# Copyright 2020 Huawei Technologies Co., Ltd
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
"""Exponential Distribution"""
import numpy as np
from mindspore.ops import operations as P
from mindspore.common import dtype as mstype
from .distribution import Distribution
from ._utils.utils import cast_to_tensor, check_greater_zero

class Exponential(Distribution):
    """
    Example class: Exponential Distribution.

    Args:
        rate (float, list, numpy.ndarray, Tensor, Parameter): inverse scale.
        seed (int): seed to use in sampling. Default: 0.
        dtype (mindspore.dtype): type of the distribution. Default: mstype.float32.
        name (str): name of the distribution. Default: Exponential.

    Note:
        rate should be strictly greater than 0.
        Dist_spec_args is rate.

    Examples:
        >>> # To initialize an Exponential distribution of rate 0.5
        >>> import mindspore.nn.probability.distribution as msd
        >>> e = msd.Exponential(0.5, dtype=mstype.float32)
        >>>
        >>> # The following creates two independent Exponential distributions
        >>> e = msd.Exponential([0.5, 0.5], dtype=mstype.float32)
        >>>
        >>> # An Exponential distribution can be initilized without arguments
        >>> # In this case, rate must be passed in through args during function calls
        >>> e = msd.Exponential(dtype=mstype.float32)
        >>>
        >>> # To use Exponential in a network
        >>> class net(Cell):
        >>>     def __init__(self):
        >>>         super(net, self).__init__():
        >>>         self.e1 = msd.Exponential(0.5, dtype=mstype.float32)
        >>>         self.e2 = msd.Exponential(dtype=mstype.float32)
        >>>
        >>>     # All the following calls in construct are valid
        >>>     def construct(self, value, rate_b, rate_a):
        >>>
        >>>         # Similar calls can be made to other probability functions
        >>>         # by replacing 'prob' with the name of the function
        >>>         ans = self.e1.prob(value)
        >>>         # Evaluate with the respect to distribution b
        >>>         ans = self.e1.prob(value, rate_b)
        >>>
        >>>         # Rate must be passed in during function calls
        >>>         ans = self.e2.prob(value, rate_a)
        >>>
        >>>         # Functions 'sd', 'var', 'entropy' have the same usage as'mean'
        >>>         # Will return 2
        >>>         ans = self.e1.mean()
        >>>         # Will return 1 / rate_b
        >>>         ans = self.e1.mean(rate_b)
        >>>
        >>>         # Rate must be passed in during function calls
        >>>         ans = self.e2.mean(rate_a)
        >>>
        >>>         # Usage of 'kl_loss' and 'cross_entropy' are similar
        >>>         ans = self.e1.kl_loss('Exponential', rate_b)
        >>>         ans = self.e1.kl_loss('Exponential', rate_b, rate_a)
        >>>
        >>>         # Additional rate must be passed in
        >>>         ans = self.e2.kl_loss('Exponential', rate_b, rate_a)
        >>>
        >>>         # Sample
        >>>         ans = self.e1.sample()
        >>>         ans = self.e1.sample((2,3))
        >>>         ans = self.e1.sample((2,3), rate_b)
        >>>         ans = self.e2.sample((2,3), rate_a)
    """

    def __init__(self,
                 rate=None,
                 seed=0,
                 dtype=mstype.float32,
                 name="Exponential"):
        """
        Constructor of Exponential distribution.
        """
        param = dict(locals())
        super(Exponential, self).__init__(dtype, name, param)
        if rate is not None:
            self._rate = cast_to_tensor(rate, mstype.float32)
            check_greater_zero(self._rate, "rate")
        else:
            self._rate = rate

        self.minval = np.finfo(np.float).tiny

    # ops needed for the class
        self.const = P.ScalarToArray()
        self.dtypeop = P.DType()
        self.exp = P.Exp()
        self.fill = P.Fill()
        self.less = P.Less()
        self.log = P.Log()
        self.select = P.Select()
        self.shape = P.Shape()
        self.sqrt = P.Sqrt()
        self.sq = P.Square()
        self.uniform = P.UniformReal(seed=seed)

    def extend_repr(self):
        if self.is_scalar_batch:
            str_info = f'rate = {self.rate}'
        else:
            str_info = f'batch_shape = {self._broadcast_shape}'
        return str_info

    @property
    def rate(self):
        """
        Return rate of the distribution.
        """
        return self._rate

    def _mean(self, rate=None):
        r"""
        .. math::
            MEAN(EXP) = \fract{1.0}{\lambda}.
        """
        rate = self.rate if rate is None else rate
        return 1.0 / rate


    def _mode(self, rate=None):
        r"""
        .. math::
            MODE(EXP) = 0.
        """
        rate = self.rate if rate is None else rate
        return self.fill(self.dtype, self.shape(rate), 0.)

    def _sd(self, rate=None):
        r"""
        .. math::
            sd(EXP) = \fract{1.0}{\lambda}.
        """
        rate = self.rate if rate is None else rate
        return 1.0 / rate

    def _entropy(self, rate=None):
        r"""
        .. math::
            H(Exp) = 1 - \log(\lambda).
        """
        rate = self.rate if rate is None else rate
        return 1.0 - self.log(rate)


    def _cross_entropy(self, dist, rate_b, rate_a=None):
        """
        Evaluate cross_entropy between Exponential distributions.

        Args:
            dist (str): type of the distributions. Should be "Exponential" in this case.
            rate_b (Tensor): rate of distribution b.
            rate_a (Tensor): rate of distribution a. Default: self.rate.
        """
        if dist == 'Exponential':
            return self._entropy(rate=rate_a) + self._kl_loss(dist, rate_b, rate_a)
        return None

    def _prob(self, value, rate=None):
        r"""
        pdf of Exponential distribution.

        Args:
            Args:
            value (Tensor): value to be evaluated.
            rate (Tensor): rate of the distribution. Default: self.rate.

        Note:
            Value should be greater or equal to zero.

        .. math::
            pdf(x) = rate * \exp(-1 * \lambda * x) if x >= 0 else 0
        """
        rate = self.rate if rate is None else rate
        prob = rate * self.exp(-1. * rate * value)
        zeros = self.fill(self.dtypeop(prob), self.shape(prob), 0.0)
        comp = self.less(value, zeros)
        return self.select(comp, zeros, prob)

    def _cdf(self, value, rate=None):
        r"""
        cdf of Exponential distribution.

        Args:
            value (Tensor): value to be evaluated.
            rate (Tensor): rate of the distribution. Default: self.rate.

        Note:
            Value should be greater or equal to zero.

        .. math::
            cdf(x) = 1.0 - \exp(-1 * \lambda * x) if x >= 0 else 0
        """
        rate = self.rate if rate is None else rate
        cdf = 1.0 - self.exp(-1. * rate * value)
        zeros = self.fill(self.dtypeop(cdf), self.shape(cdf), 0.0)
        comp = self.less(value, zeros)
        return self.select(comp, zeros, cdf)


    def _kl_loss(self, dist, rate_b, rate_a=None):
        """
        Evaluate exp-exp kl divergence, i.e. KL(a||b).

        Args:
            dist (str): type of the distributions. Should be "Exponential" in this case.
            rate_b (Tensor): rate of distribution b.
            rate_a (Tensor): rate of distribution a. Default: self.rate.
        """
        if dist == 'Exponential':
            rate_a = self.rate if rate_a is None else rate_a
            return self.log(rate_a) - self.log(rate_b) + rate_b / rate_a - 1.0
        return None

    def _sample(self, shape=(), rate=None):
        """
        Sampling.

        Args:
            shape (tuple): shape of the sample. Default: ().
            rate (Tensor): rate of the distribution. Default: self.rate.

        Returns:
            Tensor, shape is shape + batch_shape.
        """
        rate = self.rate if rate is None else rate
        minval = self.const(self.minval)
        maxval = self.const(1.0)
        sample = self.uniform(shape + self.shape(rate), minval, maxval)
        return -self.log(sample) / rate

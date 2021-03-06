import numpy as np
from sklearn.linear_model import LinearRegression
from splearn.linear_model import SparkLinearRegression
from splearn.utils.testing import SplearnTestCase, assert_array_almost_equal


class TestLinearRegression(SplearnTestCase):

    def test_same_coefs(self):
        X, y, Z = self.make_regression(1, 100000)

        local = LinearRegression()
        dist = SparkLinearRegression()

        local.fit(X, y)
        dist.fit(Z)

        assert_array_almost_equal(local.coef_, dist.coef_)
        assert_array_almost_equal(local.intercept_, dist.intercept_)

    def test_same_prediction(self):
        X, y, Z = self.make_regression(1, 100000)

        local = LinearRegression()
        dist = SparkLinearRegression()

        y_local = local.fit(X, y).predict(X)
        y_dist = dist.fit(Z).predict(Z[:, 'X'])

        assert_array_almost_equal(y_local, np.concatenate(y_dist.collect()))

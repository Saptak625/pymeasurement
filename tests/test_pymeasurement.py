import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from pymeasurement import Measurement
from pymeasurement.sigfig import SigFig

class TestMeasurement(unittest.TestCase):
    def test_create_measurement(self):
        m = Measurement("2.0", uncertainty="0.13", units="m")
        self.assertEqual(m.sample, SigFig("2.0"))
        self.assertEqual(m.uncertainty, SigFig("0.1"))
        self.assertEqual(m.units, "m")
        self.assertEqual(str(m), "2.0 +/- 0.1 m")

    def test_create_measurement_with_sigfigs(self):
        m = Measurement("2.0", uncertainty="0.13", units="m", precision=3)
        self.assertEqual(m.sample, SigFig("2.00"))
        self.assertEqual(m.uncertainty, SigFig("0.13"))
        self.assertEqual(m.units, "m")
        self.assertEqual(str(m), "2.00 +/- 0.13 m")

    def test_create_measurement_from_str(self):
        m = Measurement.fromStr("2.0 +/- 0.13 m")
        self.assertEqual(m.sample, SigFig("2.0"))
        self.assertEqual(m.uncertainty, SigFig("0.1"))
        self.assertEqual(m.units, "m")
        self.assertEqual(str(m), "2.0 +/- 0.1 m")

    def test_create_measurement_from_float(self):
        m = Measurement.fromFloat(3.14)
        self.assertEqual(m.sample, SigFig("3.14", constant=True))
        self.assertEqual(m.uncertainty, None)
        self.assertEqual(m.sample.sigfigs, float("inf"))
        self.assertEqual(str(m), "3.14")

    def test_add_measurements(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = Measurement("3.0", uncertainty="0.1", units="m")
        m3 = m1 + m2
        self.assertEqual(m3.sample, SigFig("5.0"))
        self.assertEqual(m3.uncertainty, SigFig("0.2"))
        self.assertEqual(m3.units, "m")
        self.assertEqual(str(m3), "5.0 +/- 0.2 m")
    
    def test_subtract_measurments(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = Measurement("3.0", uncertainty="0.1", units="m")
        m3 = m1 - m2
        self.assertEqual(m3.sample, SigFig("-1.0"))
        self.assertEqual(m3.uncertainty, SigFig("0.2"))
        self.assertEqual(m3.units, "m")
        self.assertEqual(str(m3), "-1.0 +/- 0.2 m")

    def test_multiply_measurements(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = Measurement("3.0", uncertainty="0.1", units="m")
        m3 = m1 * m2
        self.assertEqual(m3.sample, SigFig("6.0"))
        self.assertEqual(m3.absolute().uncertainty, SigFig("0.6"))
        self.assertEqual(m3.units, "m^2")
        self.assertEqual(str(m3), "6.0 +/- 1E+1% m^2")

    def test_divide_measurements(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = Measurement("3.0", uncertainty="0.1", units="m")
        m3 = m1 / m2
        self.assertEqual(m3.sample, SigFig("0.67"))
        self.assertEqual(m3.uncertainty, SigFig("10", sigfigs=1))
        self.assertEqual(m3.units, None)
        self.assertEqual(str(m3), "0.67 +/- 1E+1%")

    def test_add_measurement_to_scalar(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = m1 + Measurement.fromFloat(2, units="m")
        self.assertEqual(m2.sample, SigFig("4.0"))
        self.assertEqual(m2.uncertainty, SigFig("0.1"))
        self.assertEqual(m2.units, "m")
        self.assertEqual(str(m2), "4.0 +/- 0.1 m")

    def test_subtract_scalar_from_measurement(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = m1 - Measurement.fromFloat(2, units="m")
        self.assertEqual(m2.sample, SigFig("0.0"))
        self.assertEqual(m2.uncertainty, SigFig("0.1"))
        self.assertEqual(m2.units, "m")
        self.assertEqual(str(m2), "0.0 +/- 0.1 m")

    def test_divide_measurement_by_scalar(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = m1 / 2
        self.assertEqual(m2.sample, SigFig("1.0"))
        self.assertEqual(m2.uncertainty, SigFig("6"))
        self.assertEqual(m2.units, "m")
        self.assertEqual(str(m2), "1.0 +/- 6% m")

    def test_multiply_measurement_by_scalar(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = m1 * 2
        self.assertEqual(m2.sample, SigFig("4.0"))
        self.assertEqual(m2.uncertainty, SigFig("6"))
        self.assertEqual(m2.units, "m")
        self.assertEqual(str(m2), "4.0 +/- 6% m")

    def test_square_measurement(self):
        m1 = Measurement("2.0", uncertainty="0.13", units="m")
        m2 = m1 ** 2
        self.assertEqual(m2.sample, SigFig("4.0"))
        self.assertEqual(m2.uncertainty, SigFig("1E+1"))
        self.assertEqual(m2.units, "m^2")
        self.assertEqual(str(m2), "4.0 +/- 1E+1% m^2")

    def test_absolute_uncertainty(self):
        m = Measurement.fromStr("2.0 +/- 0.13 m")
        self.assertEqual(m.absolute().uncertainty, SigFig("0.1"))
        self.assertEqual(m.absolute().units, "m")
        self.assertEqual(str(m.absolute()), "2.0 +/- 0.1 m")

    def test_percent_uncertainty(self):
        m = Measurement.fromStr("2.0 +/- 0.13 m")
        self.assertEqual(m.percent().uncertainty, SigFig("6", sigfigs=1))
        self.assertEqual(m.percent().units, "m")
        self.assertEqual(str(m.percent()), "2.0 +/- 6% m")

    def test_sum_measurements(self):
        m1 = Measurement.fromStr("2.0 +/- 0.13 m")
        m2 = Measurement.fromStr("3.0 +/- 0.1 m")
        m3 = Measurement.fromStr("4.0 +/- 0.1 m")
        m4 = Measurement.sum([m1, m2, m3])
        self.assertEqual(m4.sample, SigFig("9.0"))
        self.assertEqual(m4.uncertainty, SigFig("0.3"))
        self.assertEqual(m4.units, "m")
        self.assertEqual(str(m4), "9.0 +/- 0.3 m")

    def test_max_measurements(self):
        m1 = Measurement.fromStr("2.0 +/- 0.13 m")
        m2 = Measurement.fromStr("3.0 +/- 0.1 m")
        m3 = Measurement.fromStr("4.0 +/- 0.1 m")
        m4 = max([m1, m2, m3])
        self.assertEqual(m4.sample, SigFig("4.0"))
        self.assertEqual(m4.uncertainty, SigFig("0.1"))
        self.assertEqual(m4.units, "m")
        self.assertEqual(str(m4), "4.0 +/- 0.1 m")

    def test_min_measurements(self):
        m1 = Measurement.fromStr("2.0 +/- 0.13 m")
        m2 = Measurement.fromStr("3.0 +/- 0.1 m")
        m3 = Measurement.fromStr("4.0 +/- 0.1 m")
        m4 = min([m1, m2, m3])
        self.assertEqual(m4.sample, SigFig("2.0"))
        self.assertEqual(m4.uncertainty, SigFig("0.1"))
        self.assertEqual(m4.units, "m")
        self.assertEqual(str(m4), "2.0 +/- 0.1 m")    

    def test_average_measurements(self):
        m1 = Measurement.fromStr("2.0 +/- 0.13 m")
        m2 = Measurement.fromStr("3.0 +/- 0.1 m")
        m3 = Measurement.fromStr("4.0 +/- 0.1 m")
        m4 = Measurement.average([m1, m2, m3])
        self.assertEqual(m4.sample, SigFig("3.0"))
        self.assertEqual(m4.uncertainty, SigFig("0.6"))
        self.assertEqual(m4.units, "m")
        self.assertEqual(str(m4), "3.0 +/- 0.6 m")
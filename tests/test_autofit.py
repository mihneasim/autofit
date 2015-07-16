import unittest
from mock import Mock

from creatives import geometry


class GeometryTestCase(unittest.TestCase):

	def test_center_crop(self):
		""" Test calculation of auto crop box """
		data_set = [
			((100, 100, 100, 100), (0, 0, 100, 100)),
			((150, 100, 100, 100), (25, 0, 125, 100)),
			((100, 200, 100, 100), (0, 50, 100, 150)),
		]
		for input, expected in data_set:
			self.assertEqual(geometry.center_crop(*input), expected)

	def test_resize_for(self):
		""" Test we're resizing properly for upcoming crop box """
		data_set = [
			((100, 100, 100, 100), (100, 100)),
			((300, 250, 60, 25), (60, 50)),
			((300, 250, 600, 50), (600, 500)),
		]
		for input, expected in data_set:
			self.assertEqual(geometry.resize_for(*input), expected)

	def test_autofit(self):
		""" Test autofit calls proper resize and crop on image object """
		image = Mock()
		image.size = (300, 250)
		intermediary = Mock()
		image.resize.return_value = intermediary
		geometry.autofit(image, 125, 125)
		image.resize.assert_called_once_with((150, 125), 1)
		intermediary.crop.assert_called_once_with((12, 0, 137, 125))

	def test_guess_ratio(self):
		self.assertTrue(callable(geometry.guess_ratio))
		self.assertEqual(geometry.guess_ratio(400, 200), "2:1")
		self.assertEqual(geometry.guess_ratio(401, 200), "401:200")
		self.assertEqual(geometry.guess_ratio(1920, 1080), "16:9")

# -*- coding: utf-8 -*-
import io
import os
import shutil
import unittest
import unittest.mock

from tests.unit.data import DATA_PATH

from comet.models import (CometEstimator, download_model, load_checkpoint,
                          model2download)


class TestDownload(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(DATA_PATH+"/hter-estimator-v1.0")

    def test_model2download(self):
        model2link = model2download(DATA_PATH+"/")
        self.assertTrue(os.path.exists(DATA_PATH + "/model2download.pkl"))
        # Double call should overwrite file.
        model2link = model2download(DATA_PATH+"/")
        self.assertIsInstance(model2link, dict)
        os.remove(DATA_PATH + "/model2download.pkl")

    def test_model2download_bad_saving_dir(self):
        self.assertRaises(FileNotFoundError, lambda: model2download("folder/that/does/not/exist/"))
    
    @unittest.mock.patch("sys.stdout", new_callable=io.StringIO)
    def test_download_model(self, mock_stdout):
        model = download_model("hter-estimator-v1.0", DATA_PATH+"/")
        self.assertIsInstance(model, CometEstimator)
        self.assertIn("Download succeeded. Loading model...", mock_stdout.getvalue())
        download_model("hter-estimator-v1.0", DATA_PATH+"/")
        self.assertIn("is already in cache.", mock_stdout.getvalue())

    def test_download_wrong_model(self):
        with self.assertRaises(Exception) as context:
            download_model("WrongModel", DATA_PATH+"/")
        self.assertEqual(str(context.exception), "WrongModel is not a valid COMET model!")

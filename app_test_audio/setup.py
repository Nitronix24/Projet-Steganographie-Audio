from setuptools import setup

setup(
  name="audio_test_app",
  version="1.0",
  py_modules=["audio_test_app"],
  install_requires=["pygame"],
  entry_points={
    "console_scripts": ["audio-test=audio_test_app:main"],
  },
)

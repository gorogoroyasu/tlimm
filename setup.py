from setuptools import setup

requires = ['pillow', 'numpy']
setup(
    name="tlimm",
    version='0.1',
    description='Image Cropping Library for Object Detection.',
    url='https://github.com/gorogoroyasu/tlimm',
    author='gorogoroyasu',
    author_email='gorogoro.yasu@gmail.com',
    license='MIT',
    keywords='object detection',
    packages=['src'],
    install_requires=requires,
)
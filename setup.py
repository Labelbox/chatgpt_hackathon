import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='chatgpt_hackathon',
    version='0.0.01',
    author='Labelbox',
    author_email="raphael@labelbox.com",
    description='Helper repo for ChatGPT Hackathon',
    long_description=long_description,
    long_description_content_type="text/markdown",    
    url='https://github.com/Labelbox/chatgpt_hackathon',    
    packages=setuptools.find_packages(),
    install_requires=["labelbox[data]", "openai", "packaging", "labelbase"]
)

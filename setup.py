from pathlib import Path

from skbuild import setup

# Read the contents of the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="TheengsExplorer",
    version="version_tag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Theengs",
    url="https://github.com/theengs/explorer",
    license="GPL-3.0 License",
    package_dir={"TheengsExplorer": "TheengsExplorer"},
    packages=["TheengsExplorer"],
    include_package_data=True,
    install_requires=["TheengsDecoder>=0.4.0", "textual>=0.1.15", "bluetooth-numbers>=0.1.1", "bleak>=0.17.0", "humanize>=4.4.0"],
)

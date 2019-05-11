# -*- coding: utf-8 -*-

from conans import ConanFile, tools
import os
import sys

DEFAULT_MAX_CONSTANTS = "64"
DEFAULT_MAX_NAME_LENGTH = "23"


class LibnameConan(ConanFile):
    name = "better-enums"
    version = "0.11.2"
    description = "C++ compile-time enum to string, iteration, in a single header file."
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("c++", "reflection", "enums")
    url = "https://github.com/rhololkeolke/conan-better-enums"
    homepage = "http://aantron.github.io/better-enums/"
    author = "Devin Schwab <dschwab@andrew.cmu.edu>"
    license = (
        "MIT"
    )  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    no_copy_source = True

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    options = {"max_constants": "ANY", "max_name_length": "ANY"}
    default_options = {
        "max_constants": DEFAULT_MAX_CONSTANTS,
        "max_name_length": DEFAULT_MAX_NAME_LENGTH,
    }

    def source(self):
        os.makedirs(os.path.join(self._source_subfolder, "include"), exist_ok=True)

        source_url = "https://raw.githubusercontent.com/aantron/better-enums"
        enum_file_path = os.path.join(self._source_subfolder, "include", "enum.h")
        tools.download(
            "{0}/{1}/enum.h".format(source_url, self.version), enum_file_path
        )
        tools.check_sha256(
            enum_file_path,
            "e492f35736be931e3eb6d993e0074927ea3fa25044492d21a34368a00f35525e",
        )

        license_file_path = os.path.join(self._source_subfolder, "LICENSE")
        tools.download(
            "{0}/{1}/doc/LICENSE".format(source_url, self.version), license_file_path
        )
        tools.check_sha256(
            license_file_path,
            "b213f959d7a07c2a161336723a284d795f8cf094e9146c05ed5de796eb9f2bb8",
        )

        if (
            self.options.max_constants != DEFAULT_MAX_CONSTANTS
            or self.options.max_name_length != DEFAULT_MAX_NAME_LENGTH
        ):
            tools.download(
                "{0}/{1}/script/make_macros.py".format(source_url, self.version),
                "make_macros.py",
            )
            tools.check_sha256(
                "make_macros.py",
                "b64d9a45a11ed607a4bd3911d17541753d0cde50298f284b5063185be5602872",
            )

            # script is python 2, convert to python 3
            from lib2to3.main import main

            if main("lib2to3.fixes", ["--no-diffs", "-w", "-n", "make_macros.py"]):
                raise Exception("py3 conversion of 'make_macros' failed")

            # generate
            sys.path.append(os.getcwd())
            import make_macros

            os.makedirs(os.path.join(self._source_subfolder, "include", "common"))
            with open(
                os.path.join(
                    self._source_subfolder, "include", "common", "enum_macros.h"
                ),
                "w",
            ) as f:
                make_macros.generate(
                    f,
                    int(self.options.max_constants),
                    int(self.options.max_name_length),
                    "make_macros.py",
                )

    def package(self):
        include_folder = os.path.join(self._source_subfolder, "include")
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=include_folder)

    def package_info(self):
        if (
            self.options.max_constants != DEFAULT_MAX_CONSTANTS
            or self.options.max_name_length != DEFAULT_MAX_NAME_LENGTH
        ):
            self.cpp_info.defines.append(
                "BETTER_ENUMS_MACRO_FILE=<common/enum_macros.h>"
            )

    def package_id(self):
        self.info.header_only()

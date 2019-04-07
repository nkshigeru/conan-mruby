import os
from conans import ConanFile, tools


class MrubyConan(ConanFile):
    name = "mruby"
    version = "2.0.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Mruby here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "enable_cxx_abi": [True, False]
    }
    default_options = \
        "enable_cxx_abi=False"
    generators = "cmake"
    source_subfolder = "mruby-{version}".format(version=version)

    def build_requirements(self):
        if tools.os_info.is_linux:
            installer = tools.SystemPackageTool()
            installer.install("ruby")
            installer.install("bison")
        if tools.os_info.is_windows:
            self.build_requires("ruby_installer/2.5.1@bincrafters/stable")

    def source(self):
        url = "https://github.com/mruby/mruby/archive/{version}.tar.gz".format(version=self.version)
        tools.get(url)

    def build(self):
        with tools.chdir(self.source_subfolder):
            build_config = "build_config.rb"
            os.rename(build_config, build_config + ".0")
            with open(build_config, "w") as f:
                f.write("MRuby::Build.new do |conf|\n")
                if self.settings.compiler == "Visual Studio":
                    f.write("  toolchain :visualcpp\n")
                else:
                    f.write("  toolchain :gcc\n")

                if self.settings.build_type == "Debug":
                    f.write("  enable_debug\n")
                if self.options.enable_cxx_abi:
                    f.write("  enable_cxx_abi\n")
                
                # default gembox
                f.write("  conf.gembox 'default'\n")

                f.write("end\n")
                
            with tools.vcvars(self.settings):
                self.run("ruby minirake")

    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.source_subfolder, "include"))
        self.copy("*.lib", src=self.source_subfolder)
        self.copy("*.a", src=self.source_subfolder)
        self.copy("*", dst="bin", src=os.path.join(self.source_subfolder, "bin"), excludes=".gitkeep")

    def package_info(self):
        if self.options.enable_cxx_abi: 
            self.cpp_info.defines.append("MRB_ENABLE_CXX_ABI")
            self.cpp_info.defines.append("MRB_ENABLE_CXX_EXCEPTION")
        self.cpp_info.libdirs = ["build/host/lib"]
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["libmruby", "ws2_32"]
        else:
            self.cpp_info.libs = ["mruby"]


# ulptool-cp-fix
Added into Arduino build recipe ulp assembly files.s copies from {build.source.path} to {build.path}/sketch so that they get included in build.  This is based on repository https://github.com/duff2013/ulptool

dec-2021 start code for copy of {build.source.path}/*.s to {build_path} directory
     The idea is to use .../platform.local.txt to call this esp32ulp_build_recipe.py
     to pass in (-j) the sketch source directory and (-b) build directory
     to allow the *.s files to be copied from source dir to dest dir.
     The original code seemed to assume the .s files were copied into the build directory.
     This dec-2021 code is added to accomplish the copy of .s files from source dir to build dir.
    

dec-2021  see these lines in .../platform.local.txt file
dec-2021 pass in source directory ({build.source.path}) for *.s file copy to build directory ({build.path})
     compiler.s.cmd=python {tools.ulptool.path}{tools.ulptool.cmd} -j {build.source.path}

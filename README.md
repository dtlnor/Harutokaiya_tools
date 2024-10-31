# ~~NeXAS Switch string dumper/importer~~

# NeXAS PC string dumper/importer

Only tested on`あくありうむ。for Windows(Steam)`

## How to use

#### Step1. unpack the pac

Unpack the following pac files with [tools](https://github.com/Yggdrasill-Moe/Niflheim/tree/master/NeXAS)

you only need `pac_pack` and `pac_unpack` (compile yourself using **Visual Studio**)

> Config.pac
>
> Config-en.pac ( only if you want to replace English with your language)
>
> Script.pac 
>
> System.pac
>
> System-en.pac (only if you want to replace English with your language)
>
> Movie.pac

**NOTE**: You need to change the encode from `932` to `CP_UTF8` for `WideCharToMultiByte` function in the `*.c` files before compile.

#### Step2. extract all text from `dat` files

Put the script in the game folder .

Create a `Output` folder in the same directory and copy the `*.pac_unpack` folder into the `Output` folder

change the **target pac path** in line 53.

run `python bin_dump.py`

all text files will be in the original `*.pac_unpack` folder.

#### Step3. repack new `dat` files

do not move extracted  `txt` files

change the **target folder path** in line 42.

run `python bin_import.py`

#### Step4. repack `dat folder`  to `pac`

drag the folder to `pac_pack.exe`

don't forget to backup the original file.





---

## OG README

### Modified from https://github.com/Yggdrasill-Moe/Niflheim/tree/master/NeXAS to support binu8 and datu8

</br>

### Only tested on Aquarium might require some modification for other games

</br>
</br>

## String dumper/importer for binu8 and datu8 files

### How to use

> Dump the game romfs, then copy the Script folder and Config folder to the root directory
>
> Create a ./Output/ folder in the root directory and create Script and Config folder inside it

```> python binu8_dump.py```

> Extract the strings from Script folder binu8 files into .txt files

```> python binu8_import.py```

>Create a new binu8 files based on the modified txt files and put them in the ./Output/Script/ folder

```> python datu8_dump.py```

> Extract the strings from Config folder datu8 files into .txt files

```> python datu8_import.py```

>Create a new datu8 files based on the modified txt files and put them in the ./Output/Config/ folder


### How to import the modified files into the game

> Create a Folder structure such as this
>
> titleID > ModName > romfs
>
> Example : 0100D11018A7E000\English Translation\romfs\
> Inside the folder structure replicate the original game folder structure and put your modified files in those folders
>
> Example : 0100D11018A7E000\English Translation\romfs\Script\aqu_01_01.binu8


### Yuzu

> Put that folder inside %appdata%/yuzu/load/

### Ryujinx

> Put that folder inside %appdata%/Ryujinx/mods/contents/






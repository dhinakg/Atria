# Generated by luzgen at 2023-03-30 14:35:09.112499
from pathlib import Path
from shutil import copytree

from luz import Control, Meta, Module, Script

meta = Meta(release=True, cc="clang++")

# Define control metadata here
control = Control(
    name="Atria",
    id="me.lau.atria",
    version="1.3.3-4",
    author="ren7995",
    maintainer="Dhinak G <dhinak@dhinak.net>",
    description="A proper homescreen layout editor for iOS 13-15",
    depends=[
        "firmware (>= 13.0)",
        "mobilesubstrate",
        "preferenceloader",
         "ws.hbang.alderis (>= 1.1)"
    ],
    conflicts=["com.irepo.boxy4", "me.kritanta.homepluspro"],
    architecture="iphoneos-arm64" if meta.release else "iphoneos-arm",
    section="Tweaks",
)

install_dir = meta.root_dir.relative_to(meta.staging_dir)
if install_dir == Path("."):
    install_dir = ""
else:
    install_dir = "/" + str(install_dir)

install_prefix = f'-DINSTALL_PREFIX=\\"{install_dir}\\"'


scripts = [
    Script("postinst", "layout/DEBIAN/postinst"),
]

for script in scripts:
    script.content = script.content.replace("@@INSTALL_PREFIX@@", install_dir)


# Module info
modules = [
    Module(
        type="tweak",
        name="Atria",
        files=["Hooks/*.xm", "src/**/*.m"],
        c_flags=["-I.", install_prefix],
        frameworks=["UIKit", "QuartzCore", "CoreGraphics", "CoreText"],
        filter={"bundles": ["com.apple.springboard"]},
    ),
    Module(
        type="prefs",
        name="AtriaPrefs",
        files=["Prefs/*.m"],
        c_flags=[install_prefix],
        frameworks=["UIKit", "QuartzCore"],
        after_stage=lambda: copytree(Path("Prefs/layout/Library"), meta.root_dir / "Library", dirs_exist_ok=True),
        resources_dir=Path("Prefs/Resources"),
    ),
]

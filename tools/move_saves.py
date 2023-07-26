import os
import shutil
import sys
import time

from absl import app, flags

FLAGS = flags.FLAGS

flags.DEFINE_bool(
    "setup_saves",
    False,
    "Will set up the TAS saves and store your saves in "
    + "a new folder called 'Save Backups'",
)
flags.DEFINE_bool(
    "restore_saves", False, "Will restore your saves and remove the TAS saves."
)

flags.DEFINE_string(
    "user_path",
    "",
    "Set this if your Documents folder, and thus your 'SQUARE ENIX\\FINAL FANTASY "
    + "X&X-2 HD Remaster folder' is in a different location.",
)


def _move_file(name, src_dir, dest_dir, mod_time):
    src_full_path = os.path.join(src_dir, name)
    dest_full_path = os.path.join(dest_dir, name)
    shutil.copy(src_full_path, dest_full_path)
    os.utime(dest_full_path, (mod_time, mod_time))
    return


def check_flags():
    """Checks flags."""
    if FLAGS.setup_saves == FLAGS.restore_saves:
        print("Exactly one of --setup_saves or --restore_saves must be set.")
        sys.exit(1)


def setup_saves():
    """Moves the TAS saves to the correct location."""
    square_saves = f"{FLAGS.user_path or os.path.expanduser('~')}"
    +"\\Documents\\SQUARE ENIX\\FINAL FANTASY X&X-2 HD Remaster\\FINAL FANTASY X\\"
    tas_saves = ".\\tas_saves"
    print(f"Copying save files from '{square_saves}' to '.\\Save Backups'")
    shutil.copytree(square_saves, ".\\Save Backups")
    print(
        "Copying TAS save files from '.\\tas_saves' to "
        + f"{square_saves}' and modifying timestamps."
    )
    shutil.rmtree(square_saves)
    os.mkdir(square_saves)
    current_time = time.time() - 10000
    for cur_file in sorted(
        [
            f
            for f in os.listdir(tas_saves)
            if os.path.isfile(os.path.join(tas_saves, f))
        ],
        reverse=True,
    ):
        _move_file(cur_file, tas_saves, square_saves, current_time)
        current_time += 60


def restore_saves():
    """Restores the backed up saves."""
    square_saves = f"{FLAGS.user_path or os.path.expanduser('~')}"
    +"\\Documents\\SQUARE ENIX\\FINAL FANTASY X&X-2 HD Remaster\\FINAL FANTASY X\\"
    shutil.rmtree(square_saves)
    shutil.copytree(".\\Save Backups", square_saves)
    shutil.rmtree(".\\Save Backups")


def main(argv):
    print(
        "TAS Save fixer utility. "
        + "Ensure that the script is run from the main folder of the repo."
    )
    check_flags()
    if FLAGS.setup_saves:
        print("Setting TAS Saves Up.")
        setup_saves()
    elif FLAGS.restore_saves:
        print("Restoring Backed Up Saves.")
        restore_saves()
    print("Done")


if __name__ == "__main__":
    app.run(main)

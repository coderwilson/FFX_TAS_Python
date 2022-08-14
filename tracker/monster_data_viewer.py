import sys
import tkinter as tk

from ffx_rng_tracker.data.file_functions import get_resource_path, get_version
from ffx_rng_tracker.logger import (log_exceptions, log_tkinter_error,
                                    setup_logger)
from ffx_rng_tracker.ui_tkinter.main import AZURE_THEME_PATH
from ffx_rng_tracker.ui_tkinter.monster_data_viewer import TkMonsterDataViewer


@log_exceptions()
def main() -> None:
    setup_logger()
    root = tk.Tk()
    # redirects errors to another function
    root.report_callback_exception = log_tkinter_error
    root.protocol('WM_DELETE_WINDOW', root.quit)
    root.title('ffx_monster_data_viewer v' + '.'.join(map(str, get_version())))
    root.geometry('1280x800')

    if '-notheme' not in sys.argv:
        theme_path = get_resource_path(AZURE_THEME_PATH)
        root.tk.call('source', theme_path)
        if '-darkmode' in sys.argv:
            root.tk.call('set_theme', 'dark')
        else:
            root.tk.call('set_theme', 'light')

    ui = TkMonsterDataViewer(root)
    ui.pack(expand=True, fill='both')
    root.mainloop()


if __name__ == '__main__':
    main()

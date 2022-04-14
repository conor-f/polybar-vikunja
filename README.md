# polybar-vikunja

  Polybar plugin to interact with your Vikunja lists in a basic manner. It
displays how many incomplete todos you have in a list, and allows you to mark
them as complete/incomplete easily. You can specify an individual list to show
using a basic right-click popup menu.


![Screenshot from 2022-04-14 15-57-42](https://user-images.githubusercontent.com/2671067/163417918-ab2c7315-1026-47f4-875c-7bbdc812c8c8.png)
![Screenshot from 2022-04-14 15-58-08](https://user-images.githubusercontent.com/2671067/163417934-8ecbe24f-cd43-4d9b-be74-f0267d0d3268.png)
![Screenshot from 2022-04-14 15-59-36](https://user-images.githubusercontent.com/2671067/163417946-fd2497e8-3e38-4bcc-886e-26ad035c5c80.png)

## Usage:

  After installing and configuring `spotibar` to run on your Polybar as
described below, you should see the number of remaining todos you have. If you
right-click on this, you will be able to set which list `polybar-vikunja` is
reading from, and if you left-click, you can see the tasks remaining and mark
them as complete.

## Installation:
  `polybar-vikunja` relies on python3.6+ to run. To install, run:

  ```
  python3 -m pip install polybar-vikunja
  ```

  Then to configure `polybar-vikunja`, run in a new terminal (or after sourcing
  your env):

  ```
  polybar-vikunja --init
  ```

  If you're getting errors, try removing `polybar-vikunja` and reinstalling under sudo permissions. If you get an error involving `libtk8.6.so`, install tk using your distro's package manager.

  Once `polybar-vikunja` is installed and authenticated, you need to modify your
polybar config as follows (or however suits your needs!):
```
modules-right = <other modules> polybar-vikunja <other modules>

[module/polybar-vikunja]
type = custom/script
exec = echo "  $(polybar-vikunja --get-todo-count)"
click-left = polybar-vikunja --show-todos-popup
click-right = polybar-vikunja --config-popup
format-underline = #126cfd
format-padding = 2
```

  Done! Enjoy! File (probably inevitable) bug reports as issues!

## Development:
  Create an issue if you have any bug reports/feature requests/want to add a feature and are looking for help with the environment setup.

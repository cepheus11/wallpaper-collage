# WALLPAPER-COLLAGE
#
#
# Save an image ("collage") consisting of one, two or three source images ("wallpapers").
# Whole area is covered, cropping of the wallpapers shall be minimal. Best results if aspect ratio
# of the wallpapers is near the aspect ratio of the collage, or inverse.
#
# Wallpaper files searched: *.jpg, *.jpeg, *.jpe, *.jp2, *.png, *.bmp
#
# The collage file is called "wallpaper-collage.jpg" in single mode. In multiple mode, a hyphen and 4-digit number is
# appended: wallpaper-collage-0001.jpg etc.
#
#
# usage: wallpaper-collage [-h] [-x WIDTH] [-y HEIGHT] [-w WALLPAPER_DIR]
#                         [-c COLLAGE_DIR] [-i INTERVAL] [-m MODE]
#                         [--debug DEBUG]
#
# optional arguments:
#  -h, --help            show this help message and exit
#  -x WIDTH, --width WIDTH
#                        Collage width in pixels. Default 1920.
#  -y HEIGHT, --height HEIGHT
#                        Collage height in pixels. Default 1200.
#  -w WALLPAPER_DIR, --wallpaper-dir WALLPAPER_DIR
#                        Directory with source images. Default wallpapers.
#  -c COLLAGE_DIR, --collage-dir COLLAGE_DIR
#                        Target directory for collage image. Default collage.
#  -i INTERVAL, --interval INTERVAL
#                        Collage change interval in seconds. Minimum 10. Default 60. Set to 0 for no automatic change.
#                        (Change only once at start, and at signal SIGUSR1)
#  -m MODE, --mode MODE  Output mode: single|multiple. Default single.
#  --debug DEBUG         Print debug messages to stdout. Default 0 (no debug messages).
#
#
# Signals:
#
# The process name is changed to "wallpaper", so "pkill -USR1 wallpaper" is possible
#
# On SIGUSR1, the wallpaper is changed immediately
# On SIGUSR2, the list of source wallpapers is re-read
#
#
# Flow description:
#
# 1. Select 3 not yet chosen images: A, B and C
# 2. Put images A, B, C into all possible layouts:
#   +-----------+  One
#   |           |
#   |     A     |
#   |           |
#   +-----------+
#
#   +-----------+  Two
#   |     |     |
#   |  A  |  B  |
#   |     |     |
#   +-----------+
#
#   +-----------+  Three
#   |   |   |   |
#   | A | B | C |
#   |   |   |   |
#   +-----------+
#
#   +-----------+  Large Left
#   |     |  B  |
#   |  A  |-----|
#   |     |  C  |
#   +-----------+
#
#   +-----------+  Large Right Clockwise
#   |  A  |     |
#   |-----|  B  |
#   |  C  |     |
#   +-----------+
#
#   +-----------+  Large Right Counter Clockwise
#   |  A  |     |
#   |-----|  C  |
#   |  B  |     |
#   +-----------+
#
#   +-----------+  Two Vertical
#   |     A     |
#   |-----------|
#   |     B     |
#   +-----------+
#
#   +-----------+  Three Vertical
#   |_____A_____|
#   |_____B_____|
#   |     C     |
#   +-----------+
#
#   +-----------+  Large Bottom
#   |  A  |  B  |
#   |-----------|
#   |     C     |
#   +-----------+
#
#   +-----------+  Large Top Clockwise
#   |     B     |
#   |-----------+
#   |  A  |  C  |
#   +-----------+
#
#   +-----------+  Large Top Counter Clockwise
#   |     A     |
#   |-----------|
#   |  B  |  C  |
#   +-----------+
#
# 3. For every layout: calculate ratio of images which must be cropped
# 4. Select the layout solution with lowest crop ratio.
#    Either all 3 images are chosen, or only A and B, or only A
# 5. Create combined wallpaper
# 6. Put the chosen images into the list of already chosen images
# 7. Wait <interval> seconds.
# Repeat.

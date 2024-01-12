"""Settings module for desktop slideshow."""

from pathlib import Path

try:
    if not Path.exists(
        Path(Path.home() / "Desktop" / "desktopSlideshow" / "transitionFrames"),
    ):
        Path.mkdir(
            Path(
                Path.home() / "Desktop" / "desktopSlideshow" / "transitionFrames",
            ),
            parents=True,
        )
except OSError:
    print("Error: Creating directory of transitionFrames")

path = Path(Path.home() / "Desktop" / "desktopSlideshow" / "deer")
transition_path = Path(
    Path.home() / "Desktop" / "desktopSlideshow" / "transitionFrames",
)
video_path = Path(Path.home() / "Desktop" / "desktopSlideshow" / "transition.mp4")

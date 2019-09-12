from .. import RoutingProfile
from pathlib import Path

profiles_dir = Path(__file__).parent

bicycle = RoutingProfile(profiles_dir / "bicycle.lua", default=True)
foot = RoutingProfile(profiles_dir / "foot.lua", default=True)
car = RoutingProfile(profiles_dir / "car.lua", default=True)


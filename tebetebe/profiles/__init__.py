from .. import RoutingProfile
from pathlib import Path

profiles_dir = Path(__file__).parent

bicycle = RoutingProfile(profiles_dir / "bicycle.lua")
foot = RoutingProfile(profiles_dir / "foot.lua")
car = RoutingProfile(profiles_dir / "car.lua")

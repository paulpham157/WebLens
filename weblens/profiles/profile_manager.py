"""
Browser profile management for WebLens
"""
import json
from typing import Dict, List, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict

from ..config import config
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ProfileSettings:
    """Browser profile settings"""
    name: str
    browser: str
    user_agent: Optional[str] = None
    viewport: Dict[str, int] = None
    locale: str = "en-US"
    timezone: str = "America/New_York"
    permissions: List[str] = None
    cookies: List[Dict[str, Any]] = None
    local_storage: Dict[str, str] = None
    session_storage: Dict[str, str] = None
    extensions: List[str] = None
    proxy: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1920, "height": 1080}
        if self.permissions is None:
            self.permissions = []
        if self.cookies is None:
            self.cookies = []
        if self.local_storage is None:
            self.local_storage = {}
        if self.session_storage is None:
            self.session_storage = {}
        if self.extensions is None:
            self.extensions = []


class ProfileManager:
    """Manages browser profiles for different testing scenarios"""
    
    def __init__(self):
        self.profiles: Dict[str, ProfileSettings] = {}
        self.profiles_dir = config.profiles_dir
        self._load_default_profiles()
    
    def _load_default_profiles(self):
        """Load default profiles for common testing scenarios"""
        
        # Desktop Chrome profile
        self.create_profile(
            name="desktop_chrome",
            browser="chrome",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            permissions=["geolocation", "notifications"]
        )
        
        # Mobile Chrome profile
        self.create_profile(
            name="mobile_chrome",
            browser="chrome",
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 375, "height": 812},
            permissions=["geolocation"]
        )
        
        # Tablet profile
        self.create_profile(
            name="tablet",
            browser="chrome",
            user_agent="Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            viewport={"width": 768, "height": 1024}
        )
        
        # Firefox desktop profile
        self.create_profile(
            name="desktop_firefox",
            browser="firefox",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0",
            viewport={"width": 1920, "height": 1080}
        )
        
        # High DPI profile
        self.create_profile(
            name="high_dpi",
            browser="chrome",
            viewport={"width": 2560, "height": 1440}
        )
        
        # Privacy-focused profile
        self.create_profile(
            name="privacy",
            browser="firefox",
            permissions=[],  # No permissions granted
            locale="en-US",
            timezone="UTC"
        )
        
        logger.info(f"Loaded {len(self.profiles)} default profiles")
    
    def create_profile(self, 
                      name: str,
                      browser: str,
                      **kwargs) -> ProfileSettings:
        """Create a new profile"""
        profile = ProfileSettings(name=name, browser=browser, **kwargs)
        self.profiles[name] = profile
        
        # Create profile directory
        profile_dir = self.profiles_dir / browser / name
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        # Save profile settings
        self._save_profile(profile)
        
        logger.info(f"Created profile: {name} for {browser}")
        return profile
    
    def get_profile(self, name: str) -> Optional[ProfileSettings]:
        """Get profile by name"""
        return self.profiles.get(name)
    
    def list_profiles(self, browser: Optional[str] = None) -> List[ProfileSettings]:
        """List all profiles, optionally filtered by browser"""
        profiles = list(self.profiles.values())
        if browser:
            profiles = [p for p in profiles if p.browser == browser]
        return profiles
    
    def delete_profile(self, name: str) -> bool:
        """Delete a profile"""
        if name not in self.profiles:
            return False
        
        profile = self.profiles[name]
        profile_dir = self.profiles_dir / profile.browser / name
        
        # Remove profile directory
        if profile_dir.exists():
            import shutil
            shutil.rmtree(profile_dir)
        
        # Remove from memory
        del self.profiles[name]
        
        logger.info(f"Deleted profile: {name}")
        return True
    
    def update_profile(self, name: str, **kwargs) -> Optional[ProfileSettings]:
        """Update an existing profile"""
        if name not in self.profiles:
            return None
        
        profile = self.profiles[name]
        
        # Update attributes
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        # Save updated profile
        self._save_profile(profile)
        
        logger.info(f"Updated profile: {name}")
        return profile
    
    def clone_profile(self, source_name: str, new_name: str, **overrides) -> Optional[ProfileSettings]:
        """Clone an existing profile with optional overrides"""
        if source_name not in self.profiles:
            return None
        
        source_profile = self.profiles[source_name]
        
        # Create new profile with same settings
        profile_data = asdict(source_profile)
        profile_data["name"] = new_name
        profile_data.update(overrides)
        
        new_profile = ProfileSettings(**profile_data)
        self.profiles[new_name] = new_profile
        
        # Create profile directory
        profile_dir = self.profiles_dir / new_profile.browser / new_name
        profile_dir.mkdir(parents=True, exist_ok=True)
        
        # Save profile
        self._save_profile(new_profile)
        
        logger.info(f"Cloned profile {source_name} to {new_name}")
        return new_profile
    
    def _save_profile(self, profile: ProfileSettings):
        """Save profile settings to file"""
        profile_dir = self.profiles_dir / profile.browser / profile.name
        settings_file = profile_dir / "weblens_profile.json"
        
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(profile), f, indent=2, ensure_ascii=False)
    
    def _load_profile(self, profile_path: Path) -> Optional[ProfileSettings]:
        """Load profile settings from file"""
        settings_file = profile_path / "weblens_profile.json"
        
        if not settings_file.exists():
            return None
        
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return ProfileSettings(**data)
        except Exception as e:
            logger.warning(f"Failed to load profile from {settings_file}: {e}")
            return None
    
    def load_profiles_from_disk(self):
        """Load all profiles from disk"""
        for browser_dir in self.profiles_dir.iterdir():
            if not browser_dir.is_dir():
                continue
            
            for profile_dir in browser_dir.iterdir():
                if not profile_dir.is_dir():
                    continue
                
                profile = self._load_profile(profile_dir)
                if profile:
                    self.profiles[profile.name] = profile
        
        logger.info(f"Loaded {len(self.profiles)} profiles from disk")
    
    def get_profiles_by_browser(self, browser: str) -> List[ProfileSettings]:
        """Get all profiles for a specific browser"""
        return [p for p in self.profiles.values() if p.browser == browser]
    
    def get_profile_combinations(self, browsers: List[str]) -> List[tuple]:
        """Get all valid browser-profile combinations"""
        combinations = []
        
        for browser in browsers:
            browser_profiles = self.get_profiles_by_browser(browser)
            if browser_profiles:
                for profile in browser_profiles:
                    combinations.append((browser, profile.name))
            else:
                # Add default profile if no specific profiles exist
                combinations.append((browser, None))
        
        return combinations

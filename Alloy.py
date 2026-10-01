import array
from collections import OrderedDict
import json
import math
import random
import sys
from pathlib import Path

import pygame


WIDTH, HEIGHT = 1100, 750
FPS = 60
MAX_PARTICLES = 300
MAX_FLOATING_TEXTS = 40
BELLOWS_HEAT_DURATION = (5.0, 6.0, 7.0, 8.0)
VERSION = "1.0.0-rc1"
SAVE_VERSION = 1
SAVE_FILE = Path.home() / ".alloy_forge_save.json"

BACKGROUND = (22, 22, 26)
PANEL = (35, 35, 42)
TEXT = (220, 220, 220)
MUTED = (150, 150, 160)
GOLD = (255, 215, 0)
GREEN = (80, 220, 100)
RED = (230, 70, 70)
BLUE = (150, 200, 255)
CYAN = (100, 230, 240)
PURPLE = (180, 130, 255)

ELEMENTS = {
    "Iron (Fe)": {
        "density": 7.87,
        "strength": 200,
        "cost": 0.5,
        "color": (160, 160, 165),
        "unlocked": True,
    },
    "Carbon (C)": {
        "density": 2.26,
        "strength": 50,
        "cost": 0.2,
        "color": (40, 40, 40),
        "unlocked": True,
    },
    "Copper (Cu)": {
        "density": 8.96,
        "strength": 220,
        "cost": 8.0,
        "color": (184, 115, 51),
        "unlocked": True,
    },
    "Zinc (Zn)": {
        "density": 7.14,
        "strength": 110,
        "cost": 3.0,
        "color": (190, 200, 210),
        "unlocked": True,
    },
    "Chromium (Cr)": {
        "density": 7.19,
        "strength": 300,
        "cost": 12.0,
        "color": (210, 220, 230),
        "unlocked": True,
    },
    "Titanium (Ti)": {
        "density": 4.50,
        "strength": 430,
        "cost": 35.0,
        "color": (140, 150, 170),
        "unlocked": False,
    },
    "Gold (Au)": {
        "density": 19.30,
        "strength": 100,
        "cost": 60.0,
        "color": (240, 200, 40),
        "unlocked": False,
    },
    "Silver (Ag)": {
        "density": 10.49,
        "strength": 140,
        "cost": 22.0,
        "color": (220, 225, 230),
        "unlocked": False,
    },
    "Aluminum (Al)": {
        "density": 2.70,
        "strength": 90,
        "cost": 2.5,
        "color": (200, 210, 215),
        "unlocked": False,
    },
    "Nickel (Ni)": {
        "density": 8.90,
        "strength": 310,
        "cost": 18.0,
        "color": (170, 180, 175),
        "unlocked": False,
    },
    "Tungsten (W)": {
        "density": 19.25,
        "strength": 550,
        "cost": 45.0,
        "color": (100, 110, 125),
        "unlocked": False,
    },
}

RECIPES = {
    frozenset(("Iron (Fe)", "Carbon (C)")): "Carbon Steel",
    frozenset(("Iron (Fe)", "Chromium (Cr)")): "Stainless Steel",
    frozenset(("Copper (Cu)", "Zinc (Zn)")): "Brass",
    frozenset(("Titanium (Ti)", "Iron (Fe)")): "Titanium Steel",
    frozenset(("Gold (Au)", "Copper (Cu)")): "Rose Gold",
    frozenset(("Gold (Au)", "Silver (Ag)")): "Electrum Alloy",
    frozenset(("Aluminum (Al)", "Copper (Cu)")): "Duralumin",
    frozenset(("Nickel (Ni)", "Chromium (Cr)")): "Nichrome Wire",
    frozenset(("Titanium (Ti)", "Aluminum (Al)")): "Aero Titanium-Aluminide",
    frozenset(("Tungsten (W)", "Carbon (C)")): "Tungsten Carbide",
}

CONTRACTS = [
    {
        "client": "Guild Forgery",
        "desc": "Light Sword Blade",
        "max_den": 8.0,
        "min_str": 260,
        "max_cost": 10.0,
        "reward": 300,
    },
    {
        "client": "Brass Quintet",
        "desc": "Trumpet Bell",
        "max_den": 8.5,
        "min_str": 185,
        "max_cost": 7.0,
        "reward": 350,
        "require": ("Zinc (Zn)", 0.30),
    },
    {
        "client": "Chem Plant",
        "desc": "Corrosion-Proof Pipe",
        "max_den": 8.0,
        "min_str": 290,
        "max_cost": 6.0,
        "reward": 500,
        "require": ("Chromium (Cr)", 0.12),
    },
    {
        "client": "AeroSpace Lab",
        "desc": "Lightweight Jet Strut",
        "max_den": 5.5,
        "min_str": 350,
        "max_cost": 40.0,
        "reward": 600,
    },
    {
        "client": "Royal Mint",
        "desc": "Lustrous Golden Coin",
        "max_den": 20.0,
        "min_str": 80,
        "max_cost": 70.0,
        "reward": 800,
        "require": ("Gold (Au)", 0.30),
    },
    {
        "client": "Jewelry House",
        "desc": "Ancient Electrum Crown",
        "max_den": 16.0,
        "min_str": 120,
        "max_cost": 50.0,
        "reward": 950,
        "require": ("Silver (Ag)", 0.25),
    },
    {
        "client": "Grid Power Corp",
        "desc": "High-Temp Heating Element",
        "max_den": 8.8,
        "min_str": 320,
        "max_cost": 25.0,
        "reward": 1100,
        "require": ("Nickel (Ni)", 0.30),
    },
    {
        "client": "Defense Tech",
        "desc": "Armor-Piercing Core",
        "max_den": 18.0,
        "min_str": 450,
        "max_cost": 35.0,
        "reward": 1500,
        "require": ("Tungsten (W)", 0.35),
    },
]

BELLOWS_SPEED = (1.0, 1.8, 2.5, 3.5)
ANVIL_HALF_WIDTH = (0.07, 0.09, 0.11, 0.13)
BAR_SPEED = (2.2, 1.8, 1.5, 1.2)
MASTERY_BONUS = (0.15, 0.20, 0.25)
MASTERY_CAP = (1.6, 1.8, 2.0)
QUENCH_MULT = (1.45, 1.60)
SUPPLIER_COST = (1.0, 0.9, 0.8, 0.7)
REPUTATION = (1.0, 1.2, 1.4, 1.6)

UPGRADES = [
    {
        "id": "bellows",
        "name": "Bellows",
        "costs": (150, 300, 600),
        "desc": "Furnace heats faster and stays hot longer.",
    },
    {
        "id": "anvil",
        "name": "Heavy Anvil",
        "costs": (120, 250, 500),
        "desc": "Widens the perfect-strike zone on the hammer bar.",
    },
    {
        "id": "hands",
        "name": "Steady Hands",
        "costs": (100, 220, 450),
        "desc": "Slows the timing bar so strikes are easier to hit.",
    },
    {
        "id": "mastery",
        "name": "Forge Mastery",
        "costs": (300, 700),
        "desc": "Perfect strikes yield higher strength bonuses and quality cap.",
    },
    {
        "id": "brine",
        "name": "Brine Quench",
        "costs": (250,),
        "desc": "Boosts strength gain when quenching hot metal.",
    },
    {
        "id": "supplier",
        "name": "Bulk Supplier",
        "costs": (200, 400, 800),
        "desc": "Reduces raw-material production costs.",
    },
    {
        "id": "reputation",
        "name": "Reputation",
        "costs": (250, 500, 1000),
        "desc": "Increases contract payout rewards.",
    },
    {
        "id": "analyzer",
        "name": "Spec Analyzer",
        "costs": (180,),
        "desc": "Shows real-time pass/fail status for contract specs.",
    },
    {
        "id": "unlock_ti",
        "name": "Titanium",
        "costs": (300,),
        "unlock": "Titanium (Ti)",
        "desc": "Unlocks lightweight, high-strength Titanium.",
    },
    {
        "id": "unlock_au",
        "name": "Gold Supply",
        "costs": (400,),
        "unlock": "Gold (Au)",
        "desc": "Unlocks Gold, needed for Royal Mint contracts.",
    },
    {
        "id": "unlock_ag",
        "name": "Silver Supply",
        "costs": (350,),
        "unlock": "Silver (Ag)",
        "desc": "Unlocks Silver for jewelry and high-conductivity alloys.",
    },
    {
        "id": "unlock_al",
        "name": "Aluminum",
        "costs": (200,),
        "unlock": "Aluminum (Al)",
        "desc": "Unlocks low-density Aluminum.",
    },
    {
        "id": "unlock_ni",
        "name": "Nickel Supply",
        "costs": (450,),
        "unlock": "Nickel (Ni)",
        "desc": "Unlocks high-temperature Nickel.",
    },
    {
        "id": "unlock_w",
        "name": "Tungsten",
        "costs": (600,),
        "unlock": "Tungsten (W)",
        "desc": "Unlocks ultra-dense, ultra-strong Tungsten.",
    },
]

UPGRADES_BY_ID = {upgrade["id"]: upgrade for upgrade in UPGRADES}


def clamp(value, low, high):
    return max(low, min(value, high))


def short(name):
    return name.split(" (", 1)[0]


def create_procedural_sounds():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        except Exception:
            return {}

    mixer_info = pygame.mixer.get_init()
    if not mixer_info:
        return {}

    sample_rate = mixer_info[0]
    channel_count = mixer_info[2]

    def make_sound(duration, func, volume=0.25):
        try:
            num_samples = int(sample_rate * duration)
            samples = array.array("h")

            for i in range(num_samples):
                t = i / sample_rate
                value, envelope = func(t, duration)
                sample = int(32767 * volume * envelope * value)
                sample = max(-32768, min(32767, sample))

                samples.append(sample)
                for _ in range(channel_count - 1):
                    samples.append(sample)

            if sys.byteorder != "little":
                samples.byteswap()

            return pygame.mixer.Sound(buffer=samples.tobytes())
        except Exception:
            return None

    return {
        "hammer": make_sound(
            0.15,
            lambda t, duration: (
                math.sin(2 * math.pi * 880 * t)
                + 0.5 * math.sin(2 * math.pi * 1760 * t),
                math.exp(-25 * t),
            ),
            volume=0.35,
        ),
        "heat": make_sound(
            0.3,
            lambda t, duration: (
                random.uniform(-1.0, 1.0) * 0.5
                + math.sin(2 * math.pi * 110 * t),
                math.sin(math.pi * t / duration),
            ),
            volume=0.25,
        ),
        "quench": make_sound(
            0.45,
            lambda t, duration: (
                random.uniform(-1.0, 1.0),
                math.exp(-6 * t),
            ),
            volume=0.35,
        ),
        "success": make_sound(
            0.35,
            lambda t, duration: (
                math.sin(
                    2 * math.pi * (523.25 if t < 0.18 else 659.25) * t
                ),
                1.0 - t / duration,
            ),
            volume=0.3,
        ),
        "fail": make_sound(
            0.3,
            lambda t, duration: (
                1.0 if math.sin(2 * math.pi * 120 * t) > 0 else -1.0,
                math.exp(-7 * t),
            ),
            volume=0.25,
        ),
        "click": make_sound(
            0.04,
            lambda t, duration: (
                math.sin(2 * math.pi * 1200 * t),
                1.0 - t / duration,
            ),
            volume=0.15,
        ),
    }


class TextCache:
    def __init__(self, max_items=512):
        self.max_items = max_items
        self.items = OrderedDict()

    def render(self, font, text, color):
        key = (id(font), text, color)
        surface = self.items.get(key)
        if surface is not None:
            self.items.move_to_end(key)
            return surface

        surface = font.render(text, True, color)
        self.items[key] = surface
        if len(self.items) > self.max_items:
            self.items.popitem(last=False)
        return surface


class FloatingText:
    def __init__(self, x, y, text, color, font):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.surface = font.render(text, True, color)
        self.life = 1.2
        self.vy = -35.0

    def update(self, dt):
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return

        self.surface.set_alpha(
            max(0, min(255, int(255 * (self.life / 1.2))))
        )
        rect = self.surface.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(self.surface, rect)


class Particle:
    def __init__(self, x, y, particle_type):
        self.x = x
        self.y = y
        self.particle_type = particle_type
        self.life = 1.0
        self.size = random.randint(2, 5)

        if particle_type == "spark":
            angle = random.uniform(0, math.tau)
            speed = random.uniform(140, 450)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
            self.color = (255, random.randint(180, 255), 60)
        elif particle_type == "steam":
            self.vx = random.uniform(-60, 60)
            self.vy = random.uniform(-250, -130)
            self.color = (210, 230, 255)
        else:
            self.vx = random.uniform(-30, 30)
            self.vy = random.uniform(-120, -50)
            self.color = (255, random.randint(60, 160), 20)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.particle_type == "spark":
            self.vy += 900 * dt
            self.life -= 2.4 * dt
        else:
            self.life -= 1.2 * dt

    def draw(self, surface):
        if self.life <= 0:
            return

        radius = max(1, int(self.size * self.life))
        color = tuple(int(channel * self.life) for channel in self.color)
        pygame.draw.circle(
            surface, color, (int(self.x), int(self.y)), radius
        )


class Slider:
    def __init__(self, x, y, width, label, font):
        if width < 2:
            raise ValueError("Slider width must be at least 2 pixels")

        self.rect = pygame.Rect(x, y, width, 14)
        self.value = 50.0
        self.label = label
        self.font = font
        self.handle_radius = 9
        self.is_dragging = False
        self._cached_text = None
        self._cached_key = None

    def set_value(self, value):
        self.value = clamp(float(value), 0.0, 100.0)

    def draw(self, surface):
        pygame.draw.rect(surface, (70, 70, 80), self.rect, border_radius=4)
        travel = self.rect.width - 1
        handle_x = self.rect.left + round(self.value / 100.0 * travel)
        color = (255, 255, 255) if self.is_dragging else (190, 190, 200)
        pygame.draw.circle(
            surface, color, (handle_x, self.rect.centery), self.handle_radius
        )

        key = (self.label, round(self.value))
        if key != self._cached_key:
            self._cached_text = self.font.render(
                f"{self.label}: {round(self.value)}%", True, TEXT
            )
            self._cached_key = key

        surface.blit(self._cached_text, (self.rect.x, self.rect.y - 22))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.inflate(10, 20).collidepoint(event.pos):
                self.is_dragging = True
                self.update_value(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.update_value(event.pos[0])

    def update_value(self, mouse_x):
        x = clamp(mouse_x, self.rect.left, self.rect.right - 1)
        ratio = (x - self.rect.left) / (self.rect.width - 1)
        self.set_value(ratio * 100.0)


class Button:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        text,
        color,
        hover_color,
        font,
        hotkey_text=None,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.hotkey_text = hotkey_text
        self.is_hovered = False
        self.enabled = True
        self._text = None
        self._text_color = None
        self._surface = None
        self._text_rect = None
        self.set_text(text)

    def set_text(self, text, color=(255, 255, 255)):
        full_text = f"{text} [{self.hotkey_text}]" if self.hotkey_text else text
        if (full_text, color) == (self._text, self._text_color):
            return

        self._text = full_text
        self._text_color = color
        self._surface = self.font.render(full_text, True, color)

        max_width = max(1, self.rect.width - 12)
        if self._surface.get_width() > max_width:
            ratio = max_width / self._surface.get_width()
            new_size = (
                max_width,
                max(1, round(self._surface.get_height() * ratio)),
            )
            self._surface = pygame.transform.smoothscale(
                self._surface, new_size
            )

        self._text_rect = self._surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        if not self.enabled:
            fill, border = (45, 45, 52), (80, 80, 90)
        else:
            fill = self.hover_color if self.is_hovered else self.color
            border = (180, 180, 190)

        pygame.draw.rect(surface, fill, self.rect, border_radius=6)
        pygame.draw.rect(
            surface, border, self.rect, width=2, border_radius=6
        )
        surface.blit(self._surface, self._text_rect)

    def update(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def is_clicked(self, event):
        return (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class AlloyForgeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.canvas = pygame.Surface((WIDTH, HEIGHT))

        self.heat_glow_surface = pygame.Surface(
            (240, 240), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.heat_glow_surface,
            (255, 100, 20, 255),
            (0, 0, 240, 240),
            border_radius=16,
        )

        self.text_cache = TextCache()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(
            f"Alloy Forge: Master Smith {VERSION}"
        )

        self.font_large = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 20)

        self.sounds = create_procedural_sounds()

        self.elements = tuple(ELEMENTS)
        self.unlocked = {
            name: data["unlocked"] for name, data in ELEMENTS.items()
        }
        self.active = [self.elements[0], self.elements[1]]

        self.temperature = 25.0
        self.target_temp = 25.0
        self.heat_timer = 0.0
        self.is_quenched = False
        self.money = 150
        self.contract_idx = 0
        self.completed = 0
        self.quality_bonus = 1.0
        self.unlocked_recipes = set()
        self.show_codex = False
        self.status_msg = "Mix metals, heat furnace, hammer, quench, then submit!"

        self.levels = {upgrade["id"]: 0 for upgrade in UPGRADES}
        self.particles = []
        self.floating_texts = []
        self.shake = 0.0
        self.hammer_pos = 0.0
        self.hammer_dir = 1
        self.hammer_active = False
        self.hammer_swing = 0.0

        self.setup_ui()
        self.load_game()
        self.refresh_shop()

    def play_sfx(self, name):
        if name in self.sounds and self.sounds[name]:
            try:
                self.sounds[name].play()
            except Exception:
                pass

    def add_floating_text(self, x, y, text, color):
        if len(self.floating_texts) >= MAX_FLOATING_TEXTS:
            self.floating_texts.pop(0)

        self.floating_texts.append(
            FloatingText(x, y, text, color, self.font_medium)
        )

    def setup_ui(self):
        self.s1 = Slider(40, 130, 220, self.active[0], self.font_small)
        self.s2 = Slider(40, 210, 220, self.active[1], self.font_small)

        self.btn_heat = Button(
            360, 520, 120, 40, "HEAT",
            (180, 50, 50), (220, 70, 70), self.font_medium,
            hotkey_text="H",
        )
        self.btn_hammer = Button(
            490, 520, 140, 40, "HAMMER!",
            (200, 140, 30), (230, 170, 40), self.font_medium,
            hotkey_text="SPACE",
        )
        self.btn_quench = Button(
            640, 520, 120, 40, "QUENCH",
            (50, 100, 180), (70, 130, 220), self.font_medium,
            hotkey_text="Q",
        )
        self.btn_submit = Button(
            770, 520, 150, 40, "SUBMIT",
            (40, 150, 60), (60, 190, 80), self.font_medium,
            hotkey_text="S",
        )
        self.btn_c1 = Button(
            270, 120, 30, 22, ">",
            (70, 70, 80), (100, 100, 110), self.font_small,
            hotkey_text="1",
        )
        self.btn_c2 = Button(
            270, 200, 30, 22, ">",
            (70, 70, 80), (100, 100, 110), self.font_small,
            hotkey_text="2",
        )
        self.btn_codex = Button(
            930, 462, 110, 28, "CODEX",
            (80, 70, 30), (120, 100, 40), self.font_small,
            hotkey_text="C",
        )

        self.shop_buttons = {}
        for index, upgrade in enumerate(UPGRADES):
            x = 40 + (index % 5) * 206
            y = 608 + (index // 5) * 32
            self.shop_buttons[upgrade["id"]] = Button(
                x, y, 196, 28, upgrade["name"],
                (80, 60, 100), (110, 80, 140), self.font_small,
            )

        self.buttons = [
            self.btn_heat,
            self.btn_hammer,
            self.btn_quench,
            self.btn_submit,
            self.btn_c1,
            self.btn_c2,
            self.btn_codex,
            *self.shop_buttons.values(),
        ]

    def save_game(self):
        data = {
            "version": SAVE_VERSION,
            "money": self.money,
            "contract_idx": self.contract_idx,
            "completed": self.completed,
            "quality_bonus": self.quality_bonus,
            "is_quenched": self.is_quenched,
            "levels": self.levels,
            "unlocked_recipes": sorted(self.unlocked_recipes),
            "active_elements": self.active,
            "mix": [self.s1.value, self.s2.value],
        }

        temp_path = SAVE_FILE.with_name(SAVE_FILE.name + ".tmp")
        try:
            SAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
            temp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            temp_path.replace(SAVE_FILE)
        except (OSError, TypeError, ValueError):
            self.status_msg = "Progress could not be saved."
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass

    def load_game(self):
        try:
            data = json.loads(SAVE_FILE.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return
        except (OSError, json.JSONDecodeError):
            self.status_msg = "Save file could not be read; starting fresh."
            return

        if not isinstance(data, dict) or data.get("version") != SAVE_VERSION:
            self.status_msg = "Save version is incompatible; starting fresh."
            return

        money = data.get("money")
        if type(money) is int:
            self.money = max(0, money)

        contract_idx = data.get("contract_idx")
        if type(contract_idx) is int:
            self.contract_idx = int(
                clamp(contract_idx, 0, len(CONTRACTS) - 1)
            )

        completed = data.get("completed")
        if type(completed) is int:
            self.completed = max(0, completed)

        saved_levels = data.get("levels", {})
        if isinstance(saved_levels, dict):
            for upgrade in UPGRADES:
                upgrade_id = upgrade["id"]
                level = saved_levels.get(upgrade_id, 0)
                if type(level) is int:
                    self.levels[upgrade_id] = int(
                        clamp(level, 0, len(upgrade["costs"]))
                    )

        for upgrade in UPGRADES:
            if "unlock" in upgrade and self.levels[upgrade["id"]] > 0:
                self.unlocked[upgrade["unlock"]] = True

        saved_recipes = data.get("unlocked_recipes", [])
        valid_recipes = set(RECIPES.values())
        if isinstance(saved_recipes, list):
            self.unlocked_recipes = {
                recipe
                for recipe in saved_recipes
                if isinstance(recipe, str) and recipe in valid_recipes
            }

        active = data.get("active_elements")
        if (
            isinstance(active, list)
            and len(active) == 2
            and all(
                isinstance(name, str) and name in ELEMENTS
                for name in active
            )
            and active[0] != active[1]
            and all(self.unlocked[name] for name in active)
        ):
            self.active = active
            self.s1.label, self.s2.label = active
            self.s1._cached_key = None
            self.s2._cached_key = None

        mix = data.get("mix")
        if (
            isinstance(mix, list)
            and len(mix) == 2
            and all(
                isinstance(value, (int, float)) and math.isfinite(value)
                for value in mix
            )
        ):
            first, second = (
                clamp(float(value), 0.0, 100.0) for value in mix
            )
            total = first + second
            if total > 0:
                self.s1.set_value(first * 100.0 / total)
                self.s2.set_value(100.0 - self.s1.value)

        quality = data.get("quality_bonus")
        if isinstance(quality, (int, float)) and math.isfinite(quality):
            max_quality = MASTERY_CAP[self.lvl("mastery")]
            self.quality_bonus = clamp(float(quality), 0.8, max_quality)

        self.is_quenched = data.get("is_quenched") is True
        self.status_msg = "Saved progress loaded."

    def text(self, text, font, color):
        return self.text_cache.render(font, text, color)

    def draw_text(self, surface, text, font, color, position):
        surface.blit(self.text(text, font, color), position)

    def lvl(self, upgrade_id):
        return self.levels[upgrade_id]

    def reward_for(self, contract):
        return int(contract["reward"] * REPUTATION[self.lvl("reputation")])

    def get_fraction(self, element):
        fraction = 0.0
        if self.active[0] == element:
            fraction += self.s1.value / 100.0
        if self.active[1] == element:
            fraction += self.s2.value / 100.0
        return fraction

    def cycle_element(self, index):
        self.play_sfx("click")
        current = self.elements.index(self.active[index])
        changed = False

        for step in range(1, len(self.elements)):
            candidate = self.elements[(current + step) % len(self.elements)]
            if candidate not in self.active and self.unlocked[candidate]:
                self.active[index] = candidate
                slider = self.s1 if index == 0 else self.s2
                slider.label = candidate
                slider._cached_key = None
                changed = True
                break

        if changed:
            self.save_game()

    def get_stats(self):
        first = ELEMENTS[self.active[0]]
        second = ELEMENTS[self.active[1]]
        p1 = self.s1.value / 100.0
        p2 = self.s2.value / 100.0

        density = p1 * first["density"] + p2 * second["density"]
        strength = p1 * first["strength"] + p2 * second["strength"]
        strength *= self.quality_bonus
        cost = p1 * first["cost"] + p2 * second["cost"]
        cost *= SUPPLIER_COST[self.lvl("supplier")]

        if self.is_quenched:
            strength *= QUENCH_MULT[self.lvl("brine")]

        return density, strength, cost

    def get_alloy_name(self):
        present = set()
        if self.s1.value > 2.0:
            present.add(self.active[0])
        if self.s2.value > 2.0:
            present.add(self.active[1])

        recipe = RECIPES.get(frozenset(present))
        if recipe:
            return recipe
        if len(present) == 1:
            return next(iter(present))
        return "Custom Experimental Alloy"

    def update_recipe_unlocks(self):
        alloy_name = self.get_alloy_name()
        if (
            alloy_name in RECIPES.values()
            and alloy_name not in self.unlocked_recipes
        ):
            self.unlocked_recipes.add(alloy_name)
            self.save_game()

    def toggle_codex(self):
        self.show_codex = not self.show_codex
        self.btn_codex.set_text("CLOSE" if self.show_codex else "CODEX")

    def contract_checks(self, stats=None):
        contract = CONTRACTS[self.contract_idx]
        density, strength, cost = (
            stats if stats is not None else self.get_stats()
        )
        checks = {
            "den": density <= contract["max_den"],
            "str": strength >= contract["min_str"],
            "cost": cost <= contract["max_cost"],
        }

        if "require" in contract:
            name, minimum_fraction = contract["require"]
            checks["req"] = (
                self.get_fraction(name) >= minimum_fraction - 1e-9
            )

        return checks

    def trigger_shake(self, intensity=8.0):
        self.shake = intensity

    def buy(self, upgrade_id):
        upgrade = UPGRADES_BY_ID[upgrade_id]
        level = self.levels[upgrade_id]
        if level >= len(upgrade["costs"]):
            return

        cost = upgrade["costs"][level]
        if self.money < cost:
            self.play_sfx("fail")
            self.status_msg = (
                f"Not enough gold for {upgrade['name']} (${cost} required)."
            )
            return

        self.play_sfx("click")
        self.money -= cost
        self.levels[upgrade_id] += 1

        if "unlock" in upgrade:
            element = upgrade["unlock"]
            self.unlocked[element] = True
            self.status_msg = (
                f"Unlocked {short(element)}! Cycle to it using buttons or keys [1/2]."
            )
            self.add_floating_text(
                515, 300, f"UNLOCKED {short(element).upper()}!", GOLD
            )
        else:
            self.status_msg = (
                f"{upgrade['name']} upgraded to Level {self.levels[upgrade_id]}!"
            )
            self.add_floating_text(
                515, 300, f"+{upgrade['name'].upper()} LEVEL", CYAN
            )

        self.save_game()

    def refresh_shop(self):
        for upgrade in UPGRADES:
            button = self.shop_buttons[upgrade["id"]]
            level = self.levels[upgrade["id"]]
            count = len(upgrade["costs"])

            if level >= count:
                button.enabled = False
                label = (
                    f"{upgrade['name']}: OWNED"
                    if count == 1
                    else f"{upgrade['name']} MAX"
                )
                button.set_text(label, MUTED)
                continue

            button.enabled = True
            cost = upgrade["costs"][level]
            label = (
                f"{upgrade['name']} ${cost}"
                if count == 1
                else f"{upgrade['name']} {level}/{count} ${cost}"
            )
            color = (
                (255, 255, 255)
                if self.money >= cost
                else (255, 140, 140)
            )
            button.set_text(label, color)

    def start_heating(self):
        self.play_sfx("heat")
        self.heat_timer = BELLOWS_HEAT_DURATION[self.lvl("bellows")]
        self.is_quenched = False
        self.hammer_active = True
        self.status_msg = "Furnace roaring hot! Time your hammer strikes."
        self.add_floating_text(515, 280, "FURNACE STOKED!", RED)

    def spawn_particles(self, x, y, particle_type, count):
        available = MAX_PARTICLES - len(self.particles)
        for _ in range(min(count, available)):
            self.particles.append(Particle(x, y, particle_type))

    def hammer_strike(self):
        if self.temperature <= 450:
            self.play_sfx("fail")
            self.status_msg = "Metal is too cold! Heat furnace above 450°C to shape."
            return

        self.play_sfx("hammer")
        self.trigger_shake(6.0)
        self.hammer_swing = 1.0
        self.spawn_particles(515, 220, "spark", 14)

        half_width = ANVIL_HALF_WIDTH[self.lvl("anvil")]
        if abs(self.hammer_pos - 0.5) <= half_width:
            gain = MASTERY_BONUS[self.lvl("mastery")]
            cap = MASTERY_CAP[self.lvl("mastery")]
            self.quality_bonus = min(cap, self.quality_bonus + gain)
            self.status_msg = (
                f"PERFECT STRIKE! Grain refined (+{gain * 100:.0f}% strength)."
            )
            self.add_floating_text(
                515, 200, f"PERFECT! +{gain * 100:.0f}%", GOLD
            )
        else:
            self.quality_bonus = max(0.8, self.quality_bonus - 0.05)
            self.status_msg = "Off-center strike. Metal grain misaligned."
            self.add_floating_text(515, 200, "MISALIGNED", RED)

        self.save_game()

    def quench(self):
        if self.temperature > 650:
            self.play_sfx("quench")
            self.is_quenched = True
            self.trigger_shake(10.0)
            self.spawn_particles(515, 220, "steam", 28)
            bonus = (QUENCH_MULT[self.lvl("brine")] - 1) * 100
            medium = "BRINE" if self.lvl("brine") else "STEAM"
            self.status_msg = (
                f"{medium} QUENCH! Locked in hard martensitic phase "
                f"(+{bonus:.0f}% strength)."
            )
            self.add_floating_text(
                515, 200, f"{medium} QUENCHED (+{bonus:.0f}%)", CYAN
            )
        else:
            self.play_sfx("fail")
            self.status_msg = "Metal must be glowing red (>650°C) to quench!"

        self.heat_timer = 0.0
        self.target_temp = 25.0
        self.hammer_active = False
        self.save_game()

    def submit_order(self):
        contract = CONTRACTS[self.contract_idx]
        if all(self.contract_checks().values()):
            self.play_sfx("success")
            reward = self.reward_for(contract)
            self.money += reward
            self.completed += 1
            self.status_msg = (
                f"CONTRACT APPROVED! Earned ${reward} from {contract['client']}!"
            )
            self.add_floating_text(880, 200, f"+${reward}", GREEN)
            self.contract_idx = (self.contract_idx + 1) % len(CONTRACTS)
            self.quality_bonus = 1.0
            self.is_quenched = False
            self.save_game()
        else:
            self.play_sfx("fail")
            self.status_msg = (
                "REJECTED! Material specs do not meet client requirements."
            )
            self.add_floating_text(880, 200, "REJECTED!", RED)

    def update(self, dt):
        if self.heat_timer > 0:
            self.heat_timer -= dt
            self.target_temp = 1400.0
        else:
            self.target_temp = 25.0

        rate = (
            0.7 * BELLOWS_SPEED[self.lvl("bellows")]
            if self.target_temp > 500
            else 0.35
        )
        blend = 1.0 - math.exp(-rate * dt)
        self.temperature += (self.target_temp - self.temperature) * blend
        self.update_recipe_unlocks()

        if (
            self.hammer_active
            and self.heat_timer <= 0
            and self.temperature <= 450
        ):
            self.hammer_active = False

        if self.hammer_active:
            self.hammer_pos += (
                self.hammer_dir * dt * BAR_SPEED[self.lvl("hands")]
            )
            if self.hammer_pos >= 1.0:
                self.hammer_pos, self.hammer_dir = 1.0, -1
            elif self.hammer_pos <= 0.0:
                self.hammer_pos, self.hammer_dir = 0.0, 1

        if self.hammer_swing > 0.0:
            self.hammer_swing = max(0.0, self.hammer_swing - dt * 4.5)

        if (
            self.temperature > 400
            and len(self.particles) < MAX_PARTICLES
            and random.random() < 30 * dt
        ):
            self.particles.append(
                Particle(510 + random.randint(-40, 40), 300, "ember")
            )

        for particle in self.particles:
            particle.update(dt)
        self.particles = [
            particle for particle in self.particles if particle.life > 0
        ]

        for floating_text in self.floating_texts:
            floating_text.update(dt)
        self.floating_texts = [
            floating_text
            for floating_text in self.floating_texts
            if floating_text.life > 0
        ]

        if self.shake > 0:
            self.shake = max(0.0, self.shake - dt * 30.0)

        self.refresh_shop()

    def draw_left(self, surface):
        self.s1.draw(surface)
        self.s2.draw(surface)
        self.draw_text(
            surface, "Selected Elements", self.font_medium, BLUE, (40, 295)
        )

        for index, name in enumerate(self.active):
            element = ELEMENTS[name]
            y = 325 + index * 48
            swatch = pygame.Rect(40, y + 2, 14, 14)
            pygame.draw.rect(surface, element["color"], swatch)
            pygame.draw.rect(surface, (150, 150, 160), swatch, width=1)
            self.draw_text(surface, name, self.font_small, TEXT, (62, y))
            info = (
                f"{element['density']} g/cm³  {element['strength']} MPa  "
                f"${element['cost']}/kg"
            )
            self.draw_text(surface, info, self.font_small, MUTED, (40, y + 18))

        locked = [short(name) for name in self.elements if not self.unlocked[name]]
        for index in range(0, len(locked), 3):
            prefix = "Locked: " if index == 0 else "         "
            self.draw_text(
                surface,
                prefix + ", ".join(locked[index:index + 3]),
                self.font_small,
                MUTED,
                (40, 440 + (index // 3) * 18),
            )

    def get_metal_color(self):
        p1 = self.s1.value / 100.0
        p2 = self.s2.value / 100.0
        first = ELEMENTS[self.active[0]]["color"]
        second = ELEMENTS[self.active[1]]["color"]
        base = tuple(p1 * first[i] + p2 * second[i] for i in range(3))
        glow = clamp((self.temperature - 200) / 1200, 0.0, 1.0)
        return (
            int(clamp(base[0] + (255 - base[0]) * glow, 0, 255)),
            int(clamp(base[1] + (140 - base[1]) * glow, 0, 255)),
            int(clamp(base[2] * (1.0 - glow), 0, 255)),
        )

    def draw_center(self, surface):
        crucible = pygame.Rect(415, 120, 200, 200)

        glow_alpha = int(clamp((self.temperature - 300) / 1100, 0, 1) * 60)
        if glow_alpha > 0:
            self.heat_glow_surface.set_alpha(glow_alpha)
            surface.blit(self.heat_glow_surface, (395, 100))

        pygame.draw.rect(
            surface, (15, 15, 18), crucible.inflate(16, 16), border_radius=12
        )
        pygame.draw.rect(surface, self.get_metal_color(), crucible, border_radius=8)

        temp_color = RED if self.temperature > 600 else TEXT
        temp_text = self.text(
            f"Temp: {int(self.temperature)}°C", self.font_medium, temp_color
        )
        surface.blit(temp_text, temp_text.get_rect(center=(515, 340)))

        # Timing Bar & Sweet Spot
        pygame.draw.rect(surface, (20, 20, 25), (360, 380, 310, 20), border_radius=5)
        half_width = ANVIL_HALF_WIDTH[self.lvl("anvil")]
        sweet_spot = pygame.Rect(
            int(360 + (0.5 - half_width) * 310),
            380,
            int(2 * half_width * 310),
            20,
        )
        pygame.draw.rect(surface, GREEN, sweet_spot)
        indicator_x = int(360 + self.hammer_pos * 310)
        pygame.draw.line(
            surface, GOLD, (indicator_x, 375), (indicator_x, 405), 4
        )

        # Swinging Hammer FX
        if self.hammer_swing > 0.0:
            angle = self.hammer_swing * 0.7
            hx = indicator_x + math.sin(angle) * 35
            hy = 370 - math.cos(angle) * 35
            pygame.draw.line(surface, (150, 100, 50), (indicator_x, 370), (hx, hy), 6)
            pygame.draw.rect(
                surface, (200, 200, 210), (hx - 8, hy - 6, 16, 12), border_radius=2
            )

        cap = MASTERY_CAP[self.lvl("mastery")]
        quality = f"Quality Bonus: {self.quality_bonus:.2f}x (Max {cap:.1f}x)"
        self.draw_text(surface, quality, self.font_small, GOLD, (360, 410))

    def draw_right(self, surface):
        contract = CONTRACTS[self.contract_idx]
        self.draw_text(surface, "Client Order", self.font_medium, GOLD, (740, 85))

        lines = [
            f"Client: {contract['client']}",
            f"Item: {contract['desc']}",
            f"Max Density: {contract['max_den']} g/cm³",
            f"Min Strength: {contract['min_str']} MPa",
            f"Max Cost: ${contract['max_cost']} / kg",
        ]
        if "require" in contract:
            name, fraction = contract["require"]
            lines.append(f"Needs: {short(name)} >= {fraction * 100:.0f}%")
        lines.append(f"Reward: ${self.reward_for(contract)}")

        for index, line in enumerate(lines):
            self.draw_text(
                surface, line, self.font_small, TEXT, (740, 115 + index * 19)
            )

        pygame.draw.line(surface, (60, 60, 70), (730, 255), (1050, 255), 2)
        self.draw_text(
            surface, "Material Specs", self.font_medium, BLUE, (740, 262)
        )

        stats = self.get_stats()
        density, strength, cost = stats
        checks = self.contract_checks(stats)
        rows = [
            (f"Alloy: {self.get_alloy_name()}", None),
            (f"Density: {density:.2f} g/cm³", checks["den"]),
            (f"Yield Strength: {strength:.0f} MPa", checks["str"]),
            (f"Cost: ${cost:.2f} / kg", checks["cost"]),
            (f"State: {'Quenched' if self.is_quenched else 'Normal'}", None),
        ]
        if "req" in checks:
            name, fraction = contract["require"]
            have = self.get_fraction(name) * 100
            rows.append((
                f"{short(name)}: {have:.0f}% (need {fraction * 100:.0f}%)",
                checks["req"],
            ))

        analyzer = self.lvl("analyzer") > 0
        for index, (line, passed) in enumerate(rows):
            color = TEXT
            if analyzer and passed is not None:
                color = GREEN if passed else RED
            self.draw_text(
                surface, line, self.font_small, color, (740, 290 + index * 20)
            )

        y = 290 + len(rows) * 20 + 8
        if analyzer:
            ready = all(checks.values())
            label = "READY TO SUBMIT" if ready else "Specs not met yet"
            color = GREEN if ready else RED
            self.draw_text(surface, label, self.font_medium, color, (740, y))
        else:
            self.draw_text(
                surface,
                "Tip: Spec Analyzer shows pass/fail.",
                self.font_small,
                MUTED,
                (740, y),
            )

    def draw_shop(self, surface):
        self.draw_text(
            surface, "Workshop Upgrades", self.font_medium, GOLD, (40, 582)
        )
        tip = "Hover an upgrade to view details."
        for upgrade in UPGRADES:
            if self.shop_buttons[upgrade["id"]].is_hovered:
                tip = upgrade["desc"]
                break
        self.draw_text(surface, tip, self.font_small, (170, 170, 180), (280, 585))

    def draw_codex(self, surface):
        if not self.show_codex:
            return

        panel = pygame.Rect(300, 130, 500, 480)
        pygame.draw.rect(surface, (18, 18, 22), panel, border_radius=12)
        pygame.draw.rect(surface, GOLD, panel, width=2, border_radius=12)
        self.draw_text(surface, "Recipe Codex", self.font_large, GOLD, (335, 160))

        if self.unlocked_recipes:
            for index, recipe in enumerate(sorted(self.unlocked_recipes)):
                self.draw_text(
                    surface, f"★ {recipe}", self.font_medium, GOLD,
                    (340, 220 + index * 28),
                )
        else:
            self.draw_text(
                surface, "Mix metals to discover alloy recipes.",
                self.font_medium, MUTED, (340, 220),
            )

        self.draw_text(
            surface, "Press C or click CLOSE to return.",
            self.font_small, MUTED, (340, 570),
        )

    def draw(self):
        surface = self.canvas
        surface.fill(BACKGROUND)

        title = self.text("ALLOY FORGE: MASTER SMITH", self.font_large, GOLD)
        surface.blit(title, title.get_rect(midtop=(WIDTH // 2, 15)))
        self.draw_text(
            surface, f"Gold: ${self.money}", self.font_medium, GREEN, (940, 20)
        )
        self.draw_text(
            surface,
            f"Orders filled: {self.completed}",
            self.font_medium,
            TEXT,
            (40, 22),
        )

        panels = (
            (25, 70, 290, 430),
            (330, 70, 370, 430),
            (720, 70, 350, 430),
            (25, 575, 1050, 125),
            (25, 708, 1050, 34),
        )
        for rect in panels:
            pygame.draw.rect(surface, PANEL, rect, border_radius=10)

        self.draw_left(surface)
        self.draw_center(surface)
        self.draw_right(surface)
        self.draw_shop(surface)

        for button in self.buttons:
            button.draw(surface)
        for particle in self.particles:
            particle.draw(surface)
        for ft in self.floating_texts:
            ft.draw(surface)

        self.draw_text(
            surface, f"> {self.status_msg}", self.font_medium, TEXT, (40, 716)
        )
        self.draw_codex(surface)

        offset = (0, 0)
        if self.shake > 0:
            offset = (
                int(random.uniform(-self.shake, self.shake)),
                int(random.uniform(-self.shake, self.shake)),
            )
        self.screen.fill(BACKGROUND)
        self.screen.blit(surface, offset)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_c:
                    self.toggle_codex()
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self.hammer_strike()
                elif event.key == pygame.K_h:
                    self.start_heating()
                elif event.key == pygame.K_q:
                    self.quench()
                elif event.key == pygame.K_s:
                    self.submit_order()
                elif event.key == pygame.K_1:
                    self.cycle_element(0)
                elif event.key == pygame.K_2:
                    self.cycle_element(1)

            self.s1.handle_event(event)
            self.s2.handle_event(event)
            if self.s1.is_dragging:
                self.s2.set_value(100.0 - self.s1.value)
            elif self.s2.is_dragging:
                self.s1.set_value(100.0 - self.s2.value)

            if self.btn_c1.is_clicked(event):
                self.cycle_element(0)
            elif self.btn_c2.is_clicked(event):
                self.cycle_element(1)
            elif self.btn_codex.is_clicked(event):
                self.toggle_codex()

            for upgrade_id, button in self.shop_buttons.items():
                if button.is_clicked(event):
                    self.buy(upgrade_id)

            if self.btn_heat.is_clicked(event):
                self.start_heating()
            elif self.btn_hammer.is_clicked(event):
                self.hammer_strike()
            elif self.btn_quench.is_clicked(event):
                self.quench()
            elif self.btn_submit.is_clicked(event):
                self.submit_order()

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.save_game()

        return True

    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.update(mouse_pos)

            running = self.handle_events()
            if running:
                self.update(dt)
                self.draw()

        self.save_game()
        pygame.quit()


if __name__ == "__main__":
    AlloyForgeGame().run()
    
import io
import math
import random
import sys
import cairo
import pygame

# Inisialisasi Pygame
pygame.init()

# Pengaturan Resolusi Layar Game
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyroForest - Edukasi Bencana KARHUTLA")

clock = pygame.time.Clock()


# --- FUNGSI PEMBUAT ASET VECTOR MENGGUNAKAN PYCAIRO ---
def cairo_surface_to_pygame(surface):
  """Mengonversi Pycairo Surface ke Pygame Surface via BytesIO"""
  bio = io.BytesIO()
  surface.write_to_png(bio)
  bio.seek(0)
  return pygame.image.load(bio).convert_alpha()


def make_dark_bg_transparent(surface, threshold=22):
  """Menghapus latar belakang hitam pekat pada sprite/map menjadi transparan"""
  surf = surface.convert_alpha()
  w, h = surf.get_size()
  for y in range(h):
    for x in range(w):
      r, g, b, a = surf.get_at((x, y))
      if r <= threshold and g <= threshold and b <= threshold:
        surf.set_at((x, y), (r, g, b, 0))
  return surf


def generate_fire_asset(w, h):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)
  ctx.move_to(w * 0.5, h * 0.05)
  ctx.curve_to(w * 0.85, h * 0.4, w * 0.95, h * 0.8, w * 0.5, h * 0.95)
  ctx.curve_to(w * 0.05, h * 0.8, w * 0.15, h * 0.4, w * 0.5, h * 0.05)
  ctx.set_source_rgb(1.0, 0.3, 0.0)
  ctx.fill_preserve()
  ctx.set_source_rgb(1.0, 0.85, 0.1)
  ctx.set_line_width(3)
  ctx.stroke()
  return cairo_surface_to_pygame(surf)


def generate_smoke_asset(w, h):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)
  ctx.set_source_rgba(0.85, 0.85, 0.85, 0.65)
  ctx.arc(w * 0.4, h * 0.6, w * 0.25, 0, 2 * math.pi)
  ctx.fill()
  ctx.arc(w * 0.7, h * 0.4, w * 0.3, 0, 2 * math.pi)
  ctx.fill()
  ctx.arc(w * 0.5, h * 0.3, w * 0.2, 0, 2 * math.pi)
  ctx.fill()
  return cairo_surface_to_pygame(surf)


def generate_water_asset(w, h):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)
  ctx.move_to(w * 0.5, h * 0.1)
  ctx.curve_to(w * 0.85, h * 0.6, w * 0.9, h * 0.9, w * 0.5, h * 0.95)
  ctx.curve_to(w * 0.1, h * 0.9, w * 0.15, h * 0.6, w * 0.5, h * 0.1)
  ctx.set_source_rgba(0.1, 0.6, 1.0, 0.9)
  ctx.fill()
  return cairo_surface_to_pygame(surf)


def generate_burning_tree_asset(w, h):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)

  # Batang Kayu Coklat dengan Tekstur Garis Vertikal
  ctx.rectangle(w * 0.38, h * 0.45, w * 0.24, h * 0.5)
  ctx.set_source_rgb(0.38, 0.25, 0.16)
  ctx.fill()

  ctx.set_source_rgb(0.25, 0.15, 0.08)
  ctx.set_line_width(2)
  ctx.move_to(w * 0.45, h * 0.5)
  ctx.line_to(w * 0.45, h * 0.9)
  ctx.move_to(w * 0.55, h * 0.55)
  ctx.line_to(w * 0.55, h * 0.85)
  ctx.stroke()

  # Tajuk Daun Berlapis (Gaya Pixel Pine)
  ctx.move_to(w * 0.1, h * 0.5)
  ctx.line_to(w * 0.9, h * 0.5)
  ctx.line_to(w * 0.7, h * 0.35)
  ctx.line_to(w * 0.85, h * 0.35)
  ctx.line_to(w * 0.5, h * 0.12)
  ctx.line_to(w * 0.15, h * 0.35)
  ctx.line_to(w * 0.3, h * 0.35)
  ctx.close_path()
  ctx.set_source_rgb(0.24, 0.38, 0.31)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.15, 0.25, 0.2)
  ctx.set_line_width(3)
  ctx.stroke()

  return cairo_surface_to_pygame(surf)


def generate_well_asset(w, h):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)

  # 1. Dinding Kotak Bawah
  ctx.rectangle(w * 0.15, h * 0.45, w * 0.7, h * 0.35)
  ctx.set_source_rgb(0.65, 0.65, 0.7)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.2, 0.2, 0.25)
  ctx.set_line_width(2.5)
  ctx.stroke()

  # Garis-garis Tekstur Batu Bata Kotak
  ctx.set_source_rgb(0.35, 0.35, 0.4)
  ctx.set_line_width(1.5)
  ctx.move_to(w * 0.25, h * 0.53)
  ctx.line_to(w * 0.48, h * 0.53)
  ctx.move_to(w * 0.55, h * 0.53)
  ctx.line_to(w * 0.75, h * 0.53)
  ctx.move_to(w * 0.2, h * 0.63)
  ctx.line_to(w * 0.42, h * 0.63)
  ctx.move_to(w * 0.48, h * 0.63)
  ctx.line_to(w * 0.8, h * 0.63)
  ctx.move_to(w * 0.45, h * 0.45)
  ctx.line_to(w * 0.45, h * 0.53)
  ctx.move_to(w * 0.35, h * 0.53)
  ctx.line_to(w * 0.35, h * 0.63)
  ctx.move_to(w * 0.65, h * 0.53)
  ctx.line_to(w * 0.65, h * 0.63)
  ctx.stroke()

  # 2. Bibir Atas Sumur & Permukaan Air di Dalamnya
  ctx.save()
  ctx.scale(1.0, 0.3)
  ctx.arc((w * 0.5) / 1.0, (h * 0.45) / 0.3, w * 0.35, 0, 2 * math.pi)
  ctx.restore()
  ctx.set_source_rgb(0.5, 0.5, 0.55)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.2, 0.2, 0.2)
  ctx.set_line_width(2)
  ctx.stroke()

  # Permukaan Air Biru di Mulut Sumur
  ctx.save()
  ctx.scale(1.0, 0.24)
  ctx.arc((w * 0.5) / 1.0, (h * 0.45) / 0.24, w * 0.28, 0, 2 * math.pi)
  ctx.restore()
  ctx.set_source_rgba(0.1, 0.6, 1.0, 0.9)
  ctx.fill()

  # 3. Tiang Penyangga Kayu Kiri & Kanan
  ctx.set_source_rgb(0.45, 0.28, 0.12)
  ctx.set_line_width(5)
  ctx.move_to(w * 0.25, h * 0.45)
  ctx.line_to(w * 0.25, h * 0.22)
  ctx.move_to(w * 0.75, h * 0.45)
  ctx.line_to(w * 0.75, h * 0.22)
  ctx.stroke()

  # Poros / Gulungan Tali & Tali di Tengah
  ctx.arc(w * 0.5, h * 0.28, w * 0.05, 0, 2 * math.pi)
  ctx.set_source_rgb(0.35, 0.2, 0.08)
  ctx.fill()
  ctx.set_source_rgb(0.8, 0.75, 0.6)
  ctx.set_line_width(2.5)
  ctx.move_to(w * 0.5, h * 0.33)
  ctx.line_to(w * 0.5, h * 0.45)
  ctx.stroke()

  # 4. Atap Sumur
  ctx.move_to(w * 0.1, h * 0.22)
  ctx.line_to(w * 0.5, h * 0.05)
  ctx.line_to(w * 0.9, h * 0.22)
  ctx.close_path()
  ctx.set_source_rgb(0.55, 0.22, 0.12)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.25, 0.1, 0.05)
  ctx.set_line_width(2.5)
  ctx.stroke()

  # Garis Tekstur Atap
  ctx.set_source_rgb(0.35, 0.15, 0.08)
  ctx.set_line_width(1.5)
  ctx.move_to(w * 0.33, h * 0.13)
  ctx.line_to(w * 0.36, h * 0.22)
  ctx.move_to(w * 0.5, h * 0.05)
  ctx.line_to(w * 0.5, h * 0.22)
  ctx.move_to(w * 0.67, h * 0.13)
  ctx.line_to(w * 0.64, h * 0.22)
  ctx.stroke()

  # 5. Detail Rumput Kecil di Kanan Bawah Sumur
  ctx.move_to(w * 0.75, h * 0.8)
  ctx.line_to(w * 0.78, h * 0.72)
  ctx.line_to(w * 0.81, h * 0.8)
  ctx.line_to(w * 0.84, h * 0.72)
  ctx.line_to(w * 0.87, h * 0.8)
  ctx.set_source_rgb(0.2, 0.5, 0.2)
  ctx.fill()

  return cairo_surface_to_pygame(surf)


def generate_bucket_asset(w, h, filled=False):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)
  ctx.move_to(w * 0.2, h * 0.3)
  ctx.line_to(w * 0.8, h * 0.3)
  ctx.line_to(w * 0.7, h * 0.9)
  ctx.line_to(w * 0.3, h * 0.9)
  ctx.close_path()
  ctx.set_source_rgb(0.7, 0.7, 0.75)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.3, 0.3, 0.3)
  ctx.set_line_width(2)
  ctx.stroke()

  if filled:
    ctx.rectangle(w * 0.22, h * 0.32, w * 0.56, h * 0.18)
    ctx.set_source_rgb(0.1, 0.6, 1.0)
    ctx.fill()

  ctx.arc(w * 0.5, h * 0.3, w * 0.3, math.pi, 0)
  ctx.set_source_rgb(0.2, 0.2, 0.2)
  ctx.set_line_width(3)
  ctx.stroke()
  return cairo_surface_to_pygame(surf)


def generate_heart_asset(w, h, active=True):
  surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
  ctx = cairo.Context(surf)
  ctx.move_to(w * 0.5, h * 0.88)
  ctx.curve_to(w * 0.1, h * 0.6, w * 0.05, h * 0.22, w * 0.32, h * 0.22)
  ctx.curve_to(w * 0.44, h * 0.22, w * 0.5, h * 0.33, w * 0.5, h * 0.38)
  ctx.curve_to(w * 0.5, h * 0.33, w * 0.56, h * 0.22, w * 0.68, h * 0.22)
  ctx.curve_to(w * 0.95, h * 0.22, w * 0.9, h * 0.6, w * 0.5, h * 0.88)
  ctx.close_path()

  if active:
    ctx.set_source_rgb(0.92, 0.16, 0.22)
  else:
    ctx.set_source_rgba(0.35, 0.35, 0.38, 0.7)
  ctx.fill_preserve()

  ctx.set_source_rgb(0.15, 0.05, 0.08)
  ctx.set_line_width(1.8)
  ctx.stroke()
  return cairo_surface_to_pygame(surf)


# Generate Aset Pycairo
img_fire = generate_fire_asset(55, 65)
img_smoke = generate_smoke_asset(60, 60)
img_water = generate_water_asset(30, 30)
img_burning_tree = generate_burning_tree_asset(110, 120)
img_well = generate_well_asset(120, 120)
img_bucket_empty = generate_bucket_asset(42, 42, filled=False)
img_bucket_full = generate_bucket_asset(42, 42, filled=True)
img_heart_full = generate_heart_asset(24, 24, active=True)
img_heart_empty = generate_heart_asset(24, 24, active=False)

# --- PENGATURAN DUNIA & KAMERA ---
NUM_MAPS = 5
WORLD_WIDTH = SCREEN_WIDTH * NUM_MAPS
camera_x = 0

# --- PEMUATAN ASET GAMBAR UTAMA ---
try:
  img_menu = pygame.image.load("assets/menu_utama.png").convert()
  img_menu = pygame.transform.scale(img_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

  img_bg = pygame.image.load("assets/background-select-character.png").convert()
  img_bg = pygame.transform.scale(img_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

  img_gameplay_bg = pygame.image.load(
      "assets/background-gameplay.png"
  ).convert()
  img_gameplay_bg = pygame.transform.scale(
      img_gameplay_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )

  # Map Pertama
  img_gameplay_map = pygame.image.load("assets/gameplay.png").convert_alpha()
  img_gameplay_map = pygame.transform.scale(
      img_gameplay_map, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )
  img_gameplay_map = make_dark_bg_transparent(img_gameplay_map, threshold=18)

  # Map Kedua (load PNG & bersihkan latar belakang hitam)
  img_gameplay_map2 = pygame.image.load("assets/gameplay2.png").convert_alpha()
  img_gameplay_map2 = pygame.transform.scale(
      img_gameplay_map2, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )
  img_gameplay_map2 = make_dark_bg_transparent(img_gameplay_map2, threshold=22)

  img_hero1 = pygame.image.load("assets/hero1.png").convert_alpha()
  img_hero2 = pygame.image.load("assets/hero2.png").convert_alpha()

  hero1_frames = [
      pygame.image.load("assets/hero1_gerak1.png").convert_alpha(),
      pygame.image.load("assets/hero1_gerak2.png").convert_alpha(),
  ]
  hero2_frames = [
      pygame.image.load("assets/hero2_gerak1.png").convert_alpha(),
      pygame.image.load("assets/hero2_gerak2.png").convert_alpha(),
  ]

except Exception as e:
  print(f"Error memuat aset gambar: {e}")
  pygame.quit()
  sys.exit()


# --- GAME STATES & DIFFICULTY CONFIG ---
class GameState:
  MENU = 1
  SELECT_HERO = 2
  PLAYING = 3
  WIN = 4
  GAME_OVER = 5


DIFFICULTY_SETTINGS = {
    "Easy": {
        "max_lives": 4,
        "fire_cooldown_ms": 2500,
        "breath_base_drain": 1.2,  # per detik di udara umum
        "breath_smoke_drain": 2.4,  # per detik tambahan di dekat pohon berapi
        "breath_heal_on_extinguish": 8.0,
    },
    "Medium": {
        "max_lives": 3,
        "fire_cooldown_ms": 1800,
        "breath_base_drain": 2.4,
        "breath_smoke_drain": 4.5,
        "breath_heal_on_extinguish": 4.0,
    },
    "Hard": {
        "max_lives": 2,
        "fire_cooldown_ms": 1100,
        "breath_base_drain": 3.8,
        "breath_smoke_drain": 7.0,
        "breath_heal_on_extinguish": 0.0,
    },
}

current_state = GameState.MENU
selected_hero = 1
selected_difficulty = "Medium"

# Variabel Ekonomi, Indikator & Skor Permainan
player_coins = 100
score = 0
inventory = []
has_bucket = False
water_ammo = 0
splash_effects = []

max_lives = DIFFICULTY_SETTINGS[selected_difficulty]["max_lives"]
lives = max_lives
breath = 100.0
game_over_reason = ""
hurt_flash_timer = 0

# --- VARIABEL FISIKA KARAKTER ---
hero_width = 120
hero_height = 120
hero_x = 40
hero_y = 272
hero_vel_y = 0
gravity = 0.6
jump_strength = -12
is_grounded = False

animation_timer = 0
frame_index = 0
facing_right = True

base_plats_map1 = [
    (0, 442, 115, 38),
    (115, 390, 185, 40),
    (300, 320, 210, 42),
    (510, 395, 185, 38),
    (695, 445, 165, 35),
    (860, 355, 100, 38),
]

base_plats_map2 = [
    (0, 332, 145, 40),
    (145, 412, 180, 38),
    (325, 445, 160, 35),
    (485, 395, 180, 38),
    (665, 445, 85, 35),
    (750, 402, 110, 38),
    (860, 342, 100, 40),
]

map_sequence = []
platforms = []


def generate_random_map_sequence(num_maps):
  if num_maps <= 1:
    return [1]
  return [1] + [random.choice([1, 2]) for _ in range(num_maps - 1)]


def build_platforms_from_sequence(seq):
  plats = []
  for seg_idx, map_type in enumerate(seq):
    offset_x = seg_idx * SCREEN_WIDTH
    base_plats = base_plats_map1 if map_type == 1 else base_plats_map2
    for x, y, w, h in base_plats:
      plats.append(pygame.Rect(offset_x + x, y, w, h))
  return plats


# Inisialisasi awal
map_sequence = generate_random_map_sequence(NUM_MAPS)
platforms = build_platforms_from_sequence(map_sequence)

# Objek Ember di awal map
bucket_pickup_rect = pygame.Rect(15, 350, 42, 42)

# SUMUR AGAK KE DEPAN (menapak di platform kedua y=390, sebelum area pohon api)
wells = [pygame.Rect(210, 294, 100, 110)]


# Fungsi untuk mengacak posisi pohon agar selalu menancap pas di atas platform
def generate_random_trees():
  tree_list = []
  candidate_plats = [
      p for p in platforms if p.x >= SCREEN_WIDTH and p.width >= 120
  ]

  if not candidate_plats:
    candidate_plats = platforms[1:]

  num_trees = min(NUM_MAPS + 2, len(candidate_plats))
  chosen_plats = random.sample(candidate_plats, k=num_trees)

  for plat in chosen_plats:
    rx = random.randint(plat.left + 10, max(plat.left + 15, plat.right - 120))
    ry = plat.top - 120
    tree_list.append({
        "rect": pygame.Rect(rx, ry, 110, 120),
        "fire_hp": 2,
        "last_hurt_time": 0,
        "armor_blocked": False,
    })

  return tree_list


burning_trees = generate_random_trees()


def apply_difficulty_and_reset():
  global hero_x, hero_y, hero_vel_y, score, has_bucket, water_ammo
  global burning_trees, splash_effects, map_sequence, platforms
  global max_lives, lives, breath, game_over_reason, hurt_flash_timer

  cfg = DIFFICULTY_SETTINGS[selected_difficulty]
  max_lives = cfg["max_lives"]
  lives = max_lives
  breath = 100.0
  game_over_reason = ""
  hurt_flash_timer = 0

  hero_x = 40
  hero_y = 272
  hero_vel_y = 0
  score = 0
  has_bucket = False
  water_ammo = 0
  splash_effects.clear()

  map_sequence = generate_random_map_sequence(NUM_MAPS)
  platforms = build_platforms_from_sequence(map_sequence)
  burning_trees = generate_random_trees()


def get_spray_area(player_rect):
  """Area siram ketat secara vertikal agar harus lompat / sejajar ketinggian"""
  extra_reach = 45 if "Semprotan Air" in inventory else 0
  reach_x = 85 + extra_reach
  spray_top = player_rect.top - 12
  spray_height = player_rect.height + 10
  if facing_right:
    return pygame.Rect(
        player_rect.centerx - 10, spray_top, reach_x, spray_height
    )
  else:
    return pygame.Rect(
        player_rect.centerx - reach_x + 10, spray_top, reach_x, spray_height
    )


# --- GAME LOOP UTAMA ---
running = True
while running:
  dt = clock.tick(60) / 1000.0
  screen.fill((0, 0, 0))

  # 1. Event Handling
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()

      if current_state == GameState.MENU:
        if 380 <= mouse_pos[0] <= 580 and 300 <= mouse_pos[1] <= 370:
          current_state = GameState.SELECT_HERO
        elif 380 <= mouse_pos[0] <= 580 and 400 <= mouse_pos[1] <= 470:
          running = False

      elif current_state == GameState.SELECT_HERO:
        # Ganti Hero
        if 115 <= mouse_pos[0] <= 155 and 235 <= mouse_pos[1] <= 275:
          selected_hero = 2 if selected_hero == 1 else 1
        elif 315 <= mouse_pos[0] <= 355 and 235 <= mouse_pos[1] <= 275:
          selected_hero = 1 if selected_hero == 2 else 2

        # Pilih Level Kesulitan (Easy / Medium / Hard)
        diff_buttons = [
            ("Easy", pygame.Rect(105, 378, 78, 32)),
            ("Medium", pygame.Rect(191, 378, 78, 32)),
            ("Hard", pygame.Rect(277, 378, 78, 32)),
        ]
        for diff_name, diff_rect in diff_buttons:
          if diff_rect.collidepoint(mouse_pos):
            selected_difficulty = diff_name

        # Mulai Bermain
        if 130 <= mouse_pos[0] <= 350 and 435 <= mouse_pos[1] <= 480:
          apply_difficulty_and_reset()
          current_state = GameState.PLAYING

        # Shop Item
        elif 550 <= mouse_pos[0] <= 850 and 230 <= mouse_pos[1] <= 275:
          if player_coins >= 50 and "Semprotan Air" not in inventory:
            player_coins -= 50
            inventory.append("Semprotan Air")
        elif 550 <= mouse_pos[0] <= 850 and 300 <= mouse_pos[1] <= 345:
          if player_coins >= 100 and "Baju Anti Api" not in inventory:
            player_coins -= 100
            inventory.append("Baju Anti Api")

      elif current_state in (GameState.WIN, GameState.GAME_OVER):
        panel_x = SCREEN_WIDTH // 2 - 260
        panel_y = SCREEN_HEIGHT // 2 - 155
        btn_retry_rect = pygame.Rect(panel_x + 85, panel_y + 215, 150, 45)
        btn_menu_rect = pygame.Rect(panel_x + 285, panel_y + 215, 150, 45)

        if btn_retry_rect.collidepoint(mouse_pos):
          apply_difficulty_and_reset()
          current_state = GameState.PLAYING
        elif btn_menu_rect.collidepoint(mouse_pos):
          apply_difficulty_and_reset()
          current_state = GameState.MENU

    elif event.type == pygame.KEYDOWN:
      if current_state == GameState.PLAYING:
        hitbox_offset_x = 30
        hitbox_w = hero_width - 60
        hitbox_h = hero_height - 15
        player_rect = pygame.Rect(
            hero_x + hitbox_offset_x, hero_y, hitbox_w, hitbox_h
        )

        if event.key == pygame.K_e:
          if has_bucket:
            for well in wells:
              if player_rect.colliderect(well.inflate(60, 30)):
                water_ammo = 5

        elif event.key == pygame.K_f:
          if has_bucket and water_ammo > 0:
            water_ammo -= 1
            dir_mult = 1 if facing_right else -1
            for i in range(4):
              splash_effects.append({
                  "x": hero_x + (hero_width // 2) + (dir_mult * 35),
                  "y": hero_y + 42 + (i * 4),
                  "vx": dir_mult * (7 + i),
                  "vy": -3 - (i * 0.5),
                  "life": 18,
              })

            attack_area = get_spray_area(player_rect)
            cfg = DIFFICULTY_SETTINGS[selected_difficulty]
            for tree in burning_trees:
              if tree["fire_hp"] > 0 and attack_area.colliderect(tree["rect"]):
                tree["fire_hp"] -= 1
                score += 50
                if tree["fire_hp"] == 0:
                  player_coins += 25
                  breath = min(100.0, breath + cfg["breath_heal_on_extinguish"])

  # 2. Update & Render Tampilan Berdasarkan State
  if current_state == GameState.MENU:
    screen.blit(img_menu, (0, 0))

  elif current_state == GameState.SELECT_HERO:
    screen.blit(img_bg, (0, 0))

    font_title = pygame.font.SysFont(None, 36)
    font_sub = pygame.font.SysFont(None, 21)
    font_small = pygame.font.SysFont(None, 18)
    font_btn = pygame.font.SysFont(None, 24)

    char_panel = pygame.Surface((280, 365), pygame.SRCALPHA)
    char_panel.fill((0, 0, 0, 155))
    screen.blit(char_panel, (90, 130))

    title_left = font_title.render("PILIH KARAKTER", True, (255, 255, 255))
    screen.blit(title_left, (128, 142))

    if selected_hero == 1:
      current_preview = pygame.transform.scale(img_hero1, (120, 120))
      name_surf = font_sub.render("Hero 1 (Pemadam)", True, (255, 255, 255))
    else:
      current_preview = pygame.transform.scale(img_hero2, (120, 120))
      name_surf = font_sub.render("Hero 2 (Relawan)", True, (255, 255, 255))

    screen.blit(current_preview, (230 - 60, 190))
    screen.blit(name_surf, (230 - name_surf.get_width() // 2, 318))

    pygame.draw.rect(screen, (70, 70, 70), (115, 235, 40, 40), border_radius=6)
    pygame.draw.rect(
        screen, (200, 200, 200), (115, 235, 40, 40), 2, border_radius=6
    )
    screen.blit(font_btn.render("<", True, (255, 255, 255)), (130, 245))

    pygame.draw.rect(screen, (70, 70, 70), (315, 235, 40, 40), border_radius=6)
    pygame.draw.rect(
        screen, (200, 200, 200), (315, 235, 40, 40), 2, border_radius=6
    )
    screen.blit(font_btn.render(">", True, (255, 255, 255)), (330, 245))

    # Pilihan Tingkat Kesulitan
    lvl_label = font_small.render(
        "Tingkat Kesulitan (Nyawa & Napas):", True, (220, 220, 220)
    )
    screen.blit(lvl_label, (230 - lvl_label.get_width() // 2, 352))

    diff_colors = {
        "Easy": (46, 160, 67),
        "Medium": (210, 140, 30),
        "Hard": (200, 50, 50),
    }
    diff_buttons = [
        ("Easy", pygame.Rect(105, 378, 78, 32)),
        ("Medium", pygame.Rect(191, 378, 78, 32)),
        ("Hard", pygame.Rect(277, 378, 78, 32)),
    ]
    for diff_name, diff_rect in diff_buttons:
      is_sel = selected_difficulty == diff_name
      fill_col = diff_colors[diff_name] if is_sel else (55, 55, 60)
      border_col = (255, 255, 255) if is_sel else (130, 130, 130)
      pygame.draw.rect(screen, fill_col, diff_rect, border_radius=6)
      pygame.draw.rect(screen, border_col, diff_rect, 2, border_radius=6)
      txt = font_small.render(diff_name, True, (255, 255, 255))
      screen.blit(
          txt,
          (
              diff_rect.centerx - txt.get_width() // 2,
              diff_rect.centery - txt.get_height() // 2,
          ),
      )

    pygame.draw.rect(screen, (34, 139, 34), (130, 435, 220, 45), border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), (130, 435, 220, 45), 2, border_radius=8
    )
    start_text = font_btn.render("MULAI BERMAIN", True, (255, 255, 255))
    screen.blit(start_text, (240 - start_text.get_width() // 2, 449))

    # Panel Shop Kanan
    shop_panel = pygame.Surface((360, 365), pygame.SRCALPHA)
    shop_panel.fill((0, 0, 0, 155))
    screen.blit(shop_panel, (520, 130))

    title_right = font_title.render("SHOP ITEM KARHUTLA", True, (255, 255, 255))
    screen.blit(title_right, (555, 142))

    coin_text = font_sub.render(
        f"Koin Anda: {player_coins} Koin", True, (255, 215, 0)
    )
    screen.blit(coin_text, (550, 188))

    item1_bought = "Semprotan Air" in inventory
    btn1_color = (100, 100, 100) if item1_bought else (70, 130, 180)
    pygame.draw.rect(screen, btn1_color, (550, 230, 300, 45), border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), (550, 230, 300, 45), 2, border_radius=8
    )
    item1_label = (
        "Dibeli (Semprotan Air)"
        if item1_bought
        else "Beli Semprotan Air (50 Koin)"
    )
    screen.blit(
        font_sub.render(item1_label, True, (255, 255, 255)), (570, 244)
    )

    item2_bought = "Baju Anti Api" in inventory
    btn2_color = (100, 100, 100) if item2_bought else (70, 130, 180)
    pygame.draw.rect(screen, btn2_color, (550, 300, 300, 45), border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), (550, 300, 300, 45), 2, border_radius=8
    )
    item2_label = (
        "Dibeli (Baju Anti Api)"
        if item2_bought
        else "Beli Baju Anti Api (100 Koin)"
    )
    screen.blit(
        font_sub.render(item2_label, True, (255, 255, 255)), (570, 314)
    )

    cfg_preview = DIFFICULTY_SETTINGS[selected_difficulty]
    info_diff = font_small.render(
        f"Info {selected_difficulty}: {cfg_preview['max_lives']} Nyawa | Napas"
        f" -{cfg_preview['breath_base_drain']}/dtk",
        True,
        (180, 230, 255),
    )
    screen.blit(info_diff, (550, 370))

    inv_text = font_small.render(
        f"Inventory: {', '.join(inventory) if inventory else 'Kosong'}",
        True,
        (200, 200, 200),
    )
    screen.blit(inv_text, (550, 400))

  elif current_state == GameState.PLAYING:
    keys = pygame.key.get_pressed()
    is_moving = False
    dx = 0

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      dx = -5
      is_moving = True
      facing_right = False
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      dx = 5
      is_moving = True
      facing_right = True

    hero_x += dx
    hero_x = max(10, min(WORLD_WIDTH - hero_width - 10, hero_x))

    hitbox_offset_x = 30
    hitbox_w = hero_width - 60
    hitbox_h = hero_height - 15
    player_rect = pygame.Rect(
        hero_x + hitbox_offset_x, hero_y, hitbox_w, hitbox_h
    )

    for plat in platforms:
      if player_rect.colliderect(plat):
        if dx > 0:
          player_rect.right = plat.left
        elif dx < 0:
          player_rect.left = plat.right
        hero_x = player_rect.x - hitbox_offset_x

    if (
        keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]
    ) and is_grounded:
      hero_vel_y = jump_strength
      is_grounded = False

    hero_vel_y += gravity
    hero_y += hero_vel_y
    player_rect.y = int(hero_y)
    is_grounded = False

    for plat in platforms:
      if player_rect.colliderect(plat):
        if hero_vel_y > 0:
          player_rect.bottom = plat.top
          hero_y = player_rect.y
          hero_vel_y = 0
          is_grounded = True
        elif hero_vel_y < 0:
          player_rect.top = plat.bottom
          hero_y = player_rect.y
          hero_vel_y = 0

    if not has_bucket and player_rect.colliderect(bucket_pickup_rect):
      has_bucket = True

    # --- LOGIKA INDIKATOR NYAWA & PERNAFASAN (ISPA) ---
    cfg = DIFFICULTY_SETTINGS[selected_difficulty]
    now_ms = pygame.time.get_ticks()
    if hurt_flash_timer > 0:
      hurt_flash_timer -= 1

    near_active_fire = False
    for tree in burning_trees:
      if tree["fire_hp"] > 0:
        # Area zona asap sekitar pohon berapi
        smoke_zone = tree["rect"].inflate(160, 90)
        if player_rect.colliderect(smoke_zone):
          near_active_fire = True

        # Area tubuh api: melewati/menerobos pohon yang belum padam mengurangi nyawa
        fire_hazard_rect = tree["rect"].inflate(-28, -15)
        if player_rect.colliderect(fire_hazard_rect):
          if now_ms - tree["last_hurt_time"] >= cfg["fire_cooldown_ms"]:
            tree["last_hurt_time"] = now_ms
            if "Baju Anti Api" in inventory and not tree["armor_blocked"]:
              tree["armor_blocked"] = True
            else:
              lives -= 1
              hurt_flash_timer = 15

    # Pengurangan indikator pernafasan akibat asap karhutla
    drain_rate = cfg["breath_base_drain"]
    if near_active_fire:
      drain_rate += cfg["breath_smoke_drain"]
    if "Baju Anti Api" in inventory:
      drain_rate *= 0.85
    breath = max(0.0, breath - drain_rate * dt)

    # Cek Kondisi Kalah atau Menang
    if lives <= 0:
      lives = 0
      game_over_reason = "Nyawa habis akibat menerobos pohon yang masih terbakar!"
      current_state = GameState.GAME_OVER
    elif breath <= 0:
      breath = 0.0
      game_over_reason = "Pernapasan habis (ISPA) akibat terlalu lama menghirup asap!"
      current_state = GameState.GAME_OVER
    elif all(t["fire_hp"] == 0 for t in burning_trees):
      score += int(breath) * 2
      current_state = GameState.WIN

    camera_x = hero_x - (SCREEN_WIDTH // 2) + (hero_width // 2)
    camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))

    if is_moving:
      animation_timer += 1
      if animation_timer > 8:
        frame_index = (frame_index + 1) % 2
        animation_timer = 0
      current_frame = pygame.transform.scale(
          hero1_frames[frame_index]
          if selected_hero == 1
          else hero2_frames[frame_index],
          (hero_width, hero_height),
      )
    else:
      current_frame = pygame.transform.scale(
          img_hero1 if selected_hero == 1 else img_hero2,
          (hero_width, hero_height),
      )

    if not facing_right:
      current_frame = pygame.transform.flip(current_frame, True, False)

    # --- RENDER DUNIA ---
    screen.blit(img_gameplay_bg, (0, 0))

    for seg_idx, map_type in enumerate(map_sequence):
      draw_x = (seg_idx * SCREEN_WIDTH) - camera_x
      if -SCREEN_WIDTH <= draw_x <= SCREEN_WIDTH:
        map_surf = img_gameplay_map if map_type == 1 else img_gameplay_map2
        screen.blit(map_surf, (draw_x, 0))

    font_prompt = pygame.font.SysFont(None, 20)

    # Render Sumur Agak ke Depan (Sebelum Pohon Api)
    for well in wells:
      screen.blit(img_well, (well.x - camera_x, well.y))
      if player_rect.colliderect(well.inflate(60, 30)):
        msg = (
            "Tekan [E] Isi Air"
            if has_bucket
            else "Ambil Ember di Samping Dulu!"
        )
        screen.blit(
            font_prompt.render(msg, True, (255, 255, 0)),
            (well.x - camera_x, well.y - 25),
        )

    # Ember di Awal Map
    if not has_bucket:
      screen.blit(
          img_bucket_empty,
          (bucket_pickup_rect.x - camera_x, bucket_pickup_rect.y),
      )
      screen.blit(
          font_prompt.render("Ember", True, (255, 255, 255)),
          (bucket_pickup_rect.x - camera_x, bucket_pickup_rect.y - 20),
      )

    # Render Pohon Kebakaran
    spray_rect = get_spray_area(player_rect)
    for tree in burning_trees:
      screen.blit(img_burning_tree, (tree["rect"].x - camera_x, tree["rect"].y))
      if tree["fire_hp"] > 0:
        wobble = math.sin(pygame.time.get_ticks() * 0.01) * 4
        screen.blit(
            img_fire,
            (tree["rect"].x - camera_x + 28 + wobble, tree["rect"].y + 10),
        )
        if tree["fire_hp"] == 2:
          screen.blit(
              img_fire,
              (tree["rect"].x - camera_x + 10 - wobble, tree["rect"].y + 30),
          )
        if spray_rect.colliderect(tree["rect"]):
          screen.blit(
              font_prompt.render("Tekan [F] Siram Api!", True, (255, 110, 110)),
              (tree["rect"].x - camera_x, tree["rect"].y - 25),
          )
        elif abs(player_rect.centerx - tree["rect"].centerx) < 110 and (
            player_rect.top > tree["rect"].bottom - 35
        ):
          screen.blit(
              font_prompt.render(
                  "Lompat / Naik untuk Siram!", True, (255, 220, 120)
              ),
              (tree["rect"].x - camera_x - 20, tree["rect"].y - 25),
          )
      else:
        screen.blit(
            img_smoke, (tree["rect"].x - camera_x + 25, tree["rect"].y - 15)
        )

    screen.blit(current_frame, (hero_x - camera_x, hero_y))
    if has_bucket:
      bucket_sprite = img_bucket_full if water_ammo > 0 else img_bucket_empty
      hand_offset_x = 75 if facing_right else 5
      screen.blit(
          bucket_sprite, (hero_x - camera_x + hand_offset_x, hero_y + 55)
      )

    for splash in splash_effects[:]:
      splash["x"] += splash["vx"]
      splash["y"] += splash["vy"]
      splash["vy"] += 0.4
      splash["life"] -= 1
      screen.blit(img_water, (splash["x"] - camera_x, splash["y"]))
      if splash["life"] <= 0:
        splash_effects.remove(splash)

    # Efek kedip merah tipis saat terkena api
    if hurt_flash_timer > 0:
      hurt_overlay = pygame.Surface(
          (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
      )
      hurt_overlay.fill((220, 30, 30, 65))
      screen.blit(hurt_overlay, (0, 0))

    # --- HUD ATAS (2 INDIKATOR + STATUS GAME) ---
    hud_bg = pygame.Surface((SCREEN_WIDTH, 76), pygame.SRCALPHA)
    hud_bg.fill((15, 20, 25, 165))
    screen.blit(hud_bg, (0, 0))

    font_info = pygame.font.SysFont(None, 21)
    font_small = pygame.font.SysFont(None, 19)

    # 1. Indikator Nyawa (Hati)
    screen.blit(font_info.render("Nyawa:", True, (255, 255, 255)), (18, 12))
    for i in range(max_lives):
      heart_img = img_heart_full if i < lives else img_heart_empty
      screen.blit(heart_img, (78 + i * 26, 8))

    # 2. Indikator Pernafasan (Bar ISPA / Asap)
    breath_x = 78 + max_lives * 26 + 22
    screen.blit(
        font_info.render("Pernafasan:", True, (255, 255, 255)), (breath_x, 12)
    )
    bar_x = breath_x + 95
    bar_w = 135
    bar_h = 16
    pygame.draw.rect(screen, (50, 55, 65), (bar_x, 12, bar_w, bar_h), border_radius=4)
    fill_w = int(bar_w * (breath / 100.0))
    if breath > 50:
      bar_col = (60, 200, 120)
    elif breath > 25:
      bar_col = (240, 180, 40)
    else:
      bar_col = (230, 60, 60)
    if fill_w > 0:
      pygame.draw.rect(screen, bar_col, (bar_x, 12, fill_w, bar_h), border_radius=4)
    pygame.draw.rect(
        screen, (220, 220, 220), (bar_x, 12, bar_w, bar_h), 1, border_radius=4
    )
    breath_pct = font_small.render(f"{int(breath)}%", True, (255, 255, 255))
    screen.blit(breath_pct, (bar_x + bar_w + 8, 13))

    # Info Skor, Koin, Ember, & Level di Kanan Atas
    status_ember = (
        "Belum Ada"
        if not has_bucket
        else f"Terisi ({water_ammo}/5)" if water_ammo > 0 else "Kosong"
    )
    right_hud = font_info.render(
        f"[{selected_difficulty}]  Skor: {score}  |  Koin: {player_coins}  |"
        f"  Ember: {status_ember}",
        True,
        (255, 240, 180),
    )
    screen.blit(right_hud, (SCREEN_WIDTH - right_hud.get_width() - 18, 12))

    # Baris Panduan Singkat & Sisa Pohon Api
    remaining_fires = sum(1 for t in burning_trees if t["fire_hp"] > 0)
    hud_guide = font_small.render(
        f"A/D: Jalan | SPASI: Lompat | [E]: Isi Air di Sumur | [F]: Lompat &"
        f" Siram Api  •  Sisa Pohon Api: {remaining_fires}",
        True,
        (215, 220, 225),
    )
    screen.blit(hud_guide, (18, 45))

  elif current_state in (GameState.WIN, GameState.GAME_OVER):
    screen.blit(img_gameplay_bg, (0, 0))
    for seg_idx, map_type in enumerate(map_sequence):
      draw_x = (seg_idx * SCREEN_WIDTH) - camera_x
      if -SCREEN_WIDTH <= draw_x <= SCREEN_WIDTH:
        map_surf = img_gameplay_map if map_type == 1 else img_gameplay_map2
        screen.blit(map_surf, (draw_x, 0))

    is_win = current_state == GameState.WIN
    panel_bg = (20, 50, 30, 195) if is_win else (65, 20, 20, 205)

    end_panel = pygame.Surface((520, 315), pygame.SRCALPHA)
    end_panel.fill(panel_bg)
    pygame.draw.rect(
        end_panel,
        (255, 255, 255, 200),
        end_panel.get_rect(),
        width=2,
        border_radius=12,
    )

    panel_x = SCREEN_WIDTH // 2 - 260
    panel_y = SCREEN_HEIGHT // 2 - 155
    screen.blit(end_panel, (panel_x, panel_y))

    font_end_title = pygame.font.SysFont(None, 44)
    font_end_sub = pygame.font.SysFont(None, 23)
    font_end_reason = pygame.font.SysFont(None, 20)
    font_btn = pygame.font.SysFont(None, 22)

    if is_win:
      title_surf = font_end_title.render("ANDA MENANG!", True, (255, 215, 0))
      sub_reason = font_end_reason.render(
          f"Semua api padam pada tingkat {selected_difficulty} (Sisa Napas:"
          f" {int(breath)}%)",
          True,
          (210, 255, 220),
      )
    else:
      title_surf = font_end_title.render("GAME OVER!", True, (255, 95, 95))
      sub_reason = font_end_reason.render(
          game_over_reason, True, (255, 215, 215)
      )

    screen.blit(
        title_surf,
        (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, panel_y + 28),
    )
    screen.blit(
        sub_reason,
        (SCREEN_WIDTH // 2 - sub_reason.get_width() // 2, panel_y + 78),
    )

    score_surf = font_end_sub.render(
        f"Total Skor Poin: {score}", True, (255, 255, 255)
    )
    screen.blit(
        score_surf,
        (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, panel_y + 118),
    )

    coin_surf = font_end_sub.render(
        f"Total Koin Anda: {player_coins} Koin", True, (255, 230, 100)
    )
    screen.blit(
        coin_surf,
        (SCREEN_WIDTH // 2 - coin_surf.get_width() // 2, panel_y + 152),
    )

    btn_retry_rect = pygame.Rect(panel_x + 85, panel_y + 215, 150, 45)
    pygame.draw.rect(screen, (34, 139, 34), btn_retry_rect, border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), btn_retry_rect, width=2, border_radius=8
    )
    btn_retry_text = font_btn.render("Main Ulang", True, (255, 255, 255))
    screen.blit(
        btn_retry_text,
        (
            btn_retry_rect.centerx - btn_retry_text.get_width() // 2,
            btn_retry_rect.centery - btn_retry_text.get_height() // 2,
        ),
    )

    btn_menu_rect = pygame.Rect(panel_x + 285, panel_y + 215, 150, 45)
    pygame.draw.rect(screen, (180, 50, 50), btn_menu_rect, border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), btn_menu_rect, width=2, border_radius=8
    )
    btn_menu_text = font_btn.render("Menu Utama", True, (255, 255, 255))
    screen.blit(
        btn_menu_text,
        (
            btn_menu_rect.centerx - btn_menu_text.get_width() // 2,
            btn_menu_rect.centery - btn_menu_text.get_height() // 2,
        ),
    )

  pygame.display.flip()

pygame.quit()
sys.exit()
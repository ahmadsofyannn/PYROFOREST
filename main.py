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
  ctx.rectangle(w * 0.1, h * 0.4, w * 0.8, h * 0.55)
  ctx.set_source_rgb(0.5, 0.5, 0.55)
  ctx.fill_preserve()
  ctx.set_source_rgb(0.2, 0.2, 0.2)
  ctx.set_line_width(3)
  ctx.stroke()
  ctx.rectangle(w * 0.2, h * 0.45, w * 0.6, h * 0.2)
  ctx.set_source_rgb(0.05, 0.35, 0.7)
  ctx.fill()
  ctx.move_to(w * 0.15, h * 0.4)
  ctx.line_to(w * 0.15, h * 0.1)
  ctx.move_to(w * 0.85, h * 0.4)
  ctx.line_to(w * 0.85, h * 0.1)
  ctx.set_source_rgb(0.4, 0.25, 0.1)
  ctx.set_line_width(6)
  ctx.stroke()
  ctx.move_to(w * 0.02, h * 0.15)
  ctx.line_to(w * 0.5, h * 0.02)
  ctx.line_to(w * 0.98, h * 0.15)
  ctx.set_source_rgb(0.6, 0.2, 0.1)
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


# Generate Aset Pycairo
img_fire = generate_fire_asset(55, 65)
img_smoke = generate_smoke_asset(60, 60)
img_water = generate_water_asset(30, 30)
img_burning_tree = generate_burning_tree_asset(110, 120)
img_well = generate_well_asset(120, 120)
img_bucket_empty = generate_bucket_asset(42, 42, filled=False)
img_bucket_full = generate_bucket_asset(42, 42, filled=True)

# --- PENGATURAN DUNIA & KAMERA ---
WORLD_WIDTH = 1920
camera_x = 0

# --- PEMUATAN ASET GAMBAR UTAMA ---
try:
  img_menu = pygame.image.load("assets/menu_utama.png").convert()
  img_menu = pygame.transform.scale(img_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

  img_bg = pygame.image.load("assets/background-select-character.png").convert()
  img_bg = pygame.transform.scale(img_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

  img_gameplay_bg = pygame.image.load("assets/background-gameplay.png").convert()
  img_gameplay_bg = pygame.transform.scale(
      img_gameplay_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )

  img_gameplay_map = pygame.image.load("assets/gameplay.png").convert()
  img_gameplay_map = pygame.transform.scale(
      img_gameplay_map, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )
  img_gameplay_map.set_colorkey(img_gameplay_map.get_at((0, 0)))

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


# --- GAME STATES ---
class GameState:
  MENU = 1
  SELECT_HERO = 2
  PLAYING = 3
  WIN = 4


current_state = GameState.MENU
selected_hero = 1

# Variabel Ekonomi & Skor Permainan
player_coins = 100
score = 0
inventory = []
has_bucket = False
water_ammo = 0
splash_effects = []

# --- VARIABEL FISIKA KARAKTER ---
hero_width = 120
hero_height = 120
hero_x = 80
hero_y = 325
hero_vel_y = 0
gravity = 0.6
jump_strength = -12
is_grounded = False

animation_timer = 0
frame_index = 0
facing_right = True

# Pijakan Platform Tanah
platforms = [
    pygame.Rect(0, 445, 960, 95),
    pygame.Rect(130, 385, 165, 60),
    pygame.Rect(295, 325, 225, 120),
    pygame.Rect(520, 385, 185, 60),
    pygame.Rect(855, 360, 105, 85),
    pygame.Rect(960, 445, 960, 95),
    pygame.Rect(960 + 130, 385, 165, 60),
    pygame.Rect(960 + 295, 325, 225, 120),
    pygame.Rect(960 + 520, 385, 185, 60),
    pygame.Rect(960 + 855, 360, 105, 85),
]

# Objek Ember di awal map (dekat sumur)
bucket_pickup_rect = pygame.Rect(20, 400, 42, 42)

# SUMUR DIPINDAH KE AWAL MAP (Dekat posisi awal pemain)
wells = [pygame.Rect(80, 325, 110, 120)]


# Fungsi untuk mengacak posisi 5 pohon secara random di atas platform yang valid
def generate_random_trees():
  tree_list = []
  valid_x_ranges = [(300, 500), (600, 800), (1050, 1250), (1350, 1550), (1650, 1820)]

  for x_min, x_max in valid_x_ranges:
    rx = random.randint(x_min, x_max)
    ry = 265 if (rx % 2 == 0) else 205
    tree_list.append({"rect": pygame.Rect(rx, ry, 110, 120), "fire_hp": 2})
  return tree_list


burning_trees = generate_random_trees()


def reset_game():
  global hero_x, hero_y, hero_vel_y, score, has_bucket, water_ammo, burning_trees, splash_effects
  hero_x = 80
  hero_y = 325
  hero_vel_y = 0
  score = 0
  has_bucket = False
  water_ammo = 0
  splash_effects.clear()
  burning_trees = generate_random_trees()


# --- GAME LOOP UTAMA ---
running = True
while running:
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
        if 115 <= mouse_pos[0] <= 155 and 250 <= mouse_pos[1] <= 290:
          selected_hero = 2 if selected_hero == 1 else 1
        elif 315 <= mouse_pos[0] <= 355 and 250 <= mouse_pos[1] <= 290:
          selected_hero = 1 if selected_hero == 2 else 2
        elif 130 <= mouse_pos[0] <= 350 and 440 <= mouse_pos[1] <= 485:
          current_state = GameState.PLAYING

        elif 570 <= mouse_pos[0] <= 850 and 240 <= mouse_pos[1] <= 290:
          if player_coins >= 50 and "Semprotan Air" not in inventory:
            player_coins -= 50
            inventory.append("Semprotan Air")
        elif 570 <= mouse_pos[0] <= 850 and 340 <= mouse_pos[1] <= 390:
          if player_coins >= 100 and "Baju Anti Api" not in inventory:
            player_coins -= 100
            inventory.append("Baju Anti Api")

      elif current_state == GameState.WIN:
        if 330 <= mouse_pos[0] <= 470 and 340 <= mouse_pos[1] <= 390:
          reset_game()
          current_state = GameState.PLAYING
        elif 490 <= mouse_pos[0] <= 630 and 340 <= mouse_pos[1] <= 390:
          reset_game()
          current_state = GameState.MENU

    elif event.type == pygame.KEYDOWN:
      if current_state == GameState.PLAYING:
        player_rect = pygame.Rect(hero_x, hero_y, hero_width, hero_height)

        if event.key == pygame.K_e:
          if not has_bucket:
            print("Ambil ember terlebih dahulu di dekat sumur!")
          else:
            for well in wells:
              if player_rect.colliderect(well.inflate(60, 30)):
                water_ammo = 5
                print("Ember terisi air penuh! (5x Siram)")

        elif event.key == pygame.K_f:
          if not has_bucket:
            print("Kamu belum membawa ember!")
          elif water_ammo <= 0:
            print("Ember kosong! Ambil air di sumur dan tekan [E].")
          else:
            water_ammo -= 1
            dir_mult = 1 if facing_right else -1
            for i in range(4):
              splash_effects.append({
                  "x": hero_x + (hero_width // 2) + (dir_mult * 40),
                  "y": hero_y + 50 + (i * 5),
                  "vx": dir_mult * (6 + i),
                  "vy": -2 - i,
                  "life": 20,
              })

            attack_area = player_rect.inflate(100, 40)
            for tree in burning_trees:
              if tree["fire_hp"] > 0 and attack_area.colliderect(tree["rect"]):
                tree["fire_hp"] -= 1
                score += 50
                if tree["fire_hp"] == 0:
                  player_coins += 25
                  print("Pohon dipadamkan! +50 Poin | Konversi +25 Koin")

  # 2. Update & Render Tampilan Berdasarkan State
  if current_state == GameState.MENU:
    screen.blit(img_menu, (0, 0))

  elif current_state == GameState.SELECT_HERO:
    screen.blit(img_bg, (0, 0))

    font_title = pygame.font.SysFont(None, 38)
    font_sub = pygame.font.SysFont(None, 22)
    font_btn = pygame.font.SysFont(None, 24)

    char_panel = pygame.Surface((280, 360), pygame.SRCALPHA)
    char_panel.fill((0, 0, 0, 150))
    screen.blit(char_panel, (90, 130))

    title_left = font_title.render("PILIH KARAKTER", True, (255, 255, 255))
    screen.blit(title_left, (125, 145))

    if selected_hero == 1:
      current_preview = pygame.transform.scale(img_hero1, (130, 130))
      name_surf = font_sub.render(
          "Karakter: Hero 1 (Pemadam)", True, (255, 255, 255)
      )
    else:
      current_preview = pygame.transform.scale(img_hero2, (130, 130))
      name_surf = font_sub.render(
          "Karakter: Hero 2 (Relawan)", True, (255, 255, 255)
      )

    screen.blit(current_preview, (SCREEN_WIDTH // 4 - 65, 205))
    screen.blit(name_surf, (230 - name_surf.get_width() // 2, 350))

    pygame.draw.rect(screen, (70, 70, 70), (115, 250, 40, 40), border_radius=6)
    pygame.draw.rect(
        screen, (200, 200, 200), (115, 250, 40, 40), 2, border_radius=6
    )
    screen.blit(font_btn.render("<", True, (255, 255, 255)), (130, 260))

    pygame.draw.rect(screen, (70, 70, 70), (315, 250, 40, 40), border_radius=6)
    pygame.draw.rect(
        screen, (200, 200, 200), (315, 250, 40, 40), 2, border_radius=6
    )
    screen.blit(font_btn.render(">", True, (255, 255, 255)), (330, 260))

    pygame.draw.rect(screen, (34, 139, 34), (130, 440, 220, 40), border_radius=8)
    pygame.draw.rect(
        screen, (255, 255, 255), (130, 440, 220, 40), 2, border_radius=8
    )
    start_text = font_btn.render("MULAI BERMAIN", True, (255, 255, 255))
    screen.blit(start_text, (240 - start_text.get_width() // 2, 451))

    shop_panel = pygame.Surface((360, 360), pygame.SRCALPHA)
    shop_panel.fill((0, 0, 0, 150))
    screen.blit(shop_panel, (520, 130))

    title_right = font_title.render("SHOP ITEM KARHUTLA", True, (255, 255, 255))
    screen.blit(title_right, (555, 145))

    coin_text = font_sub.render(
        f"Koin Anda: {player_coins} 🪙", True, (255, 215, 0)
    )
    screen.blit(coin_text, (550, 190))

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
        font_sub.render(item1_label, True, (255, 255, 255)), (570, 243)
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
        font_sub.render(item2_label, True, (255, 255, 255)), (570, 313)
    )

    inv_text = font_sub.render(
        f"Inventory: {', '.join(inventory) if inventory else 'Kosong'}",
        True,
        (200, 200, 200),
    )
    screen.blit(inv_text, (550, 380))

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

    if all(t["fire_hp"] == 0 for t in burning_trees):
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
    screen.blit(img_gameplay_map, (0 - camera_x, 0))
    screen.blit(img_gameplay_map, (960 - camera_x, 0))

    font_prompt = pygame.font.SysFont(None, 20)

    # Render Sumur di Awal Map
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

    # Render Pohon Kebakaran (Posisi Random)
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
        if player_rect.colliderect(tree["rect"].inflate(100, 40)):
          screen.blit(
              font_prompt.render("Tekan [F] Siram Api!", True, (255, 100, 100)),
              (tree["rect"].x - camera_x, tree["rect"].y - 25),
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

    font_info = pygame.font.SysFont(None, 22)
    status_ember = (
        "Belum Ada"
        if not has_bucket
        else f"Terisi ({water_ammo}/5)" if water_ammo > 0 else "Kosong"
    )
    hud_top = font_info.render(
        f"Skor Poin: {score} ⭐  |  Koin: {player_coins} 🪙  |  Ember:"
        f" {status_ember}",
        True,
        (255, 255, 255),
    )
    screen.blit(hud_top, (20, 15))

    hud_guide = font_info.render(
        "A/D: Jalan | SPASI: Lompat | [E]: Isi Air di Sumur (Awal) | [F]: Siram"
        " 5 Pohon Api",
        True,
        (220, 220, 220),
    )
    screen.blit(hud_guide, (20, 40))

  elif current_state == GameState.WIN:
    screen.blit(img_gameplay_bg, (0, 0))
    screen.blit(img_gameplay_map, (0 - camera_x, 0))
    screen.blit(img_gameplay_map, (960 - camera_x, 0))

    win_panel = pygame.Surface((520, 310), pygame.SRCALPHA)
    win_panel.fill((20, 50, 30, 180))
    pygame.draw.rect(
        win_panel,
        (255, 255, 255, 200),
        win_panel.get_rect(),
        width=2,
        border_radius=12,
    )

    panel_x = SCREEN_WIDTH // 2 - 260
    panel_y = SCREEN_HEIGHT // 2 - 155
    screen.blit(win_panel, (panel_x, panel_y))

    font_win_title = pygame.font.SysFont(None, 46)
    font_win_sub = pygame.font.SysFont(None, 24)
    font_btn = pygame.font.SysFont(None, 22)

    title_surf = font_win_title.render("ANDA MENANG!", True, (255, 215, 0))
    screen.blit(
        title_surf,
        (SCREEN_WIDTH // 2 - title_surf.get_width() // 2, panel_y + 30),
    )

    score_surf = font_win_sub.render(
        f"Total Skor Poin: {score} ⭐", True, (255, 255, 255)
    )
    screen.blit(
        score_surf,
        (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, panel_y + 90),
    )

    coin_earned = score // 2
    coin_surf = font_win_sub.render(
        f"Koin Diperoleh untuk Shop: +{coin_earned} 🪙", True, (255, 230, 100)
    )
    screen.blit(
        coin_surf,
        (SCREEN_WIDTH // 2 - coin_surf.get_width() // 2, panel_y + 125),
    )

    btn_retry_rect = pygame.Rect(panel_x + 85, panel_y + 210, 150, 45)
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

    btn_menu_rect = pygame.Rect(panel_x + 285, panel_y + 210, 150, 45)
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
  clock.tick(60)

pygame.quit()
sys.exit()
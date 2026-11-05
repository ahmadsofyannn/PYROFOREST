import pygame
import sys 

# Inisialisasi Pygame
pygame.init()

# Pengaturan Resolusi Layar Game
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyroForest - Edukasi Bencana KARHUTLA")

clock = pygame.time.Clock()

# --- PEMUATAN ASET GAMBAR ---
try:
  # Menu Utama
  img_menu = pygame.image.load("assets/menu_utama.png").convert()
  img_menu = pygame.transform.scale(img_menu, (SCREEN_WIDTH, SCREEN_HEIGHT))

  # Background untuk Pemilihan Karakter
  img_bg = pygame.image.load("assets/background.png").convert()
  img_bg = pygame.transform.scale(img_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

  # =========================================================================
  # TODO: REVISI SEMENTARA BACKGROUND GAMEPLAY
  # Untuk sementara kita pakai 'background.png'.
  # Nanti kalau desain background gameplay barunya sudah ada,
  # kamu tinggal ganti nama file 'assets/background.png' di bawah ini
  # menjadi nama file background gameplay yang baru (misal: 'assets/bg_gameplay.png').
  # =========================================================================
  img_gameplay_bg = pygame.image.load("assets/background.png").convert()
  img_gameplay_bg = pygame.transform.scale(
      img_gameplay_bg, (SCREEN_WIDTH, SCREEN_HEIGHT)
  )

  # Karakter Diam / Pilih
  img_hero1 = pygame.image.load("assets/hero1.png").convert_alpha()
  img_hero2 = pygame.image.load("assets/hero2.png").convert_alpha()

  # Animasi Gerak Hero 1 & Hero 2
  hero1_frames = [
      pygame.image.load("assets/hero1_gerak1.png").convert_alpha(),
      pygame.image.load("assets/hero1_gerak2.png").convert_alpha(),
  ]
  hero2_frames = [
      pygame.image.load("assets/hero2_gerak1.png").convert_alpha(),
      pygame.image.load("assets/hero2_gerak2.png").convert_alpha(),
  ]
except Exception (FileNotFoundError, pygame.error) as e:
  print(f"Error memuat aset gambar: {e}")
  print("Pastikan semua nama file di dalam folder 'assets/' sudah benar!")
  pygame.quit()
  sys.exit()


# --- GAME STATES (STATUS PERMAINAN) ---
class GameState:
  MENU = 1
  SELECT_HERO = 2
  PLAYING = 3


current_state = GameState.MENU
selected_hero = 1  # Pilihan default Hero 1

# Variabel Posisi & Animasi Karakter di Gameplay
hero_x = 100
hero_y = 350
animation_timer = 0
frame_index = 0
facing_right = True  # Status arah hadap karakter (True = Kanan, False = Kiri)

# --- GAME LOOP UTAMA ---
running = True
while running:
  screen.fill((0, 0, 0))

  # 1. Event Handling (Input Mouse & Keyboard)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()

      # Logika Klik di Menu Utama
      if current_state == GameState.MENU:
        # Tombol Play (Perkiraan area tombol di gambar menu)
        if 380 <= mouse_pos[0] <= 580 and 300 <= mouse_pos[1] <= 370:
          current_state = GameState.SELECT_HERO
        # Tombol Exit
        elif 380 <= mouse_pos[0] <= 580 and 400 <= mouse_pos[1] <= 470:
          running = False

      # Logika Klik di Pemilihan Karakter
      elif current_state == GameState.SELECT_HERO:
        # Pilih Hero 1 (kotak kiri)
        if 230 <= mouse_pos[0] <= 430 and 180 <= mouse_pos[1] <= 380:
          selected_hero = 1
          current_state = GameState.PLAYING
        # Pilih Hero 2 (kotak kanan)
        elif 530 <= mouse_pos[0] <= 730 and 180 <= mouse_pos[1] <= 380:
          selected_hero = 2
          current_state = GameState.PLAYING

  # 2. Update & Render Tampilan Berdasarkan State
  if current_state == GameState.MENU:
    # Tampilkan Menu Utama
    screen.blit(img_menu, (0, 0))

  elif current_state == GameState.SELECT_HERO:
    # Tampilkan Background Hutan untuk Pemilihan Karakter
    screen.blit(img_bg, (0, 0))

    font_title = pygame.font.SysFont(None, 42)
    font_sub = pygame.font.SysFont(None, 24)

    title_surf = font_title.render("PILIH KARAKTERMU", True, (255, 255, 255))
    screen.blit(title_surf, (SCREEN_WIDTH // 2 - 140, 80))

    # Gambar kotak preview Hero 1 & Hero 2
    hero1_preview = pygame.transform.scale(img_hero1, (140, 140))
    hero2_preview = pygame.transform.scale(img_hero2, (140, 140))
    screen.blit(hero1_preview, (260, 200))
    screen.blit(hero2_preview, (560, 200))

    label_h1 = font_sub.render("Klik untuk Pilih Hero 1", True, (255, 255, 255))
    label_h2 = font_sub.render("Klik untuk Pilih Hero 2", True, (255, 255, 255))
    screen.blit(label_h1, (245, 360))
    screen.blit(label_h2, (545, 360))

  elif current_state == GameState.PLAYING:
    # =========================================================================
    # TODO: RENDER BACKGROUND GAMEPLAY
    # Saat ini merender variabel img_gameplay_bg. Nanti kalau file gambarnya
    # sudah diganti di atas, otomatis akan tampil di sini.
    # =========================================================================
    screen.blit(img_gameplay_bg, (0, 0))

    # Kontrol Karakter Menggunakan Keyboard (A/D atau Panah Kiri/Kanan)
    keys = pygame.key.get_pressed()
    is_moving = False

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
      hero_x -= 4
      is_moving = True
      facing_right = False  # Ubah arah hadap ke kiri
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
      hero_x += 4
      is_moving = True
      facing_right = True  # Ubah arah hadap ke kanan

    # Batasi pergerakan karakter agar tidak keluar layar
    hero_x = max(50, min(SCREEN_WIDTH - 130, hero_x))

    # Logika Pergantian Frame Animasi Gerak
    if is_moving:
      animation_timer += 1
      if animation_timer > 8:  # Kecepatan ganti frame animasi
        frame_index = (frame_index + 1) % 2
        animation_timer = 0

      # Ambil frame gerak sesuai karakter yang dipilih
      if selected_hero == 1:
        current_frame = pygame.transform.scale(
            hero1_frames[frame_index], (90, 90)
        )
      else:
        current_frame = pygame.transform.scale(
            hero2_frames[frame_index], (90, 90)
        )
    else:
      # Tampilkan posisi diam (idle) jika tidak bergerak
      if selected_hero == 1:
        current_frame = pygame.transform.scale(img_hero1, (90, 90))
      else:
        current_frame = pygame.transform.scale(img_hero2, (90, 90))

    # Balik gambar secara horizontal jika karakter menghadap ke kiri
    if not facing_right:
      current_frame = pygame.transform.flip(current_frame, True, False)

    # Gambar karakter di layar
    screen.blit(current_frame, (hero_x, hero_y))

    # Informasi panduan di gameplay
    font_info = pygame.font.SysFont(None, 22)
    info_text = font_info.render(
        "Gunakan Tombol A/D atau Panah untuk Bergerak", True, (255, 255, 255)
    )
    screen.blit(info_text, (20, 20))

  pygame.display.flip()
  clock.tick(60)

pygame.quit()
sys.exit()
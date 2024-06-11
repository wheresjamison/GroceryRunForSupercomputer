from mpi4py import MPI
import pygame
import sys
import os
import random
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Initialize pygame
pygame.init()

# Screen dimensions
width, height = 1920, 1080  # Set screen resolution to 1920x1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"Node {rank} Display")

# Path to assets
assets_path = "assets"

# Function to load and scale an image
def load_and_scale_image(image_path):
    image = pygame.image.load(image_path)
    return pygame.transform.scale(image, (width, height))

# Function to handle common pygame events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# New Node 1: Toggle between two images every 5 minutes
if rank == 0:
    image1 = os.path.join(assets_path, "gr3.png")
    image2 = os.path.join(assets_path, "gr4.png")
    images = [image1, image2]

    # Ensure both images exist
    for img in images:
        if not os.path.exists(img):
            print(f"Image {img} not found!")
            sys.exit()

    current_image_index = 0
    next_update = time.time() + 300

    while True:
        handle_events()

        screen.fill((0, 0, 0))
        screen.blit(load_and_scale_image(images[current_image_index]), (0, 0))
        pygame.display.flip()

        if time.time() >= next_update:
            current_image_index = 1 - current_image_index
            next_update = time.time() + 300

        time.sleep(1)

# New Node 2: Random images every minute
elif rank == 1:
    image_files = [f"customer{i}.png" for i in range(1, 11)]
    images = [os.path.join(assets_path, img) for img in image_files]

    # Ensure all images exist
    for img in images:
        if not os.path.exists(img):
            print(f"Image {img} not found!")
            sys.exit()

    current_image = random.choice(images)
    next_update = time.time() + 60

    while True:
        handle_events()

        screen.fill((0, 0, 0))
        screen.blit(load_and_scale_image(current_image), (0, 0))
        pygame.display.flip()

        if time.time() >= next_update:
            current_image = random.choice(images)
            next_update = time.time() + 60

        time.sleep(1)

# Node 3: Display sequence of images every 12 seconds
elif rank == 3:
    image_files = ["Accepted.png", "OTW1.png", "Shopping.png", "OTW2.png", "Delivered.png"]
    images = [os.path.join(assets_path, img) for img in image_files]

    # Ensure all images exist
    for img in images:
        if not os.path.exists(img):
            print(f"Image {img} not found!")
            sys.exit()

    current_image_index = 0
    next_update = time.time() + 12

    while True:
        handle_events()

        screen.fill((0, 0, 0))
        screen.blit(load_and_scale_image(images[current_image_index]), (0, 0))
        pygame.display.flip()

        if time.time() >= next_update:
            current_image_index = (current_image_index + 1) % len(images)
            next_update = time.time() + 12

        time.sleep(1)

# Node 4: Blank
#elif rank == 2:
   # while True:
   #     handle_events()
  #      screen.fill((0, 0, 0))
 #       pygame.display.flip()
#        time.sleep(1)
#this is for the game to run on webgl node 4.
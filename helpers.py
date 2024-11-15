def create_top_rock():
    rock_width = random.randint(50, 150) # Generates a random width between 50 and 150
    rock_height = random.randint(100, max_height) # Generates a random height between 100 and the max height given (260)
    rock_grass_scaled = pygame.transform.scale(down_rock_grass, (rock_width, rock_height)) # Scale the rock to the height and width; which are random
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = 0  # Stays at the top of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def create_bottom_rock():
    rock_width = random.randint(50, 150) # Generates a random width between 50 and 150
    rock_height = random.randint(100, max_height) # Generates a random height between 100 and the max height given (260)
    rock_grass_scaled = pygame.transform.scale(rock_grass, (rock_width, rock_height)) # Scale the rock to the height and width; which are random
    rock_x = WIDTH + random.randint(0, 200)  # Start off-screen to the right
    rock_y = HEIGHT - rock_height  # Stays at the bottom of the screen
    return (rock_grass_scaled, rock_x, rock_y)

def rocks_overlap(new_rock, existing_rocks): # Checking if any new rocks over lap with existing rocks
    new_image, new_x, new_y = new_rock # new_image = the new rock image, new_x = starting x coordinate of the rectangle (new rock), new_y = starting y coordinate of the rectangle (new rock)
    new_rect = pygame.Rect(new_x, new_y, new_image.get_width(), new_image.get_height()) # gives x and y position, width and height of the image 

    for rock in existing_rocks: # For loop goes over every rock that is already exisiting
        existing_image, existing_x, existing_y = rock # x and y position of the existing rock and the image. 
        existing_rect = pygame.Rect(existing_x, existing_y, existing_image.get_width(), existing_image.get_height()) # Creating a Rect for the existing rock, which gives the x and y position and width and height of the image
        
        if new_rect.colliderect(existing_rect): # Checking to see if a new rock overlaps with an exisiting rock
            # colliderect: test if two rectangle overlap 
            return True  # return true if there is an overlap
    return False  # return false if there is no overlap

def try_create_bottom_rock(existing_rocks): # Creates a new bottom rock, and makes sure that the new rock does not overlap an existing rock
    while True: # We need a while loop because we need to find a rock that does not overlap another rock, so it will continue until it is found.
        new_rock = create_bottom_rock() # Calls the function and assigns it to new_rock (which includes x and y position)
        if not rocks_overlap(new_rock, existing_rocks): # This checks if any new rocks over lap with any existing rocks 
            # if there is no overlap, then it will return false, and then it will then turn it true, returning a new rock
            return new_rock  # Return the new rock if no overlap

def try_create_top_rock(existing_rocks): # Creates a new top rock, and makes sure that the new rock does not overlap an exisiting rock
    while True: # We need a while loop because we want it to continue to try and place a rock until there is no overlap with another rock
        new_rock = create_top_rock() # Calls the function and assigns it to new rock (this function includes an x and y poisiton and height and width of the rock)
        if not rocks_overlap(new_rock, existing_rocks): # This checks to make sure that no new rock that is being added overlaps with an already existing rock
            # if there is no overlap, then it will return false, and the NOT will then turn it true, returning a new rock 
            return new_rock # If no overlap it will execute the if statement and return a new rock

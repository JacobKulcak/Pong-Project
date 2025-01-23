
# START SCREEN
def start_screen():
    running = True
    black_surface = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    black_surface.fill((0,0,0))
    black_surface.set_alpha(230)
    
    title_surface = title_font.render(("Ultimate BONG"), True, (20,200,50))
    title_rect = title_surface.get_rect(center = (SCREEN_WIDTH/2, 100))
    
    button_color = (70,130,180)
    start_button = pygame.Rect(400,300,200,100)
    start_text = normal_font.render("START", True, (255,255,255))
    start_text_rect = start_text.get_rect(center = start_button.center)
    start_button_surface = pygame.Surface((start_button.width, start_button.height))
    
    exit_button = pygame.Rect(SCREEN_WIDTH-600,SCREEN_HEIGHT-300,200,100)
    exit_text = normal_font.render("EXIT", True, (255,255,255))
    exit_text_rect = exit_text.get_rect(center = exit_button.center)
    
    while running:
        
        pygame.Surface.fill(screen,(0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            
            if start_button.collidepoint(pygame.mouse.get_pos()):  # Check if click is inside button
                start_button_surface.set_alpha(255)
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                    running = False
                    return "game"
            else:
                start_button_surface.set_alpha(128)
            
            if exit_button.collidepoint(pygame.mouse.get_pos()):  # Check if click is inside button
                if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                    running = False
                    return "exit"
        
        screen.blit(bob, (0,0))
        screen.blit(black_surface, (0,0))
        screen.blit(title_surface, title_rect)
        screen.blit(start_button_surface, (400,300))
        
        pygame.draw.rect(screen, button_color, start_button)
        screen.blit(start_text, start_text_rect)
        
        pygame.draw.rect(screen, button_color, exit_button)
        screen.blit(exit_text, exit_text_rect)
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            running = False
            return "game"
            
        pygame.display.update()

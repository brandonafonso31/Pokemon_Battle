# Une class en plus pour pokemon_team ?
import sprite,json,utils,os,pygame,sys
from config import battle_json_path,res_screen_top,sprite_trainers_dir_path,song_dir_path,pokeball_dir_path
from copy import deepcopy

class Pokemon_trainer:
    def __init__(self, name: str, theme_path = os.path.join(song_dir_path,"battle","trainer_BW.mp3"), pokeball = "pokeball"):
        self.name = name
        self.pokemon_team = []
        self.pc = []
        self.sprite_path = os.path.join(sprite_trainers_dir_path,f"{(self.name).upper()}.png")
        self.sprite_coord = -1,-1
        self.theme = theme_path
        self.pokeball = pokeball
        
    def __str__(self):
        string  = f"Dresseur: {self.name}\nPokémon:"
        if len(self.pokemon_team)>0:
            string += f"\n{self.pokemon_team[0]}"
        if len(self.pokemon_team)>1:
            string +=f"\n{self.pokemon_team[1]}"
        if len(self.pokemon_team)>2:
            string += f"\n{self.pokemon_team[2]}"
        if len(self.pokemon_team)>3:
            string += f"\n{self.pokemon_team[3]}"
        if len(self.pokemon_team)>4:
            string += f"\n{self.pokemon_team[4]}"
        if len(self.pokemon_team)>5:
            string += f"\n{self.pokemon_team[5]}"
        return string
    
    def catch_pokemon(self, pokemon, nickname=None):
        nb_pokemon = len(self.pokemon_team)
        pokemon.id = nb_pokemon
        if nb_pokemon >= 6:
            print(f"{self.name} a déjà 6 Pokémon dans son équipe.")
            self.pc.append(pokemon)
            print(f"{pokemon.name} a été envoyé dans la boîte PC.")
        else:
            pokemon.trainer = self
            pokemon.nickname = nickname if nickname is not None else pokemon.name
            pokemon.id = len(self.pokemon_team) + 1
            self.pokemon_team.append(pokemon)
            print(f"{self.name} a capturé {pokemon.name}")
            
    def send_next(self,window,front_or_back: str,reset = False):
        "for now only send the next in list, no choice"
        with open(battle_json_path, "r") as f:
            data = json.load(f)
        team = self.pokemon_team
        for i in range(len(team)):
            pokemon = team[i]
            if pokemon.hp != 0:
                text = f"{self.name} envoie {pokemon.name} !"
                utils.print_log_ingame(window,text,reset)
                dic = data["current"]
                dic = {"current": [dic[0],i+1]} if front_or_back == "front" else {"current": [i+1,dic[1]]}
                utils.update_battle_json(dic)
                
                if front_or_back == "front":
                    poke_x = data["opponent"][str(i+1)]["x"]
                    poke_y = data["opponent"][str(i+1)]["y"]
                    poke_w = utils.get_width_pokemon_sprite(front_or_back)
                    
                    # largeur d'une frame de pokéball
                    ball_w = utils.get_width_pokeball_sprite()
                    pos = (
                        poke_x + poke_w // 2 - ball_w // 2,
                        poke_y
                    )

                    self.send_pokeball(window, pos)
                    utils.check_hp_to_change_music(pokemon)
                    
                pokemon.play_howl()
                return pokemon
        return None
    
    def set_team_into_json(self,trainer_or_opponent: str):
        pokemon_team = {}
        for i in range(len(self.pokemon_team)):
            pokemon = self.pokemon_team[i]
            if trainer_or_opponent == "trainer":
                data = sprite.create_pokemon_trainer(res_screen_top, pokemon, f"pokemon_back_{i+1}.png")
            else:
                data = sprite.create_pokemon_opponent(res_screen_top, pokemon, f"pokemon_front_{i+1}.png")
            pokemon_team[str(i+1)] = data      
        
        utils.update_battle_json({trainer_or_opponent: pokemon_team})  
        
    def get_opponent_sprite(self):
        sprite_path = self.sprite_path
        if not os.path.exists(sprite_path):
            return 0,0
        
        sprite_trainer = pygame.image.load(sprite_path).convert()
        sprite_trainer.set_colorkey(sprite.get_first_pixel(sprite_path))
        
        if self.sprite_coord == (-1,-1) :
            base_offset = sprite.get_base_pixel(sprite_path) - sprite_trainer.get_height()
            x_trainer = (res_screen_top[0] + sprite_trainer.get_width())//2 + 30
            y_trainer = res_screen_top[1]//2 - base_offset - 150
            self.sprite_coord = x_trainer,y_trainer
            
        return sprite_trainer

    def move_to_right(self,window):
        sprite_trainer = self.get_opponent_sprite()
        x,y = self.sprite_coord
        with open(battle_json_path, "r") as f:
            data = json.load(f)        
        bg = pygame.image.load(data["background"]).convert()
        clock = pygame.time.Clock()
        dt = 0
        limit_x = res_screen_top[0]
        while x < limit_x:
            dt = clock.tick(30) / 1000
            rect = pygame.Rect(x,y,sprite_trainer.get_width(),sprite_trainer.get_height())
            window.blit(bg,rect,rect)
            x += 200 * dt
            window.blit(sprite_trainer,(x,y))          
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.flip()
            
    def send_pokeball(self,window, pos):
        pokeball_name = self.pokeball
        
        x,y = pos
        path = os.path.join(pokeball_dir_path,f"ball_{pokeball_name.upper()}.png")
        pokeball_sprite = pygame.image.load(path).convert()
        pokeball_sprite.set_colorkey(sprite.get_first_pixel(path))
        
        path_open = os.path.join(pokeball_dir_path,f"ball_{pokeball_name.upper()}_open.png")
        pokeball_sprite_open = pygame.image.load(path_open).convert()
        pokeball_sprite_open.set_colorkey(sprite.get_first_pixel(path_open))
        
        with open(battle_json_path, "r") as f:
            data = json.load(f)        
        bg = pygame.image.load(data["background"]).convert()
        
        width = pokeball_sprite.get_width()
        height = pokeball_sprite.get_height()
        
        clock = pygame.time.Clock()
        nb_frames = 8
        width_per_frame = width // nb_frames
        elapsed = 0
        x_frame = 0
        rect_bg = pygame.Rect(x, y, width_per_frame, height)
        loop = 0
        
        while loop <= 3:
            dt = clock.tick(30) / 1000
            elapsed += dt
            
            if elapsed >= 0.05:
                rect = pygame.Rect(x_frame, 0, width_per_frame, height)
                window.blit(bg,pos,rect_bg)
                window.blit(pokeball_sprite, pos, rect) 
                x_frame += width_per_frame
                elapsed = 0
                
                if x_frame >= width :
                    loop += 1
                    x_frame = 0             
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.flip() 
        
        window.blit(bg,pos,rect_bg)
        window.blit(pokeball_sprite_open, pos)
        pygame.display.flip()
        utils.delay_flat(0.1)
        # flash écran ou qqch
        window.blit(bg,pos,rect_bg)
        utils.delay_flat(0.2)
            
def init_trainer():       
    from pokemon_init import leviator,dracaufeu,gengar   
    trainer_ai = Pokemon_trainer("Red","hgss_champion.mp3","luxuryball")
    trainer_ai.catch_pokemon(dracaufeu)
    # trainer_ai.catch_pokemon(gengar)
    trainer = Pokemon_trainer("Brandon")
    trainer.catch_pokemon(leviator)
    gengar_trainer = deepcopy(gengar)
    trainer.catch_pokemon(gengar_trainer)
    
    assert gengar_trainer != gengar
    # print(trainer_ai,trainer,sep="\n")

    trainer.set_team_into_json("trainer")
    trainer_ai.set_team_into_json("opponent")
    utils.update_battle_json({"current": [1,1]})
    return trainer,trainer_ai

def get_winner(trainer1,trainer2):
    winner,loser = None,None
    hp_total_trainer1 = sum([pokemon.hp for pokemon in trainer1.pokemon_team])
    hp_total_trainer2 = sum([pokemon.hp for pokemon in trainer2.pokemon_team])
    
    if hp_total_trainer1 <= 0 and hp_total_trainer2 > 0:
        winner,loser = trainer2,trainer1
    elif hp_total_trainer1 > 0 and hp_total_trainer2 <= 0:
        winner,loser = trainer1,trainer2
    return winner,loser
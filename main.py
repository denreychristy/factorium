# Factorium: Main

# ================================================================================================ #
# Imports

from time import time

import pygame as pg

from modules import *

# ================================================================================================ #

class Factorium:
	def __init__(self):
		pg.init()

		self.clock = pg.time.Clock()
		self.fps = 120

		self.COLORS = {
			'black': (0, 0, 0),
			'grey': (31, 31, 31),
			'orange': (181, 109, 59)
		}

		self.inventory: Inventory = Inventory()

		# ==================== #
		# Window & Main Surface
		self.window_surf = pg.display.set_mode((800, 1200), pg.RESIZABLE)
		self.window_rect = self.window_surf.get_frect()

		self.main_surf = pg.surface.Surface((
			self.window_rect.width,
			max(self.window_rect.height, 2000)
		))
		self.main_rect = self.main_surf.get_rect()
		self.main_surf_color: tuple[int, int, int] = self.COLORS['grey']
		self.main_surf.fill(self.main_surf_color)

		self.last_mouse_position = pg.mouse.get_pos()

		# ==================== #
		# Text Objects
		self.font = pg.font.Font('assets/Full Automation/Full Automation.otf', 50)
		self.debug_font = pg.font.Font(pg.font.get_default_font(), 20)

		self.text_boxes: TextBoxList = TextBoxList()
		self.text_boxes.add(
			TextBox(
				'Factorium', font = self.font, center = (self.main_rect.centerx, 100),
				background_color = self.COLORS['orange'], border_radius = 30, padding = 10
			),
			ValueTextBox(
				lambda: self.inventory.get_formatted_str('wood'), center = (200, 300),
				background_color = self.COLORS['orange'], border_radius = 10, border_width = 5,
				padding = 20
			),
			ValueTextBox(
				lambda: self.inventory.get_formatted_str('coal'), center = (200, 370),
				background_color = self.COLORS['orange'], border_radius = 10, border_width = 5,
				padding = 20
			)
		)

		# ==================== #
		# Buttons
		self.buttons: ButtonList = ButtonList()
		self.buttons.add(
			Button(
				'Collect', center = (400, 300), on_click = lambda: self.inventory.update('wood', 1),
				background_color = self.COLORS['orange'], border_radius = 10, border_width = 5,
				padding = 20
			),
			Button(
				'Mine', center = (400, 370), on_click = lambda: self.inventory.update('coal', 1),
				background_color = self.COLORS['orange'], border_radius = 10, border_width = 5,
				padding = 20
			)
		)

		# ==================== #
		# Load Assets
		self.images_path: str = 'assets/images/'
		self.IMAGES = {}
		for name in ['coal', 'wood']:
			image = pg.transform.scale(
				pg.image.load(self.images_path + name + '.png').convert_alpha(),
				(50, 50)
			)
			self.IMAGES[name] = {
				'surf': image,
				'rect': image.get_frect()
			}
		self.IMAGES['wood']['rect'].center = (50, 300)
		self.IMAGES['coal']['rect'].center = (50, 370)

	def run(self):
		self.flag_run: bool = True
		while self.flag_run:
			self.clock.tick(self.fps)

			self.user_input()
			self.update()
			self.display()
		pg.quit()
	
	# ================================================== #
	# User Input
	# ================================================== #

	def user_input(self):
		for event in pg.event.get():
			self.handle_quit(event)

			if event.type == pg.MOUSEBUTTONDOWN:
				self.last_mouse_position = pg.mouse.get_pos()
			
			elif event.type == pg.MOUSEBUTTONUP:
				self.buttons.check_click(pg.mouse.get_pos())
		
		self.handle_vertical_scrolling()
	
	def handle_quit(self, event) -> None:
		if event.type == pg.QUIT:
			self.flag_run = False
	
	def handle_vertical_scrolling(self) -> None:
		if pg.mouse.get_pressed()[0]:
			current_mouse_position = pg.mouse.get_pos()
			self.main_rect.y += current_mouse_position[1] - self.last_mouse_position[1]
			self.last_mouse_position = current_mouse_position

			# Keep main_surf on the screen
			self.main_rect.y = min(self.main_rect.y, 0)
			self.main_rect.bottom = max(self.main_rect.bottom, self.window_rect.bottom)
	
	# ================================================== #
	# Update
	# ================================================== #

	def update(self):
		self.buttons.update()
		self.text_boxes.update()

	# ================================================== #
	# Display
	# ================================================== #

	def display_item_images(self):
		for key, value in self.IMAGES.items():
			surf, rect = value['surf'], value['rect']
			self.main_surf.blit(surf, rect)
	
	def show_debug(self):
		fps_surf = self.debug_font.render(
			str(int(self.clock.get_fps())), True, (255, 255, 255), (0, 0, 0)
		)
		fps_rect = fps_surf.get_rect()
		self.window_surf.blit(fps_surf, fps_rect)

	def display(self):
		self.window_surf.fill(self.COLORS['black'])

		# Main Surf
		self.main_surf.fill(self.main_surf_color)
		self.display_item_images()
		self.buttons.display(self.main_surf)
		self.text_boxes.display(self.main_surf)
		self.window_surf.blit(self.main_surf, self.main_rect)

		self.show_debug()

		pg.display.flip()

# ================================================================================================ #

if __name__ == '__main__':
	game = Factorium()
	game.run()
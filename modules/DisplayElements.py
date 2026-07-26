# Factorium: Display Elements

# ================================================================================================ #
# Imports

from time import time
from typing import Callable

import pygame as pg

# ================================================================================================ #

class TextBox:
	def __init__(self, text: str, **kwargs):
		if not pg.font.get_init(): pg.font.init()

		# Text
		self._text: str = text
		self._last_text: str = text
		self.font_size: int = kwargs.get('font_size', 20)
		self.font: pg.font.Font = kwargs.get(
			'font',
			pg.font.Font(pg.font.get_default_font(), self.font_size)
		)
		self.text_color: tuple[int, int, int] = kwargs.get('text_color', (255, 255, 255))
		self.text_surf: pg.surface.Surface = self.font.render(self.text, True, self.text_color)
		self.text_rect: pg.rect.Rect = self.text_surf.get_rect()
		
		# Background
		self.padding: int = kwargs.get('padding', 0)
		raw_box_size = kwargs.get('box_size', self.text_rect.size)
		self.box_size: tuple[int, int] = (
			max(raw_box_size[0], self.text_rect.width + 2 * self.padding),
			max(raw_box_size[1], self.text_rect.height + 2 * self.padding)
		)
		self.background_surf: pg.surface.Surface = pg.surface.Surface(self.box_size, pg.SRCALPHA)
		self.background_rect: pg.rect.Rect = self.background_surf.get_rect(
			center = kwargs.get('center', (0, 0))
		)
		self._background_color: tuple[int, int, int] = kwargs.get('background_color', (0, 0, 0, 0))
		self.border_width: int = kwargs.get('border_width', 0)
		self.border_radius: int = kwargs.get('border_radius', 0)
		pg.draw.rect(
			self.background_surf,
			self.background_color,
			(0, 0, self.background_rect.width, self.background_rect.height),
			self.border_width,
			self.border_radius
		)

		self.text_rect.center = self.local_center
		self.background_surf.blit(self.text_surf, self.text_rect)

		self._is_active: Callable[[], bool] = kwargs.get('is_active', lambda: True)
	
	@property
	def background_color(self) -> tuple[int, int, int]:
		return self._background_color

	@property
	def text(self) -> str:
		return self._text
	
	@property
	def is_active(self) -> bool:
		return self._is_active()

	@property
	def local_center(self) -> tuple[int, int]:
		return (
			self.background_rect.width // 2,
			self.background_rect.height // 2
		)
	
	def render(self):
		self.text_surf = self.font.render(self.text, True, self.text_color)
		self.text_rect = self.text_surf.get_rect(center = self.local_center)
		self._last_text = self.text

		self.background_surf.fill((0, 0, 0, 0), special_flags=pg.BLEND_RGBA_MIN)

		pg.draw.rect(
			self.background_surf,
			self.background_color,
			(0, 0, self.background_rect.width, self.background_rect.height),
			self.border_width,
			self.border_radius
		)
		
		self.background_surf.blit(self.text_surf, self.text_rect)
	
	def update(self, **kwargs):
		if self.text != self._last_text:
			self.render()
	
	def display(self, target_surface: pg.surface.Surface):
		if not self.is_active: return

		target_surface.blit(self.background_surf, self.background_rect)

# ================================================================================================ #

class ValueTextBox(TextBox):
	def __init__(self, text: Callable[[], str], **kwargs):
		self._text_callable: Callable[[], str] = text
		super().__init__('', **kwargs)
	
	@property
	def text(self) -> str:
		if not hasattr(self, '_text_callable'):
			return ''
		return self._text_callable()

# ================================================================================================ #

class TextBoxList:
	def __init__(self):
		self.text_boxes: list[TextBox | ValueTextBox] = []
	
	def add(self, *text_boxes: TextBox | ValueTextBox) -> None:
		for text_box in text_boxes:
			self.text_boxes.append(text_box)
	
	def update(self, **kwargs) -> None:
		for text_box in self.text_boxes:
			text_box.update(**kwargs)
	
	def display(self, target_surface: pg.surface.Surface) -> None:
		for text_box in self.text_boxes:
			text_box.display(target_surface)

# ================================================================================================ #

class Button(TextBox):
	def __init__(self, text: str, **kwargs):
		self._last_clicked: float = 0.0
		self._clicked_flag: bool = False
		super().__init__(text, **kwargs)
		self._on_click: Callable[[], None] = kwargs.get(
			'on_click',
			lambda: print(f'"{self.text}" button clicked!')
		)
	
	@property
	def background_color(self) -> tuple[int, int, int]:
		if self.was_recently_clicked:
			return (
				255 - self._background_color[0],
				255 - self._background_color[1],
				255 - self._background_color[2]
			)
		return self._background_color
	
	@property
	def was_recently_clicked(self) -> bool:
		return (time() - self._last_clicked) < .1
	
	def check_click(self, mouse_position: tuple[float, float]) -> bool:
		if not self.background_rect.collidepoint(mouse_position): return False

		self._on_click()
		self._last_clicked = time()
		self._clicked_flag = True
		return True
	
	def update(self, **kwargs):
		if self.text != self._last_text:
			self.render()
		
		# Show alternate configuration when clicked
		if self.was_recently_clicked:
			self.render()
		elif self._clicked_flag:
			self._clicked_flag = False
			self.render()

# ================================================================================================ #

class ButtonList:
	def __init__(self):
		self.buttons: list[Button] = []
	
	def add(self, *buttons: Button) -> None:
		for button in buttons:
			self.buttons.append(button)
	
	def check_click(self, mouse_position: tuple[int, int]) -> bool:
		for button in self.buttons:
			if button.check_click(mouse_position):
				return True
		return False
	
	def update(self, **kwargs) -> None:
		for button in self.buttons:
			button.update(**kwargs)
	
	def display(self, target_surface: pg.surface.Surface) -> None:
		for button in self.buttons:
			button.display(target_surface)
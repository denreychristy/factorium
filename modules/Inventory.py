# Factorium: Inventory

# ================================================================================================ #

class Inventory:
	def __init__(self):
		self._inventory: dict[str, float] = {
			'coal': 0,
			'wood': 0
		}
	
	def update(self, item: str, amount: float) -> None:
		self._inventory[item] += amount
	
	def get(self, item: str) -> float:
		return self._inventory[item]
	
	def get_formatted_str(self, item: str) -> str:
		value = self.get(item)
		
		if value < 1000:
			return str(int(value))
		
		# Format as scientific notation with 2 decimal places (e.g. 2.35e+03)
		formatted = f"{value:.2e}"
		base, exponent = formatted.split('e')
		
		# Convert exponent "+03" -> 3
		exp_num = int(exponent)
		
		return f"{base} x 10^{exp_num}"
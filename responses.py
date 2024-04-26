from random import choice, randint

def get_response(user_input: str) -> str:
	lowered: str = user_input.lower()

	if lowered == '':
		return 'digita alguma merda'
	elif 'bezinho' in lowered:
		return 'Cala a boca porra!'
	elif 'viado' in lowered:
		return 'teu pai'
	elif 'boiola' in lowered:
		return 'tua tia'
	elif 'tigrinho' in lowered:
		return f'olha a cartinha: {randint(1, 6)}'

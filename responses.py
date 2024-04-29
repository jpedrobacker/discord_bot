from random import choice, randint

def get_response(user_input: str) -> str:
	lowered: str = user_input.lower()

	if lowered == '':
		return 'Say something dammit!!!'
	elif 'Pizza' in lowered:
		return 'My cousin have a place'
	elif 'Hey' in lowered:
		return 'How you doing'
	elif 'tigrinho' in lowered:
		return f'olha a cartinha: {randint(1, 6)}'

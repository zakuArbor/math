all:
	manim -pql --save_sections main.py Main
test:
	manim -pql example.py OpeningManimExample
prod:
	manim -pqh --save_sections main.py Main
editor:
	cd media && manedit

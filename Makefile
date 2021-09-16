default:
	pdflatex main
	biber main
	makeglossaries main
	pdflatex main
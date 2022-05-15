build:
	pdflatex main
	biber main
	makeglossaries main
	pdflatex main

cleanup:
	@rm -f main.acn
	@rm -f main.aux
	@rm -f main.bbl
	@rm -f main.bcf
	@rm -f main.blg
	@rm -f main.fdb_latexmk
	@rm -f main.fls
	@rm -f main.glo
	@rm -f main.ist
	@rm -f main.log
	@rm -f main.out
	@rm -f main.pdf
	@rm -f main.run.xml
	@rm -f main.synctex.gz
	@rm -f main.toc

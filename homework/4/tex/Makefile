all: build/homework.pdf
	cp build/homework.pdf homework.pdf
	cp homework.pdf ../HW4_harnisc6.pdf


TeXOptions = -lualatex \
			 -interaction=nonstopmode \
			 -halt-on-error \
			 -output-directory=build
                                                                                
build/homework.pdf: FORCE | build
	latexmk $(TeXOptions) homework.tex
	
FORCE:

build:
	mkdir -p build/

clean:
	rm -rf build

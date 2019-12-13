all: build/homework.pdf
	cp build/homework.pdf homework.pdf
	cp homework.pdf ../HW7_harnisc6.pdf

TeXOptions = -pdf \
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

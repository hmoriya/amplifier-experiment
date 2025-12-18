# Book to PDF Makefile

.PHONY: install dev test check convert preview clean help

# Default target
help:
	@echo "Book to PDF - Available targets:"
	@echo "  install    Install the module and dependencies"
	@echo "  dev        Install in development mode with dev dependencies"
	@echo "  test       Run tests"
	@echo "  check      Run linting and type checks"
	@echo "  convert    Convert the book to PDF (all parts)"
	@echo "  preview    Start HTML preview server"
	@echo "  clean      Clean generated files"
	@echo ""
	@echo "Examples:"
	@echo "  make install        # Install the module"
	@echo "  make convert        # Generate PDF"
	@echo "  make PART=1 convert # Generate only Part 1"

# Install dependencies
install:
	uv pip install -e .

# Install with dev dependencies
dev:
	uv pip install -e ".[dev]"

# Run tests
test:
	uv run pytest tests/ -v

# Check code quality
check:
	uv run ruff check .
	uv run mypy amplifier_module_book_to_pdf/

# Convert book to PDF
convert:
	@if [ -n "$(PART)" ]; then \
		echo "Converting Part $(PART) to PDF..."; \
		uv run book2pdf convert --part $(PART); \
	else \
		echo "Converting entire book to PDF..."; \
		uv run book2pdf convert; \
	fi

# Start preview server
preview:
	uv run book2pdf preview

# Clean generated files
clean:
	rm -rf output/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf *.egg-info/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Quick conversion shortcuts
part1:
	make PART=1 convert

part2:
	make PART=2 convert

part3:
	make PART=3 convert

part4:
	make PART=4 convert

appendices:
	make PART=5 convert  # Assuming appendices are treated as part 5

# Check dependencies
check-deps:
	uv run book2pdf check-dependencies

# Check fonts
check-fonts:
	uv run book2pdf check-fonts
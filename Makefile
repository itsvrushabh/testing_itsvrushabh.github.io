.PHONY: test report test-ui test-terminal test-nav test-theme test-seo headed clean

test:
	uv run behave

report:
	uv run behave -f behave_html_formatter:HTMLFormatter -o reports/report.html -f pretty

test-ui:
	uv run behave --tags=@ui

test-terminal:
	uv run behave --tags=@terminal

test-nav:
	uv run behave --tags=@navigation

test-theme:
	uv run behave --tags=@theme

test-seo:
	uv run behave --tags=@seo

headed:
	uv run behave -D headless=false

clean:
	rm -rf reports/*.html screenshots/*.png .pytest_cache/

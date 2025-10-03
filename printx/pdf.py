import asyncio
import frappe
from pyppeteer import launch
from frappe.utils import get_url
from typing import Optional, Dict, Any

class PyppeteerPDF:
    def __init__(self, html: str, options: Optional[Dict[str, Any]] = None):
        self.html = html
        self.options = options or {}
        self.default_options = {
            'viewport': {
                'width': 800,
                'height': 600,
                'deviceScaleFactor': 1,
            },
            'pdf': {
                'printBackground': True,
                'format': 'A4',
                'margin': {
                    'top': '15mm',
                    'right': '15mm',
                    'bottom': '15mm',
                    'left': '15mm'
                }
            }
        }

    async def _generate_pdf(self) -> bytes:
        """Generate PDF using pyppeteer"""
        browser = await launch(handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False)
        try:
            page = await browser.newPage()
            
            # Set viewport
            viewport_options = {**self.default_options['viewport'], **self.options.get('viewport', {})}
            await page.setViewport(viewport_options)

            # Get custom CSS/JS from settings
            settings = frappe.get_doc('PrintX Settings', 'PrintX Settings')
            custom_css = settings.custom_css if settings.enable_custom_css else ""
            custom_js = settings.custom_js if settings.enable_custom_js else ""

            # Inject custom CSS and JS
            html_with_customization = f"""
                <style>{custom_css}</style>
                {self.html}
                <script>{custom_js}</script>
            """
            
            # Set content and wait for network idle
            await page.setContent(html_with_customization, {'waitUntil': 'networkidle0'})
            
            # Generate PDF with options
            pdf_options = {**self.default_options['pdf'], **self.options.get('pdf', {})}
            pdf_data = await page.pdf(pdf_options)
            
            return pdf_data
        finally:
            await browser.close()

    def get_pdf(self) -> bytes:
        """Synchronous wrapper for PDF generation"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(self._generate_pdf())
        finally:
            loop.close()

def get_pdf(html: str, options: Optional[Dict[str, Any]] = None) -> bytes:
    """Helper function to generate PDF"""
    generator = PyppeteerPDF(html, options)
    return generator.get_pdf()


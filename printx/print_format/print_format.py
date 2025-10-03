import frappe
from printx.pdf import get_pdf

def generate_pdf(print_format=None, html=None, options=None, output=None, pdf_generator=None):
    """Hook function for PDF generation"""
    if pdf_generator != "PrintX":
        return None
    
    try:
        # Get settings
        settings = frappe.get_doc('PrintX Settings', 'PrintX Settings')
        
        # Prepare options
        pdf_options = {
            'viewport': {
                'width': settings.default_width,
                'height': settings.default_height,
                'deviceScaleFactor': settings.device_scale_factor,
            },
            'pdf': {
                'format': settings.default_format,
                'printBackground': settings.print_background,
            }
        }
        
        # Merge with provided options
        if options:
            pdf_options = frappe.utils.deep_merge(pdf_options, options)
        
        # Generate PDF
        pdf_data = get_pdf(html, pdf_options)
        
        if output:
            output.write(pdf_data)
            return True
        
        return pdf_data
        
    except Exception as e:
        if settings.debug_mode:
            frappe.throw(e)
        else:
            frappe.log_error(f"PrintX PDF Generation Error: {str(e)}", "PrintX Error")


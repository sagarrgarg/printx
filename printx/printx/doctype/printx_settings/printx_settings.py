import frappe
from frappe.model.document import Document

class PrintXSettings(Document):
    def validate(self):
        if self.enable_custom_css and not self.custom_css:
            frappe.throw("Custom CSS is enabled but no CSS code provided")
        
        if self.enable_custom_js and not self.custom_js:
            frappe.throw("Custom JavaScript is enabled but no JS code provided")
        
        if self.device_scale_factor <= 0:
            frappe.throw("Device Scale Factor must be greater than 0")


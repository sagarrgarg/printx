import frappe

def add_pdf_generator_option():
    fieldname = "pdf_generator"
    doctype = "Print Format"

    frappe.logger().info("🔧 PrintX: Adding PDF generator option via Property Setter...")

    try:
        # Check if property setter already exists
        ps = frappe.get_all("Property Setter", 
            filters={
                "doc_type": doctype,
                "field_name": fieldname,
                "property": "options"
            }
        )
        if ps:
            frappe.logger().info("ℹ️ PrintX Property Setter already exists, skipping.")
            return

        df = frappe.get_meta(doctype).get_field(fieldname)
        if not df:
            frappe.logger().error(f"❌ PrintX: Field {fieldname} not found in {doctype}")
            return

        options = df.options.split("\n") if df.options else []
        if "PrintX" not in options:
            options.append("PrintX")

        # Create property setter
        ps = frappe.make_property_setter({
            "doctype": doctype,
            "fieldname": fieldname,
            "property": "options",
            "value": "\n".join(options),
            "property_type": "Text"
        }, validate_fields_for_doctype=False)

        frappe.db.commit()
        frappe.logger().info("✅ PrintX: Property Setter created and saved")

        frappe.clear_cache(doctype=doctype)
        frappe.logger().info("🔄 Cache cleared for Print Format")

    except Exception as e:
        frappe.log_error(message=str(e), title="PrintX Install Error")
        frappe.logger().error(f"❌ PrintX: Failed to add option — {e}")

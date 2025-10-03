import frappe

def remove_pdf_generator_option():
    frappe.logger().info("🔧 PrintX: Removing Property Setter...")

    try:
        ps_list = frappe.get_all("Property Setter", 
            filters={
                "doc_type": "Print Format",
                "field_name": "pdf_generator",
                "property": "options"
            },
            pluck="name"
        )

        if not ps_list:
            frappe.logger().info("ℹ️ No PrintX Property Setter found, nothing to remove.")
            return

        for ps_name in ps_list:
            frappe.delete_doc("Property Setter", ps_name, force=True)
            frappe.logger().info(f"🗑️ Deleted Property Setter: {ps_name}")

        frappe.db.commit()
        frappe.clear_cache(doctype="Print Format")
        frappe.logger().info("🔄 Cache cleared for Print Format")

    except Exception as e:
        frappe.log_error(message=str(e), title="PrintX Uninstall Error")
        frappe.logger().error(f"❌ PrintX: Failed to remove option — {e}")

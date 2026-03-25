frappe.ui.form.on(cur_frm.doctype, {
    refresh: function (frm) {
        frm.trigger('custom_is_parent_partner');
        frm.set_query("custom_parent_partner", function () {
            return {
                filters: {
                    "custom_is_parent_partner": 1,
                    "name": ["!=", frm.doc.name] // Prevent self-linking selection
                }
            };
        });
    },
    custom_is_parent_partner: function (frm) {
        // Hide parent partner link field if this company is a parent
        if (frm.doc.custom_is_parent_partner) {
            frm.set_df_property('custom_parent_partner', 'hidden', 1);
            frm.set_value('custom_parent_partner', '');
        } else {
            frm.set_df_property('custom_parent_partner', 'hidden', 0);
        }
    }
});

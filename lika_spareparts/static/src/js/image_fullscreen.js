/** @odoo-module **/

import { registry } from "@web/core/registry";
import { ImageField, imageField } from "@web/views/fields/image/image_field";
import { Dialog } from "@web/core/dialog/dialog";
import { Component, xml } from "@odoo/owl";

class ImageLightboxDialog extends Component {
    static template = xml`
        <Dialog title="props.title" size="'xl'">
            <div class="d-flex justify-content-center align-items-center p-3 bg-dark rounded">
                <img :src="props.src" class="img-fluid" style="max-height: 85vh; object-fit: contain;" />
            </div>
        </Dialog>
    `;
    static components = { Dialog };
}

export class FullscreenImageField extends ImageField {
    onClick(ev) {
        // Prevent default upload trigger if image exists
        const src = this.getUrl(this.props.name);
        if (src && !src.includes("placeholder")) {
            ev.stopPropagation();
            this.env.services.dialog.add(ImageLightboxDialog, {
                src: src,
                title: this.props.record.data.display_name || "Part Diagram",
            });
            return;
        }
        super.onClick(...arguments);
    }

    onFileDownload(ev) {
        this.onClick(ev);
    }
}

export const fullscreenImageField = {
    ...imageField,
    component: FullscreenImageField,
};

registry.category("fields").add("image_fullscreen", fullscreenImageField);
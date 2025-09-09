/** @odoo-module **/
import { registry } from "@web/core/registry";
const { Component, onMounted } = owl;

export class VideoWidget extends Component {
    static template = 'VideoWidget';
    setup() {
        onMounted(this.mount);
        super.setup();
    }
    mount() {
        this.el.querySelector('source').src = this.props.value;
    }
}
registry.category("fields").add("videoWidget", VideoWidget);

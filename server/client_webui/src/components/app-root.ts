import { LitElement, html, css } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('app-root')
export class AppRoot extends LitElement {
    static styles = css`
        /* Add any custom styles for the app-root component here */
        :host {
            display: block;
            padding: 16px;
            background-color: var(--app-background-color, #ffffff);
        }
    `;

    render() {
        return html`
        1
            <header>
                <h1>Welcome to the Client Web UI</h1>
            </header>
            <main>
            hi  
            </main>
        `;
    }
}
import { html, css, LitElement } from 'lit';
import './components/app-root';

export class MyApp extends LitElement {
  static styles = css`
    :host {
      display: block;
      height: 100vh;
      background-color: var(--app-background-color, #f0f0f0);
    }
  `;

  render() {
    return html`
      <app-root></app-root>
    `;
  }
}

customElements.define('client-ui', MyApp);

const app = document.createElement('client-ui');
document.body.appendChild(app);
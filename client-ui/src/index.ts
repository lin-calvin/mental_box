import { LitElement, html, css } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import {default as state} from 'store.js'


@customElement('client-ui')
export class ClientUI extends LitElement {
  constructor() {
    super();
  }
  static styles = css`
    :host {
      display: block;
      padding: 16px;
      max-width: 800px;
      margin: 0 auto;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    
    .container {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    h1 {
      color: #333;
      margin-top: 0;
    }
  `;

  render() {
    return html`
      <div class="container">
        <h1>Hello, ${this.name}!</h1>
        <p>.</p>
        <slot></slot>
      </div>
    `;
  }
}

const appElement = document.createElement('client-ui');
document.body.appendChild(appElement);
// Insert the element into the DOM once the page is loaded

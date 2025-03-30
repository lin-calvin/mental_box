window.process = { env: { NODE_ENV: 1 } };
import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";
import { default as store, Stage, changeStage } from "./store.js";
window.store = store;
console.log(process.env.NODE_ENV);
import install from "@twind/with-web-components";
import config from "../twind.config.js";
const withTwind = install(config);
import { WelcomePage } from "./pages/welcome.ts";
import { BASE_URL } from "./const.ts";
@customElement("client-ui")
@withTwind
export class ClientUI extends LitElement {
  constructor() {
    super();
    store.subscribe(() => {
      console.log(1);
      this.update({});
    });
  }
  pages = {
    [Stage.IDLE]: new WelcomePage(),
    [Stage.READING]: html``,
  };
  static styles = css`
    /* @tailwind base;
    @tailwind components;
    @tailwind utilities;
    :host {
      display: block;
      padding: 16px;
      background-color: var(--color-gray-100);

      margin: 0 auto;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
    } */
  `;
  async start() {
    //await fetch(BASE_URL + "test");
    window.store.dispatch(changeStage(Stage.READING));
  }
  render() {
    return html`${this.pages[store.getState().appState.stage]} `;
  }
}

//const appElement = document.createElement('client-ui');
//document.body.appendChild(appElement);
// Insert the element into the DOM once the page is loaded

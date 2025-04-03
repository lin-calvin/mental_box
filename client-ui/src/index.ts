import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";
import { default as store, Stage, changeStage } from "./store.js";
window.store = store;
import install from "@twind/with-web-components";
import config from "../twind.config.js";
const withTwind = install(config);
import { WelcomePage } from "./pages/welcome.ts";
import { ReadingPage } from "./pages/reading.ts";

import { BASE_URL } from "./const.ts";
console.log(process.env.NODE_ENV);
@customElement("client-ui")
@withTwind
export class ClientUI extends LitElement {
  constructor() {
    super();
    store.subscribe(() => {
      this.update({});
    });
  }
  pages = {
    [Stage.IDLE]: new WelcomePage(),
    [Stage.READING]: new ReadingPage(),
  };
  render() {
    return html`${this.pages[store.getState().appState.stage]} `;
  }
}

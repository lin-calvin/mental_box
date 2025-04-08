import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";
import { default as store, Stage, changeStage } from "./store.js";
window.store = store;
import install from "@twind/with-web-components";
import config from "../twind.config.js";
const withTwind = install(config);
import { WelcomePage } from "./pages/welcome.ts";
import { ReadingPage } from "./pages/reading.ts";
import { RespondingPage } from "./pages/responding.ts";

import { BASE_URL } from "./const.ts";
@customElement("client-ui")
@withTwind
export class ClientUI extends LitElement {
  currentPage=Stage.IDLE
  constructor() {
    super();
    store.subscribe(() => {
      console.log(1);
      if (this.currentPage!=store.getState().appState.stage ) {
        this.currentPage=store.getState().appState.stage;
        this.update({});
      }
    });
  }
  pages = {
    [Stage.IDLE]: new WelcomePage(),
    [Stage.READING]: new ReadingPage(),
    [Stage.RESPONDING]: new RespondingPage()
  };
  render() {
    return html`${this.pages[store.getState().appState.stage]} `;
  }
}

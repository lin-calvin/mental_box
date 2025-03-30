import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";
import { default as state, Stage, changeStage } from "../store.js";
console.log(process.env.NODE_ENV);
import install from "@twind/with-web-components";
import config from "../../twind.config.js";
const withTwind = install(config);
import { BASE_URL } from "../const.ts";
@customElement("page-welcome")
@withTwind
export class WelcomePage extends LitElement {
  constructor() {
    super();
  }
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
    await fetch(BASE_URL + "test");
    //console.log(changeStage(Stage.READING));
    window.store.dispatch(changeStage(Stage.READING));
  }
  render() {
    return html`
        <div class="text-white bg-black h-screen items-center ">
            <div class="flex justify-center items-center h-screen">
                <div
                  @click="${() => {
                    this.start();
                  }}"
                    class=" mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg outline outline-black/5 dark:bg-slate-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10  hover:bg-sky-700"
                >
                    <p class="text-xl font-medium font-sans">hello-world!</h1>
                </div>
            </div>
        </div>
    `;
  }
}

//const appElement = document.createElement('client-ui');
//document.body.appendChild(appElement);
// Insert the element into the DOM once the page is loaded

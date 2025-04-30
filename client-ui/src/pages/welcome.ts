import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";
import { BASE_URL } from "../const.ts";
import { default as store, Stage, changeStage } from "../store.js";
import install from "@twind/with-web-components";
import config from "../../twind.config.js";
const withTwind = install(config);
@customElement("page-welcome")
@withTwind
export class WelcomePage extends LitElement {
  connectedCallback(): void {
    if(!store.getState()._CLEAN){
    store.dispatch({ type: 'RESET' }); //calls the root reducer with RESET as action!
  }
  super.connectedCallback();
    
  }
  async start() {
    await fetch(BASE_URL + "run");
    
    window.store.dispatch(changeStage(Stage.READING));
  }

  render() {
    return html`
      <div class="text-white bg-black h-screen items-center">
      
        <div class="flex flex-col justify-center items-center h-screen">
        <div><p class="text-2xl">单击以开始</p></div>
        
          <div
            @click="${() => {
              this.start();
            }}"
            class="m-5  px-10 mx-auto flex max-w-sm items-center gap-x-4 rounded-xl bg-white p-6 shadow-lg outline outline-black/5 dark:bg-slate-800 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10 hover:bg-sky-700"
          >
            <p class="text-xl font-medium font-sans">Start</p>
          </div>
        </div>
      </div>
    `;
  }
}

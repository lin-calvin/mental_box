import { default as store, Stage, changeStage } from "../store.js";
import { LitElement, html, css } from "lit";
import { customElement } from "lit/decorators.js";
import { BASE_URL } from "../const.ts";
import install from "@twind/with-web-components";
import config from "../../twind.config.js";
const withTwind = install(config);
console.log(process.env.NODE_ENV);
@customElement("page-responding")
@withTwind
export class RespondingPage extends LitElement {
    constructor() {
        super();
        // store.subscribe((() => {
        //   this.update();
        // }));
      }
      connectedCallback() {
        super.connectedCallback()
                store.subscribe((() => {
          this.update();
        }));
        setTimeout(()=>{store.dispatch(changeStage(Stage.IDLE))},10000);
      }

      render() {
        
        const data=store.getState().serverState.data;
        // if (!data){data=""}
        return html`
        
<div class="text-white bg-black h-screen items-center">
  <div class="p-10 text-3xl">System is writing respond,</div>
  <div class="flex justify-center items-center h-screen italic">
    <p>${data.data}</p>
  </div>
</div>
        `;
      }
    }
    
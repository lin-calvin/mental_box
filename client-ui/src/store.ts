import {
  configureStore,
  createSlice,
  PayloadAction,
  ReducerType,
} from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import { BASE_URL } from "./const.js";
enum Stage {
  IDLE,
  READING,
  RESPONDING,
}

const appState = createSlice({
  name: "app",
  initialState: { stage: Stage.IDLE },
  reducers: {
    changeStage: (state, action: PayloadAction<Stage>) => {
      state.stage = action.payload;
    },
  },
});
const serverState = createSlice({
  name: "server",
  initialState: { data: {} },
  reducers: {
    pushServerState: (state, action: PayloadAction) => {
      console.log("Pushing server state: ", action.payload);
      state.data = action.payload;
    },
  },
});

const reducers = combineReducers({
  serverState: serverState.reducer,
  appState: appState.reducer,
});

const rootReducer = (state, action) => {
  if (action.type === 'RESET') {
     return reducers(undefined, action);
  }
  
  return reducers(state,action);
 };
const store = configureStore({
  devTools: true,
  reducer: rootReducer,
});
let eventstream = new EventSource(BASE_URL + "event");
eventstream.onmessage = ((event) => {
  console.log("Received event: ", event.data);
  let data = JSON.parse(event.data)
  store.dispatch(serverState.actions.pushServerState(JSON.parse(event.data)));
  store.dispatch(appState.actions.changeStage({ ocr: Stage.READING, final: Stage.RESPONDING, print_finish:Stage.IDLE }[data.event]));
}).bind(this);

export const { pushServerState } = serverState.actions;
export const { changeStage } = appState.actions;
export { Stage };
export default store;

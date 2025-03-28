import { configureStore, createSlice, PayloadAction, ReducerType } from '@reduxjs/toolkit';
import { combineReducers } from 'redux';
import {BASE_URL} from './const.js';
enum Stage {
    IDLE,
    PRINTING,
}

const appState = createSlice({
    name: "app",
    initialState: { stage: Stage.IDLE },
    reducers: {
        changeStage: (state, action: PayloadAction<Stage>) => {
            state.stage = action.payload;
        }
    }
});
const serverState= createSlice({
    name: "server",
    initialState: { data:{}},
    reducers: {
        pushServerState: (state, action: PayloadAction) => {
            console.log("Pushing server state: ", action.payload);
            state.data = action.payload;
        }
    }
});

const reducers = combineReducers({
    serverState: serverState.reducer,
    appState: appState.reducer
});

const store = configureStore({
    devTools: true,
    reducer: reducers
});

let eventstream = new EventSource(BASE_URL + "test_sse");
eventstream.onmessage= ((event) => {
    console.log("Received event: ", event.data);
    store.dispatch(serverState.actions.pushServerState(JSON.parse(event.data)));

}).bind(this);

export const { pushServerState } = serverState.actions;
export const { changeStage } = appState.actions;
export default store;
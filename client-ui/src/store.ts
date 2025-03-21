import { configureStore, createSlice, PayloadAction, ReducerType } from '@reduxjs/toolkit';
import { combineReducers } from 'redux'
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
            state.data = action.payload;
        }
    }
});

const reducers= combineReducers({
    serverState,
    appState
})
export const {pushServerState, changeStage} = reducers.actions;
export default reducers
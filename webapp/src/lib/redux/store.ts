import { configureStore } from '@reduxjs/toolkit';
// Or from '@reduxjs/toolkit/query/react'
import { reducer } from './rootReducer';
import { setupListeners } from '@reduxjs/toolkit/query/react';
import {
  healthApi,

} from './services';
import { combineReducers } from '@reduxjs/toolkit';
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const rootReducer = combineReducers({});

export type RootState = ReturnType<typeof rootReducer>;

export const store = configureStore({
  reducer,
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware().concat(
      healthApi.middleware,
    ),
});

// optional, but required for refetchOnFocus/refetchOnReconnect behaviors
// see `setupListeners` docs - takes an optional callback as the 2nd arg for customization
setupListeners(store.dispatch);

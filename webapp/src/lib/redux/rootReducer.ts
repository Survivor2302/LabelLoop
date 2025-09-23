/* Instruments */
import {
  healthApi,
} from './services';

export const reducer = {
  [healthApi.reducerPath]: healthApi.reducer,
};

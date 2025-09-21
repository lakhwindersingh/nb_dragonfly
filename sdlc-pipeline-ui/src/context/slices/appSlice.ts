import { createSlice } from '@reduxjs/toolkit';

interface AppState {
  // Extend later as needed
}

const initialState: AppState = {};

const appSlice = createSlice({
  name: 'app',
  initialState,
  reducers: {},
});

export default appSlice.reducer;

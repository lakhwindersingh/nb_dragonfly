import { createSlice } from '@reduxjs/toolkit';

interface ApprovalsState {
  // Placeholder state
}

const initialState: ApprovalsState = {};

const approvalsSlice = createSlice({
  name: 'approvals',
  initialState,
  reducers: {},
});

export default approvalsSlice.reducer;

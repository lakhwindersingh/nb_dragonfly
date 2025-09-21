import { createSlice } from '@reduxjs/toolkit';

interface RepositoriesState {
  // Placeholder state
}

const initialState: RepositoriesState = {};

const repositoriesSlice = createSlice({
  name: 'repositories',
  initialState,
  reducers: {},
});

export default repositoriesSlice.reducer;

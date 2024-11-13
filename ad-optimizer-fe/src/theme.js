// src/theme.js
import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#3f51b5",
    },
    secondary: {
      main: "#f50057",
    },
    mode: "light", // default to light mode
  },
  typography: {
    fontFamily: "Roboto, sans-serif",
  },
});

export default theme;

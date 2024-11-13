// src/components/Header.js
import React from "react";
import { AppBar, Toolbar, Typography, IconButton } from "@mui/material";
import { AdUnits } from "@mui/icons-material";

const Header = () => {
  return (
    <AppBar position="fixed">
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu">
          <AdUnits />
        </IconButton>
        <Typography variant="h6">Real Estate Ad Optimizer</Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
